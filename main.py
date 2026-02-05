import os
import streamlit as st
import pickle
import re
from dotenv import load_dotenv

# 1. Setup & Environment
load_dotenv()
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQAWithSourcesChain

st.set_page_config(page_title="RockyBot", layout="wide")
st.title("Financy: Automated Research Agent")

# Shared configuration
file_path = "faiss_store_automated.pkl"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- SECTION 1: INGESTION (Sidebar or Top) ---
st.sidebar.header("Research Settings")
search_query = st.sidebar.text_input("Enter a news topic:")
process_btn = st.sidebar.button("Auto-Research & Ingest")

if process_btn and search_query:
    with st.status("🔍 Researching and Ingesting...", expanded=True) as status:
        st.write("Step 1: Searching for news...")
        search = DuckDuckGoSearchResults(max_results=5)
        raw_results = search.run(search_query)
        
        # Robust link extraction
        links = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', raw_results)
        final_links = [l for l in links if "duckduckgo" not in l][:2]
        
        if not final_links:
            status.update(label="❌ Search Failed", state="error")
        else:
            st.write(f"✅ Found: {final_links}")
            loader = UnstructuredURLLoader(urls=final_links)
            data = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.split_documents(data)
            
            vectorstore = FAISS.from_documents(docs, embeddings)
            with open(file_path, "wb") as f:
                pickle.dump(vectorstore, f)
            
            status.update(label="🚀 Ingestion Complete!", state="complete", expanded=False)
            st.success("Knowledge base ready!")

# --- SECTION 2: PERMANENT QUERY UI ---
# This section is OUTSIDE the button logic so it stays visible
st.divider()
st.subheader("Chat with your Research")

# Check if the file exists to show the query box
if os.path.exists(file_path):
    query = st.text_input("Ask a question about the news topic:", placeholder="e.g., What are the key takeaways?")
    
    if query:
        with st.spinner("Thinking..."):
            # Load and Re-bind
            with open(file_path, "rb") as f:
                vectorstore = pickle.load(f)
            vectorstore.embedding_function = embeddings
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.7
            )
            
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain.invoke({"question": query})
            
            st.markdown("### Answer")
            st.write(result.get("answer"))
            
            if result.get("sources"):
                with st.expander("View Sources"):
                    st.write(result["sources"])
else:
    st.info("👋 Welcome! Use the sidebar to research a topic first.")