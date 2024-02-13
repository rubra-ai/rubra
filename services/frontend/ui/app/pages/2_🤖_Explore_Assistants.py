# Standard Library

# Third Party
import streamlit as st
import streamlit_antd_components as sac
import streamlit_shadcn_ui as ui
from rubra_ui_config import get_entity_options, rubra_client
from rubra_ui_utils import remove_streamlit_elements


def get_all_assistants():
    all_assistants = []
    while True:
        response = rubra_client.beta.assistants.list(limit=100, after=after)
        assistants = response.data

        all_assistants.extend(assistants)

        if len(assistants) < 100:
            break
        else:
            after = assistants[-1]["id"]

    return all_assistants



def create_assistant(name, description, instructions, model, file_ids, tools):
    if file_ids:
        tools.append({"type": "retrieval"})
    print(tools)
    assistant = rubra_client.beta.assistants.create(
        name=name,
        description=description,
        instructions=instructions,
        tools=tools,
        model=model,
        file_ids=file_ids,
    )
    if assistant:
        st.session_state.entity_options = get_entity_options()
        st.success(
            f"Assistant '{name}' with model {model} created successfully!", icon="✅"
        )
    else:
        st.error("Failed to create assistant.")


def delete_assistant(assistant_id):
    try:
        rubra_client.beta.assistants.delete(assistant_id)
        st.session_state["delete_message"] = "Assistant deleted successfully."
        # Trigger a rerun
        st.session_state.entity_options = get_entity_options()
        st.rerun()
    except Exception as e:
        st.session_state["delete_message"] = f"Failed to delete: {e}"
        # Trigger a rerun
        st.rerun()


def modify_assistant(
    assistant_id,
    name,
    instructions,
    description,
    code_interpreter_status,
    browser_status,
):
    tools = []
    if code_interpreter_status:
        tools.append({"type": "code_interpreter"})
    if browser_status:
        tools.append({"type": "browser"})

    try:
        my_updated_assistant = rubra_client.beta.assistants.update(
            assistant_id,
            description=description,
            instructions=instructions,
            name=name,
            tools=tools,
        )
        if my_updated_assistant:
            st.session_state[
                "update_message"
            ] = f"Assistant '{name}' updated successfully."
            st.session_state[
                "modify_id"
            ] = None  # Reset the modify_id to close the modal
            st.rerun()
    except Exception as e:
        st.error(f"Failed to update assistant: {e}")


def get_configured_models():
    configured_models = rubra_client.models.list().data
    print(configured_models)
    return [model.id for model in configured_models]


def upload_files(uploaded_files):
    file_ids = []
    for uploaded_file in uploaded_files:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        uploaded_file = rubra_client.files.create(
            file=open(uploaded_file.name, "rb"), purpose="assistants"
        )
        # Wait for the file status to become 'uploaded'
        while uploaded_file.status != "uploaded":
            pass
        file_ids.append(uploaded_file.id)
    return file_ids


