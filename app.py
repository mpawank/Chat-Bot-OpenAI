import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env
load_dotenv()

# Fetch API key from environment variables
api_key = os.getenv("LANGCHAIN_API_KEY")

if not api_key:
    st.error("LANGCHAIN_API_KEY is not set. Please check your .env file or enter it manually in the sidebar.")

# Streamlit App Title
st.title("Enhanced Q&A Chatbot With OpenAI")

# Sidebar Settings
st.sidebar.title("Settings")

# Optional API key input for users who don't have a .env file
user_api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
api_key = user_api_key if user_api_key else api_key

# Model Selection
engine = st.sidebar.selectbox("Select OpenAI Model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])

# Response Configuration
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)

# Define Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user's queries."),
    ("user", "Question: {question}")
])

# Function to generate responses
def generate_response(question):
    """Generates a response from OpenAI based on user input."""
    if not api_key:
        return "Error: API Key is missing. Please enter it in the sidebar."

    try:
        llm = ChatOpenAI(model=engine, openai_api_key=api_key)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        answer = chain.invoke({'question': question})
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

# User Input Section
st.write("Go ahead and ask any question:")
user_input = st.text_input("You:")

# Button for Submission
if st.button("Submit"):
    if user_input:
        response = generate_response(user_input)
        st.write("Chatbot:", response)
    else:
        st.warning("Please enter a question.")
