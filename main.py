import os
import streamlit as st
import time
import requests
from bs4 import BeautifulSoup
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables (API keys, etc.)
load_dotenv()

# Constants
FAISS_INDEX_PATH = "faiss_index"

# Streamlit UI setup
st.set_page_config(page_title="SourceSense AI", page_icon="📈", layout="wide")
st.title("SourceSense AI Agent – Intelligent source-based Q&A")

# Sidebar UI for Dynamic URL Input
st.sidebar.title("🔗 Enter Article URLs")

# Initialize session state for URLs
if "urls" not in st.session_state:
    st.session_state.urls = [""]  # Start with one URL input field

# Function to add a new URL input field
def add_url():
    st.session_state.urls.append("")  # Add a new empty URL field

# Function to remove the last URL input field
def remove_url():
    if len(st.session_state.urls) > 1:  # Ensure at least one input remains
        st.session_state.urls.pop()

# Display URL input fields dynamically
for i in range(len(st.session_state.urls)):
    st.session_state.urls[i] = st.sidebar.text_input(f"URL {i+1}", st.session_state.urls[i])

# Buttons to dynamically add or remove URL fields
st.sidebar.button("➕ Add URL", on_click=add_url)
st.sidebar.button("➖ Remove Last URL", on_click=remove_url)

# Process URLs button
process_url_clicked = st.sidebar.button("🔄 Process URLs")


### 📌 **Function: Fetch & Extract Text from URLs**
def fetch_text_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        text = "\n".join([p.get_text() for p in paragraphs])

        return text if text else "No readable content found."
    except Exception as e:
        return f"Error fetching URL {url}: {e}"


### 📌 **Function: Process URLs & Build FAISS Index**
def process_urls(urls):
    urls = [url for url in urls if url.strip()]  # Remove empty URLs

    if not urls:  # If no URL is provided, show warning
        st.warning("⚠️ Please enter at least one valid URL before processing.")
        return

    with st.spinner("Fetching and processing URLs..."):
        documents = []
        for url in urls:
            text = fetch_text_from_url(url)
            if text and "Error" not in text:
                documents.append({"text": text, "source": url})

    if not documents:  # If no valid text is extracted
        st.error("⚠️ No valid text found in the provided URLs.")
        return

    with st.spinner("Splitting text into chunks..."):
        text_splitter = RecursiveCharacterTextSplitter(separators=['\n\n', '\n', '.', ','], chunk_size=1000)
        docs = []
        metadata = []

        for doc in documents:
            text_chunks = text_splitter.split_text(doc["text"])
            for chunk in text_chunks:
                docs.append(chunk)
                metadata.append({"source": doc["source"]})  # ✅ Add source metadata

    if docs:
        with st.spinner("Generating embeddings & building FAISS index..."):
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_texts(docs, embeddings, metadatas=metadata)  # ✅ Pass metadata
            vectorstore.save_local(FAISS_INDEX_PATH)

        st.success("✅ URLs processed! You can now ask questions.")
    else:
        st.error("No valid text found in the URLs provided.")


### 📌 **Function: Load FAISS Index**
def load_faiss_index():
    try:
        embeddings = OpenAIEmbeddings()
        return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        st.error(f"Error loading FAISS index: {e}")
        return None


### **📌 Execute Processing on Button Click**
if process_url_clicked:
    process_urls(st.session_state.urls)


### **📌 Q&A Section with Submit Button**
st.subheader("🧐 Ask a Question About the Articles")
query = st.text_input("Enter your question below:")
search_button = st.button("🔍 Submit Question")

if search_button:  # ✅ Start searching only when button is pressed
    if not query.strip():
        st.warning("⚠️ Please enter a question before submitting.")
    else:
        vectorstore = load_faiss_index()
        if vectorstore:
            with st.spinner("🔍 Searching for the best answer..."):
                retriever = vectorstore.as_retriever()
                chain = RetrievalQAWithSourcesChain.from_llm(llm=OpenAI(temperature=0.7, max_tokens=500), retriever=retriever)
                result = chain({"question": query}, return_only_outputs=True)

                # Display results
                st.header("📢 Answer:")
                st.write(result["answer"])

                # Display sources (if available)
                sources = result.get("sources", "")
                if sources:
                    st.subheader("📌 Sources:")
                    st.write("\n".join(sources.split("\n")))
        else:
            st.warning("⚠️ No FAISS index found. Please process some URLs first.")
