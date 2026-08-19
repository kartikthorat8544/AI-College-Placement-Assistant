import streamlit as st

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


st.set_page_config(
    page_title="AI Placement Assistant",
    page_icon="🤖"
)

initialize_database()

st.title("🤖 AI College and Placement Assistant")
st.write(
    "Ask placement questions or upload a PDF "
    "and ask questions about its contents."
)

if "messages" not in st.session_state:
    saved_messages = get_messages()

    if saved_messages:
        st.session_state.messages = saved_messages
    else:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! How can I help with your "
                    "placement preparation?"
                )
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
    clear_messages()

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! How can I help with your "
                "placement preparation?"
            )
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
    save_message("assistant", chatbot_response)