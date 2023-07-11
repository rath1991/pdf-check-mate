"""This is the main file that launches the chatbot."""
import os

import streamlit as st

from pdf_qa_main import ChatPDF


def initialize_model(model_type: str, api_key: str, pdf_path: str) -> ChatPDF:
    """Initialize the ChatPDF model instance.

    Args:
        model_type: Specifies the type of language model being used.
        api_key: API key required for accessing the language model.
        pdf_path: Path to the user-uploaded PDF file.
    Returns:
        Initialized ChatPDF model instance.
    """
    return ChatPDF(model_type, api_key, pdf_path)


def get_or_initialize_model(
    model_type: str, api_key: str, pdf_path: str
) -> ChatPDF:
    """Retrieve the initialized model instance from the Streamlit session.

    This method either fetches an existing model or initializes a new one.

    Args:
        model_type: Specifies the type of language model being used.
        api_key: API key required for accessing the language model.
        pdf_path: Path to the user-uploaded PDF file.

    Returns:
        Initialized ChatPDF model instance.
    """
    if "model" not in st.session_state:
        st.session_state["model"] = initialize_model(
            model_type, api_key, pdf_path
        )
    return st.session_state["model"]


def get_chat_response(bot, query: str) -> str:
    """Retrieve response from the ChatPDF model instance.

    Args:
        bot: Initialized ChatPDF model instance.
        query: User-provided query.
    Returns:
        Response dictionary.
    """
    if query:
        return bot.run_bot(query)
    return ""


def main() -> None:
    """Initialize and run the chatbot."""
    st.header("Upload PDF to see the magic")

    # Initialize session_state if it doesn't exist
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = ""
    if "query" not in st.session_state:
        st.session_state["query"] = ""
    if "query_history" not in st.session_state:
        st.session_state["query_history"] = []

    model_type = ""

    # Get user input based on the checkbox state
    paid_model_checkbox = st.checkbox("Paid Model")
    free_model_checkbox = st.checkbox("Free Model")

    if paid_model_checkbox:
        st.session_state["api_key"] = st.text_input(
            "Please enter your OpenAI API key", type="password"
        )
        model_type = "paid"
        if st.session_state["api_key"]:
            st.success("OPENAI API Key entered successfully!")
    elif free_model_checkbox:
        st.session_state["api_key"] = st.text_input(
            "Please enter your Huggingface API key", type="password"
        )
        model_type = "free"
        if st.session_state["api_key"]:
            st.success("Huggingface API Key entered successfully!")
    file = st.file_uploader("Upload your pdf", type="pdf")

    if file is not None:
        pdf_path = os.path.join(os.getcwd(), file.name)
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write((file).getbuffer())
        st.success("File Saved to local directory")

        # Initialize or retrieve the model instance
        bot = get_or_initialize_model(
            model_type, st.session_state["api_key"], pdf_path
        )

        # Display previous queries
        st.subheader("Previous Queries:")
        for prev_query in st.session_state.query_history:
            st.write(f"User: {prev_query['user']}")
            st.write(f"AI: {prev_query['ai']}")

        st.subheader("New Query:")
        new_query = st.text_area("Enter your query", value="", height=100)

        if st.button("Ask"):
            st.session_state.query_history.append(
                {"user": new_query, "ai": ""}
            )

            with st.spinner("AI is working..."):
                response = get_chat_response(bot, new_query)
                st.session_state.query_history[-1]["ai"] = response

            st.success("AI generated the response:")
            st.write(f"AI: {response}", icon="🤖")


if __name__ == "__main__":
    main()
