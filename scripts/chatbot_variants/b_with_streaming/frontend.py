import streamlit as st
from scripts.chatbot_variants.b_with_streaming.backend import chatbot
from langchain_core.messages import HumanMessage, AIMessageChunk
# wo he wala hum nh config file set ki ha as we do for configuration for persistent memory and sth aik thread id attach kr di ha
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# st.session_data aik streamlit k andr library ha jo basically hamain allow krti ha k data aik session ka hum save kr skein
#what we are doing here is k like ab ap aik message bhejogy phr dusra message and so on tu hr baar apki ye wali script shuru sh chlti ha
#and session data store krnay ka b faida na hota as initialize shuru mai kr rhy thy message history ko tu wo empty ho jati
#,,,jis ki wjh sh ap ka pichlay walay messages khtm ho jatay tu hum kia karaingy k k agr chat_messages mai koi message nhi tu hum
#us session k liye aik dict bna laingy ,, is trh srf pehl dfa apki messages wali array initialize hogi, allowing you to keep previous msgs

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