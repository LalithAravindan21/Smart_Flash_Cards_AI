import streamlit as st
import openai
import pandas as pd
import json
from docx import Document
from pptx import Presentation
import PyPDF2
from io import BytesIO

# Set your OpenAI API key
openai.api_key = "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"

def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()
    text = ""
    
    if file_type == "txt":
        text = uploaded_file.read().decode("utf-8")
    elif file_type == "pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_type == "docx":
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file_type == "pptx":
        presentation = Presentation(uploaded_file)
        text = "\n".join([shape.text for slide in presentation.slides for shape in slide.shapes if hasattr(shape, "text")])
    
    return text

def chat_with_document(user_input, document_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that answers questions based on the provided document."},
            {"role": "user", "content": f"Document Text: {document_text}\n\nUser Question: {user_input}"}
        ]
    )
    return response['choices'][0]['message']['content']

st.title("Smart Document Assistant")
st.write("Upload any document (PDF, Word, PPT, TXT) and chat with it.")

uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "docx", "pptx"]) 
document_text = ""

if uploaded_file:
    document_text = extract_text_from_file(uploaded_file)
    st.subheader("Document Preview")
    st.text_area("Extracted Text", document_text[:1000], height=200)
    
    st.subheader("Chat with Your Document")
    user_query = st.text_input("Ask a question about the document")
    if user_query:
        answer = chat_with_document(user_query, document_text)
        st.write("**Answer:**", answer)
