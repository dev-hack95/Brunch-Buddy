import os
import langchain
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.cache import InMemoryCache
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, ChatPromptTemplate, PromptTemplate


# Config
load_dotenv(".env")
api_key = os.environ.get("key")

# Cache Config
langchain.llm_cache = InMemoryCache()
chat = ChatOpenAI(api_key=api_key, model='gpt-3.5-turbo', max_tokens=500)

st.header("🧇🥞🍳🥛 BrunchBuddy")

st.sidebar.header("Parameters")
slider_value = st.sidebar.slider("Time",  0, 120, 30)
selectbox_value = st.sidebar.selectbox("Type", ("Vegetarian", "Non-Vegetarian"))

system_message = "You are an AI recipe assistant that specialize in {brunch} dishes that can be prepared in {time}"
system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
human_template = "{recipe_request}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

prompt_input = st.text_input("What would you like to have for brunch:")
if prompt_input:
    prompt = chat_prompt.format_prompt(time=str(slider_value) + " min", recipe_request=str(prompt_input), brunch=selectbox_value).to_messages()
    st.write(chat(prompt).content)