import streamlit as st
from scripts.chatbot_variants.b_with_streaming.backend import chatbot
from langchain_core.messages import HumanMessage, AIMessageChunk

CONFIG = {'configurable': {'thread_id': 'thread-1'}}


# Initialized array for message storage if first time running
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the previous conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


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