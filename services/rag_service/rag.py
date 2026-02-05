import os
import pickle
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.embeddings import HuggingFaceEmbeddings

FILE_PATH = "faiss_store.pkl"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def answer_query(query: str):
    with open(FILE_PATH, "rb") as f:
        vectorstore = pickle.load(f)

    vectorstore.embedding_function = embeddings

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )

    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )

    return chain.invoke({"question": query})
