import streamlit as st
from io import BytesIO
from docx import Document
import nltk
from summarizer_code import TextSummarizer, AbstractiveSummarizer
from chatbot import Chatbot

# Download required NLTK data
@st.cache_resource  # This will cache the downloads
def download_nltk_data():
    try:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('stopwords')
        return True
    except Exception as e:
        return str(e)

def display_summary_page():
    st.title("Smart Summarizer")
    st.subheader("Upload a Word Document and select the summarization method.")

    # File uploader
    uploaded_file = st.file_uploader("Upload a Word document", type=["docx"])
    
    if uploaded_file:
        try:
            # Read the Word document
            document = Document(uploaded_file)
            text = "\n".join([para.text for para in document.paragraphs if para.text.strip()])
            
            if not text.strip():
                st.error("The uploaded document is empty. Please upload a valid document.")
                return

            # Display document preview
            st.subheader("Uploaded Document Preview:")
            st.text_area("Text from the document", text, height=200)

            # Store document text in session state for use in the chatbot
            st.session_state.document_text = text

            # Summarization options
            st.subheader("Summarization Options:")
            method = st.selectbox("Select summarization method:", ["TF-IDF", "Embedding", "Abstractive"])
            

            # Summarize Button
            if st.button("Generate Summary"):
                with st.spinner("Generating summary..."):
                    st.subheader("Summary:")                    
                    try:
                        if method == "TF-IDF":
                            summarizer = TextSummarizer(method='tfidf')
                            summary = summarizer.summarize(text,0.3)
                        
                        elif method == "Embedding":
                            summarizer = TextSummarizer(method='embedding')
                            summary = summarizer.summarize(text, 0.3)
                        
                        elif method == "Abstractive":
                            summarizer = AbstractiveSummarizer()
                            summary = summarizer.summarize(text)
                        
                        # Display the summary
                        if summary:
                            st.write(summary)
                        else:
                            st.warning("Could not generate a summary. Please try with different parameters.")
                    
                    except Exception as e:
                        st.error(f"Error during summarization: {str(e)}")
        except Exception as e:
            st.error(f"Error processing the document: {str(e)}")

def display_chatbot_page():
    st.title("Chatbot Interaction")

    # Initialize chatbot and session state for conversation history
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Display Document Preview in Chatbot Page
    if "document_text" in st.session_state:
        st.subheader("Document Preview:")
        st.text_area("Text from the document", st.session_state.document_text, height=200, disabled=True)

    # Initialize the chatbot
    chatbot = Chatbot()

    # Process the document (if any) into the chatbot
    if "document_text" in st.session_state:
        chatbot.process_document(st.session_state.document_text)

    # User input for querying the chatbot
    user_query = st.text_input("Ask a question about the document:")

    if user_query:
        with st.spinner("Generating response..."):
            # Get response from the chatbot
            response = chatbot.query(user_query)
            
            # Append the question and answer to the conversation history
            st.session_state.conversation_history.append({"question": user_query, "answer": response})

    # Display the chat history with colors and styling
    if st.session_state.conversation_history:
        st.subheader("Conversation History")
        for chat in st.session_state.conversation_history:
            st.markdown(
    f"""
    <div style="margin-bottom: 1em; padding: 1em; border-radius: 10px; background-color: #f0f8ff; border: 1px solid #87cefa;">
        <p style="margin: 0; font-size: 16px; color: #007acc; font-weight: bold;"><strong>User:</strong></p>
        <p style="margin: 0; font-size: 15px; color: #003d99;">{chat['question']}</p>
    </div>
    <div style="margin-bottom: 1em; padding: 1em; border-radius: 10px; background-color: #f9fff0; border: 1px solid #98fb98;">
        <p style="margin: 0; font-size: 16px; color: #228b22; font-weight: bold;"><strong>Answer:</strong></p>
        <p style="margin: 0; font-size: 15px; color: #1a531b;">{chat['answer']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def main():
    # First, ensure NLTK data is downloaded
    nltk_status = download_nltk_data()
    if nltk_status is not True:
        st.error(f"Failed to download NLTK data: {nltk_status}")
        return

    # Navigation
    page = st.sidebar.selectbox("Select a page", ["Summarizer", "Chatbot"])

    # Display selected page
    if page == "Summarizer":
        display_summary_page()
    elif page == "Chatbot":
        display_chatbot_page()

if __name__ == "__main__":
    main()
