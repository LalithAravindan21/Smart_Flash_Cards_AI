import streamlit as st
import openai
import pandas as pd
import json
from docx import Document
from io import BytesIO

# Set your OpenAI API key
openai.api_key = "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"

def generate_flashcards(text):
    prompt = f"""
    Extract key concepts from the following text and convert them into flashcards.
    Format: JSON with 'question' and 'answer' fields.
    
    Text:
    {text}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant that creates educational flashcards."},
                  {"role": "user", "content": prompt}]
    )
    
    flashcards = json.loads(response['choices'][0]['message']['content'])
    return flashcards

def create_word_document(flashcards):
    doc = Document()
    doc.add_heading("Flashcards", level=1)
    
    for i, card in enumerate(flashcards):
        doc.add_heading(f"Flashcard {i+1}", level=2)
        doc.add_paragraph(f"Q: {card['question']}", style="List Bullet")
        doc.add_paragraph(f"A: {card['answer']}", style="List Bullet")
        doc.add_paragraph("\n")
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

st.title("Smart Flashcards AI")
st.write("Convert textbooks and notes into interactive flashcards for spaced repetition.")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"]) 
if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    flashcards = generate_flashcards(text)
    
    if flashcards:
        st.subheader("Preview Flashcards")
        for i, card in enumerate(flashcards):
            with st.expander(f"Flashcard {i+1}"):
                st.write(f"**Q:** {card['question']}")
                st.write(f"**A:** {card['answer']}")
        
        # Generate and provide Word document download
        word_doc = create_word_document(flashcards)
        st.download_button(
            label="Download Flashcards as Word Document",
            data=word_doc,
            file_name="flashcards.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