def main():
    st.markdown(
        f"<h1 style='color: #E53935;'>Rubra Assistants</h1>", unsafe_allow_html=True
    )

    # Creating a new assistant
    if st.button("Create New Assistant"):
        if "create_modal" not in st.session_state:
            st.session_state["create_modal"] = True
        else:
            st.session_state["create_modal"] = not st.session_state["create_modal"]

    if st.session_state.get("create_modal", False):
        with st.form("create_assistant_form"):
            name = st.text_input("Name", placeholder="Name your assistant.")
            description = st.text_area(
                "Description",
                value="",
                help="A short description to your assistant.",
                placeholder="Describe your assistant.",
            )
            instructions = st.text_area(
                "Instructions",
                value="",
                help="What does this assistant do? How should it behave?",
                placeholder="How should your assistant behave?",
            )
            models = get_configured_models()
            selected_model = st.selectbox("Model", models)
            code_interpreter = st.checkbox(
                "Code Interpreter",
                value=False,
                disabled=True,
                help="(Coming Soon) Enable Code Interpreter to execute code in your Assistant.",
            )
            browser = st.checkbox(
                "Browser",
                value=False,
                help="Enable Browser to open links in your Assistant.",
            )

            # File Uploader Section (not nested inside another expander)
            uploaded_files = st.file_uploader(
                "Knowledge",
                accept_multiple_files=True,
                help="If you upload files under Knowledge, conversations with your Assistant may include file contents. Files can be downloaded when Code Interpreter is enabled",
            )

            submit_button = st.form_submit_button(label="Create Assistant")

            if submit_button:
                # Check if all fields are filled before creating an assistant
                if name and selected_model:
                    file_ids = []
                    tools = []
                    if code_interpreter:
                        tools.append({"type": "code_interpreter"})
                    if browser:
                        tools.append({"type": "browser"})
                    if uploaded_files:
                        file_ids = upload_files(uploaded_files)
                        st.write("Uploaded File IDs:", file_ids)
                    create_assistant(
                        name, description, instructions, selected_model, file_ids, tools
                    )
                    st.session_state["create_modal"] = False
                else:
                    st.warning("Please fill in all fields before submitting.")

    # Placeholder for modification form
    modify_form_placeholder = st.empty()

    # Display the success/error message for update
    if "update_message" in st.session_state:
        st.success(st.session_state["update_message"], icon="✅")
        del st.session_state["update_message"]

    # Display the success/error message
    if "delete_message" in st.session_state:
        # This will display the message outside any columns or containers
        st.success(st.session_state["delete_message"], icon="✅")
        # Clear the message after displaying
        del st.session_state["delete_message"]

    # Display each assistant with delete and modify options
    for assistant in get_all_assistants():
        with st.container():
            st.markdown(f"### {assistant.name}")

            labels_to_add = [sac.Tag(label=assistant.model, color="blue", icon="cpu")]
            if assistant.model.startswith("gpt-"):
                labels_to_add.append(sac.Tag(label="OpenAI", icon="cloud"))
            if assistant.model.startswith("claude"):
                labels_to_add.append(sac.Tag(label="Anthropic", icon="cloud"))

            for t in assistant.tools:
                if t.type == "retrieval":
                    labels_to_add.append(
                        sac.Tag(label="Knowledge", color="green", icon="folder")
                    )
                if t.type == "code_interpreter":
                    labels_to_add.append(
                        sac.Tag(label="Code Interpreter", color="purple", icon="code")
                    )
                if t.type == "browser":
                    labels_to_add.append(
                        sac.Tag(label="Browser", color="orange", icon="browser-chrome")
                    )
            print(assistant.tools)

            sac.tags(
                labels_to_add,
                key=f"badges1-{assistant.id}",
            )

            if assistant.description:
                st.caption(f":green[**Description:**] {assistant.description}")
            if assistant.instructions:
                st.caption(f":blue[**Instructions:**] {assistant.instructions}")

            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button(f"Modify", key=f"modify_{assistant.id}"):
                    st.session_state["modify_id"] = assistant.id

            with col2:
                if ui.button(
                    f"Delete",
                    key=f"delete_{assistant.id}",
                    variant="destructive",
                ):
                    delete_assistant(assistant.id)

            st.divider()

    # Check if an assistant is selected for modification
    if "modify_id" in st.session_state and st.session_state["modify_id"]:
        modify_assistant_id = st.session_state["modify_id"]
        # Find the assistant details
        for assistant in get_all_assistants():
            if assistant.id == modify_assistant_id:
                with modify_form_placeholder.container():
                    with st.form(f"modify_{assistant.id}_form"):
                        new_name = st.text_input("New Name", value=assistant.name)
                        new_description = st.text_area(
                            "New Description", value=assistant.description
                        )
                        new_instructions = st.text_area(
                            "New Instructions", value=assistant.instructions
                        )

                        # Display the model but make it uneditable
                        st.text_input("Model", value=assistant.model, disabled=True)

                        # Add checkboxes for code interpreter and browser
                        code_interpreter_status = any(
                            tool.type == "code_interpreter" for tool in assistant.tools
                        )
                        browser_status = any(
                            tool.type == "browser" for tool in assistant.tools
                        )
                        new_code_interpreter_status = st.checkbox(
                            "Code Interpreter", value=code_interpreter_status
                        )
                        new_browser_status = st.checkbox(
                            "Browser", value=browser_status
                        )

                        submit_modification = st.form_submit_button("Update Assistant")

                        if submit_modification:
                            modify_assistant(
                                assistant.id,
                                new_name,
                                new_instructions,
                                new_description,
                                new_code_interpreter_status,
                                new_browser_status,
                            )
                            st.session_state[
                                "modify_id"
                            ] = None  # Reset modification state


if __name__ == "__main__":
    st.set_page_config(page_title="Rubra Assistants", page_icon="🐿", layout="wide")
    remove_streamlit_elements()
    main()
