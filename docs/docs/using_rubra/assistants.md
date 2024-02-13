---
id: rubra-frontend-assistants
title: Rubra Assistants
sidebar_label: Assistants
sidebar_position: 0
---

# Rubra Assistants

Rubra Assistants enables you to construct AI assistants tailored to your applications. Each Assistant is equipped with instructions and can utilize models, tools, and knowledge to answer user inquiries. Presently, the Assistants API supports two tool types: Retrieval and Web browsing. As we continue to evolve, we anticipate introducing more tools and allow you to integrate your own.

## Viewing Assistants

When you navigate to the Rubra Assistants page, you will see a list of all the assistants you have created. Each assistant is displayed with its name, model, and any additional tools enabled (like Code Interpreter or Browser). If an assistant has a description or instructions, these will also be displayed.

## Creating a New Assistant

To create a new assistant, click on the "Create New Assistant" button. This will open a form where you can enter the following details:

- **Name**: The name of your assistant.
- **Description**: A short description of your assistant.
- **Instructions**: Instructions on what the assistant does and how it should behave.
- **Model**: The AI model that your assistant will use. You can select from a list of configured models.

### Tools

You can also enable additional tools for your assistant:

- **Browser**: Enable this to allow your assistant search and open links.
- **Knowledge**: You can upload files here. If you do, conversations with your assistant may include file contents. Files can be downloaded when Code Interpreter is enabled. This feature uses automated Retrieval-Augmented Generation (RAG) to enhance the assistant's responses with information from the uploaded files.

Once you have filled in all the details, click on "Create Assistant" to create your assistant. You will be able to chat with this assistant in Rubra chat.

## Modifying an Assistant

To modify an assistant, click on the "Modify" button next to the assistant you want to modify. This will open a form where you can update the assistant's name, description, instructions, and tools.

Once you have made your changes, click on "Update Assistant" to save your changes.

## Deleting an Assistant

To delete an assistant, click on the "Delete" button next to the assistant you want to delete. You will see a success message once the assistant has been successfully deleted.
