import streamlit as st
import groq
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

os.environ['LANGCHAIN_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGSMITH_PROJECT']=os.getenv("LANGSMITH_PROJECT")
os.environ['LANGSMITH_API_KEY']=os.getenv("LANGSMITH_API_KEY")
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to user query"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,llm,api_key,temperature, maxtokens):
    groq.api_key=api_key
    llm=ChatGroq(model=llm)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

st.title("Q & A ChatBot")

st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter Your Groq API Key", type="password")
llm=st.sidebar.selectbox("Select groq models",["llama-3.1-8b-instant","qwen/qwen3-32b"])
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
maxtokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

st.write("Go a head and ask any question")
user_input=st.text_input("You:")
if user_input:
    response=generate_response(user_input,llm,api_key, temperature,maxtokens)
    st.write(response)
else:
    st.write("Please provide a query")