import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Load a faster summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=200, min_length=80):
    """Summarize text using a Transformers model with better coverage."""
    try:
        max_chunk_size = 1500  # Increase chunk size to preserve context
        chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
        
        # First pass: Summarize each chunk
        summaries = [summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text'] for chunk in chunks]
        
        # Second pass: Summarize the combined summaries to get a final concise summary
        final_summary = summarizer(" ".join(summaries), max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        
        return final_summary
    except Exception as e:
        return f"Error in summarization: {str(e)}"

def extract_text_from_url(url):
    """Extract text content from a given URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        return text
    except Exception as e:
        return f"Error in extracting text: {str(e)}"

def show_tax_advice():
    st.title("Tax Advice Summarization")

    st.markdown("""
    ### Provide Links to Financial Advisors
    Enter the URLs of your favorite financial advisors' articles to get a summarized list of do's and don'ts for reducing taxes.
    """)

    url = st.text_input("Enter URL of the article:")
    
    st.markdown("""
    <style>
        div.stButton > button {
            visibility: visible !important;
            opacity: 1 !important;
            color: white !important;
            background-color: #4CAF50 !important;
            font-size: 16px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    if st.button("Summarize"):
        if url:
            with st.spinner("Extracting and summarizing the content... This may take a few minutes. Please wait patiently."):
                text = extract_text_from_url(url)
                if "Error" in text:
                    st.error(text)
                else:
                    final_summary = summarize_text(text)
                    st.subheader("Comprehensive Summary of Do's and Don'ts")
                    st.write(final_summary)
        else:
            st.error("Please enter a valid URL.")

# Call the function to display the tax advice
show_tax_advice()
