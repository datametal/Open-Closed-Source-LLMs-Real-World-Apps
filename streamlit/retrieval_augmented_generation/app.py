# Import necessary libraries
import openai  # Library for OpenAI API
import requests  # Library for making HTTP requests
import streamlit as st  # Library for creating web apps
from bs4 import BeautifulSoup  # Library for parsing HTML and XML documents

# Set the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai_key"]


# Define function to communicate with OpenAI's GPT model
def qa_gpt(question, context, system_prompt=None):
    # Initialize conversation prompts with user's question and context
    prompts = [{'role': 'user', 'content': f"Answer given the following context: {context}\n\nQuestion: {question}"}]

    # If there's a system prompt, add it to the beginning of conversation
    if system_prompt is not None:
        prompts = [{'role': 'system', 'content': system_prompt}] + prompts

    # Send conversation prompts to GPT model and get response
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=prompts
    )

    # Extract response content and return as a dictionary
    return {'response_text': chat_completion.choices[0].message.content}


# Set title for the Streamlit app
st.title('Document Question Answering System')

# Create a text input field for users to enter a URL
url = st.text_area(
    label="URL to scrape for context",
    value="https://www.sinanozdemir.ai"
)

# Create a text input field for users to enter their question
query = st.text_input("Query")

# Create a text input field for users to enter system prompt
system_prompt = st.text_input("System Prompt")

# Process query if there is one
if len(query) > 0:
    # Make a HTTP request to the provided URL and parse the HTML content
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    # Extract text from the parsed HTML document
    text = soup.get_text()

    # Call the GPT model function with the extracted text and user's question
    answer = qa_gpt(query, text, system_prompt=system_prompt)

    # Display the model's response on the web app
    st.write(answer["response_text"])
