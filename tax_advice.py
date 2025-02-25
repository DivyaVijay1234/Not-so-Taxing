import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

def summarize_text(text):
    summarizer = pipeline("summarization")
    try:
        # Summarize the text in chunks if it's too long
        max_chunk_size = 1000
        chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
        summaries = [summarizer(chunk, max_length=60, min_length=10, do_sample=False)[0]['summary_text'] for chunk in chunks]
        return summaries
    except Exception as e:
        return [f"Error in summarization: {str(e)}"]

def extract_text_from_url(url):
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
    if st.button("Summarize"):
        if url:
            with st.spinner("Extracting and summarizing the content..."):
                text = extract_text_from_url(url)
                if "Error" in text:
                    st.error(text)
                else:
                    summaries = summarize_text(text)
                    if any("Error" in summary for summary in summaries):
                        st.error(summaries[0])
                    else:
                        st.subheader("Summary of Do's and Don'ts")
                        for summary in summaries:
                            st.write(f"- {summary}")
        else:
            st.error("Please enter a valid URL.")

# Call the function to display the tax advice
show_tax_advice()