import os

import streamlit as st
from dotenv import load_dotenv

from chatbot.ai_service import generate_document_response
from chatbot.chatbot import get_response
from database.database import (
    clear_messages,
    get_messages,
    initialize_database,
    save_message
)
from rag.document_processor import process_pdf
from rag.retriever import retrieve_relevant_chunks


load_dotenv(override=True)

WELCOME_MESSAGE = (
    "Hello! How can I help with your placement preparation?"
)


def get_config_value(name, default=None):
    environment_value = os.getenv(name)

    if environment_value is not None:
        return environment_value

    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


persistent_history_enabled = str(
    get_config_value("PERSIST_CHAT_HISTORY", "false")
).strip().lower() == "true"


st.set_page_config(
    page_title="AI Placement Assistant",
    page_icon="🤖"
)

if persistent_history_enabled:
    initialize_database()

st.title("🤖 AI College and Placement Assistant")
st.write(
    "Ask placement questions or upload a PDF "
    "and ask questions about its contents."
)

if "messages" not in st.session_state:
    if persistent_history_enabled:
        saved_messages = get_messages()
    else:
        saved_messages = []

    if saved_messages:
        st.session_state.messages = saved_messages
    else:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE
            }
        ]

if "document_chunks" not in st.session_state:
    st.session_state.document_chunks = []

if "document_signature" not in st.session_state:
    st.session_state.document_signature = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None


with st.sidebar:
    st.header("Document Question Answering")

    if persistent_history_enabled:
        st.caption("Conversation history: saved locally")
    else:
        st.caption(
            "Conversation history: private to this browser session"
        )

    uploaded_pdf = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if uploaded_pdf is not None:
        current_signature = (
            uploaded_pdf.name,
            uploaded_pdf.size
        )

        if current_signature != st.session_state.document_signature:
            try:
                with st.spinner("Processing PDF..."):
                    document_data = process_pdf(uploaded_pdf)

                st.session_state.document_chunks = (
                    document_data["chunks"]
                )
                st.session_state.document_signature = (
                    current_signature
                )
                st.session_state.document_name = uploaded_pdf.name

            except Exception as error:
                st.session_state.document_chunks = []
                st.session_state.document_signature = None
                st.session_state.document_name = None

                st.error(f"Could not process the PDF: {error}")

        if st.session_state.document_chunks:
            st.success(
                f"Ready: {st.session_state.document_name}"
            )
            st.write(
                "Text chunks:",
                len(st.session_state.document_chunks)
            )

    else:
        st.session_state.document_chunks = []
        st.session_state.document_signature = None
        st.session_state.document_name = None

    if st.session_state.document_chunks:
        st.info(
            "Document mode is active. Questions will be "
            "answered using the uploaded PDF."
        )


if st.button("Clear conversation"):
    if persistent_history_enabled:
        clear_messages()

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }
    ]

    st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_message = st.chat_input("Enter your message")

if user_message:
    user_data = {
        "role": "user",
        "content": user_message
    }

    st.session_state.messages.append(user_data)

    if persistent_history_enabled:
        save_message("user", user_message)

    with st.chat_message("user"):
        st.write(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if st.session_state.document_chunks:
                relevant_chunks = retrieve_relevant_chunks(
                    user_message,
                    st.session_state.document_chunks
                )

                chatbot_response = generate_document_response(
                    user_message,
                    relevant_chunks
                )
            else:
                chatbot_response = get_response(user_message)

        st.write(chatbot_response)

    assistant_data = {
        "role": "assistant",
        "content": chatbot_response
    }

    st.session_state.messages.append(assistant_data)

    if persistent_history_enabled:
        save_message("assistant", chatbot_response)