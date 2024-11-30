# Smart-Summarizer-Chat-Bot
The Smart-Summarizer-Chat-Bot is a web-based application that allows users to upload Word documents, generate concise summaries, and interact with a chatbot to ask questions about the document's content. It leverages document summarization techniques and uses Chroma as a vector database for embedding and similarity search.

# Features
Document Upload: Users can upload Word documents (.docx).
Summarization: Generate summaries using various methods:
TF-IDF: Traditional TF-IDF based summary.
Embedding: Summarize using embeddings generated from the document.
Abstractive Summarization: Advanced, abstractive summarization model.
Chatbot Integration: After summarization, users can ask questions about the document. The chatbot provides answers by retrieving relevant chunks of the document based on user queries.
Interactive Web Interface: Built using Streamlit, allowing an easy and engaging experience for users.

# Technologies Used
Streamlit: For creating an interactive web app.
Chroma: Used as the vector database for storing and retrieving document embeddings.
NLTK: Used for text processing tasks like tokenization, stemming, etc.
HuggingFace Embeddings: For embedding documents and queries into vector representations.
Abstractive Summarization Models: For generating human-like summaries of the document content.
Recursive Chunker: To split long documents into smaller chunks for more manageable processing.
Ollama: To interact with local downloaded Model
Groq API: You can also use Groq api for LLM
