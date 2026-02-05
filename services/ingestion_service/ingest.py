import pickle
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

FILE_PATH = "faiss_store.pkl"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_urls(urls):
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = splitter.split_documents(data)

    vectorstore = FAISS.from_documents(docs, embeddings)

    with open(FILE_PATH, "wb") as f:
        pickle.dump(vectorstore, f)

    return {"status": "ingestion_complete"}
