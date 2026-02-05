import streamlit as st
import requests

st.title("Financy: Automated Research Agent")

topic = st.sidebar.text_input("Enter news topic")
if st.sidebar.button("Research"):
    urls = requests.post(
        "http://search:8000/search",
        json={"query": topic}
    ).json()["urls"]

    requests.post(
        "http://ingestion:8001/ingest",
        json={"urls": urls}
    )

    st.success("Knowledge base ready!")

question = st.text_input("Ask a question")
if question:
    response = requests.post(
        "http://rag:8002/query",
        json={"question": question}
    ).json()

    st.write(response["answer"])
