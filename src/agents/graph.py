'''
To run python -m agents.graph in the main folder
'''
import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from .state import State
from .context_agent import ContextAgent
from .rag_agent import RagChat
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessageChunk
from ..vectorstore.get import retriever, retriever_ft

load_dotenv()
memory = MemorySaver()
app = None

llm = ChatOpenAI(temperature=0, model=os.environ["OPENAI_MODEL"], streaming=True)
graph = StateGraph(State)
_context_agent = ContextAgent(llm=llm)
_rag_agent = RagChat(llm=llm, retriever=retriever_ft)

graph.add_node('context_agent', _context_agent)
graph.add_node('chatrag_agent', _rag_agent)
graph.set_entry_point('context_agent')
graph.add_edge('context_agent', 'chatrag_agent')
graph.add_edge('chatrag_agent', END)


async def run():
    # async for event in app.astream_events({"messages":[("user", "What is Nist?")], "context":""},version="v2"):
        # print('EV', event)
    #first = True
    config = {"configurable": {"thread_id": "1"}}
    query = "What is NIST?"
    print("User:", query)
    state = app.get_state(config)
    print('STATE******', state.values)
    async for event in app.astream_events({"messages":[("user", query)], "context":""},config=config, version="v2"):
        if event['event'] == "on_chat_model_stream":
            data = event["data"]
            if data["chunk"].content:
                print(data["chunk"].content, end="|", flush=True)
    
    state = app.get_state(config)
    print('STATE 2******', state.values['context'])     
        

if __name__ == '__main__':
    app = graph.compile(checkpointer=memory)
    asyncio.run(run())
    
        

    
    






