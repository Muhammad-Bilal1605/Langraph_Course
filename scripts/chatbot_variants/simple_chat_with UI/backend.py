

from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver #Used for saving messages temprarily to the RAM
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END, START
from typing import Annotated, TypedDict


OLLAMA_MODEL = "qwen2.5-coder:14b"
OLLAMA_BASE_URL = "http://localhost:11434"
model = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
#%%
def chat(state:ChatState):
    messages=state['messages']
    response=model.invoke(messages).content
    return {'messages': [AIMessage(content=response)]}
#%%
checkpointer=MemorySaver() #used in saving the previous messages to RAM
graph= StateGraph(ChatState)

graph.add_node("chat",chat)

graph.add_edge(START,"chat")
graph.add_edge("chat",END)

chatbot=graph.compile(checkpointer=checkpointer) # checkpointer=checkpointer used in saving the previous messages to RAM