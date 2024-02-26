# Standard Library

# Third Party
import streamlit as st
import streamlit_antd_components as sac
import streamlit_shadcn_ui as ui
from rubra_ui_config import get_entity_options, rubra_client, get_all_assistants
from rubra_ui_utils import remove_streamlit_elements



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
        success_message = f"Assistant '{name}' with model {model} created successfully!"
        if file_ids:
            success_message += " Knowledge Retrieval might take a few minutes to index file data."
        st.success(success_message, icon="✅")
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

def delete_file(file_id):
    try:
        rubra_client.files.delete(file_id)
        # st.success(f"File {file_id} deleted successfully.", icon="✅")
    except Exception as e:
        st.error(f"Failed to delete file: {e}")


def modify_assistant(
    assistant_id,
    name,
    instructions,
    description,
    code_interpreter_status,
    browser_status,
    file_ids=[],
    new_uploaded_files=None,
    files_to_delete=None,
):
    tools = []
    if code_interpreter_status:
        tools.append({"type": "code_interpreter"})
    if browser_status:
        tools.append({"type": "browser"})
    if files_to_delete:
        for file_id in files_to_delete:
            if file_id in file_ids:
                # delete_file(file_id)
                file_ids.remove(file_id)
    if new_uploaded_files:
        new_file_ids = upload_files(new_uploaded_files)
        # Append new file IDs to the existing ones
        file_ids.extend(new_file_ids)

    if not file_ids:
        tools = [tool for tool in tools if tool["type"] != "retrieval"]

    try:
        print("Updating assistant...")
        print("file_ids:", file_ids)
        print("tools:", tools)
        my_updated_assistant = rubra_client.beta.assistants.update(
            assistant_id,
            description=description,
            instructions=instructions,
            name=name,
            tools=tools,
            file_ids=file_ids,
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
                type=[".pdf", ".txt", ".md", ".log", ".rtf"],
                help="If you upload files for knowledge retrieval, conversations with your Assistant may include file contents. Upon Assistant creation, the file contents will be indexed for retrieval - this may take a moment.",
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


    if 'files_marked_for_deletion' not in st.session_state:
        st.session_state['files_marked_for_deletion'] = []

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
                        # code_interpreter_status = any(
                        #     tool.type == "code_interpreter" for tool in assistant.tools
                        # )
                        browser_status = any(
                            tool.type == "browser" for tool in assistant.tools
                        )
                        # new_code_interpreter_status = st.checkbox(
                        #     "Code Interpreter", value=code_interpreter_status
                        # )
                        new_code_interpreter_status = False
                        new_browser_status = st.checkbox(
                            "Browser", value=browser_status
                        )
                        
                        # Display current files
                        if assistant.file_ids:
                            has_retrieved_file = False
                            for file_id in assistant.file_ids:
                                try:
                                    retrieved_file = rubra_client.files.retrieve(file_id)
                                    if not has_retrieved_file:
                                        st.caption("Existing Files in Knowledge Retrieval")
                                        has_retrieved_file = True
                                    col1, col2 = st.columns([4, 1])
                                    with col1:
                                        st.text(retrieved_file.filename)
                                    with col2:
                                        # Use a checkbox to mark the file for deletion
                                        if st.checkbox(f"Delete", key=f"delete_file_{file_id}"):
                                            if file_id not in st.session_state['files_marked_for_deletion']:
                                                st.session_state['files_marked_for_deletion'].append(file_id)
                                        else:
                                            if file_id in st.session_state['files_marked_for_deletion']:
                                                st.session_state['files_marked_for_deletion'].remove(file_id)
                                except Exception as e:
                                    st.session_state['files_marked_for_deletion'].append(file_id)

                        # File uploader to add new files
                        st.caption("Upload New Files for Knowledge Retrieval")
                        new_uploaded_files = st.file_uploader(
                            "Upload New Files",
                            accept_multiple_files=True,
                            type=[".pdf", ".txt", ".md", ".log", ".rtf"],
                            help="Upload new files to attach to the assistant.",
                            key=f"new_files_{assistant.id}"
                        )

                        submit_modification = st.form_submit_button("Update Assistant")

                        if submit_modification:
                            # Process files marked for deletion
                            files_to_delete = st.session_state['files_marked_for_deletion']
                            # Clear the deletion list after processing
                            st.session_state['files_marked_for_deletion'] = []
                            # Proceed with modifying the assistant as before
                            modify_assistant(
                                assistant.id,
                                new_name,
                                new_instructions,
                                new_description,
                                new_code_interpreter_status,
                                new_browser_status,
                                assistant.file_ids,
                                new_uploaded_files=new_uploaded_files,
                                files_to_delete=files_to_delete,
                            )
                            st.session_state["modify_id"] = None  # Reset modification state


if __name__ == "__main__":
    st.set_page_config(page_title="Rubra Assistants", page_icon="🐿", layout="wide")
    remove_streamlit_elements()
    main()
