import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))) # Needed just because of python ide error not like recognizing scripts folder

import streamlit as st
from scripts.chatbot_variants.c_with_resume_chat.backend import chatbot
from langchain_core.messages import HumanMessage, AIMessageChunk


CONFIG = {'configurable': {'thread_id': 'thread-1'}}


#*******************************************************   Session Setup *****************************************************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the previous conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#********************************************************** Sidebar UI *************************************************************************

st.sidebar.title("LangGraph Chatbot")
st.sidebar.button("New Chat")
st.sidebar.header("Previous Chats")


#********************************************************** Main UI *************************************************************************
# Take user message
user_input = st.chat_input('Type here')

if user_input:

    # first add the user message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    # show user message on UI
    with st.chat_message('user'):
        st.text(user_input)


    with st.chat_message('assistant'):
        #show the AI message in a streaming way
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config={'configurable': {'thread_id': 'thread-1'}},
                stream_mode='messages'
            )
            if isinstance(message_chunk, AIMessageChunk)  # ✅ only new streaming chunks
        )
    # add the AI message to message_history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})