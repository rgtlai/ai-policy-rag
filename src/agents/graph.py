'''
To run python -m agents.graph in the main folder
'''
import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, END
from .state import State
from .chat_agent import ChatAgent
from .rag_agent import RagAgent
from langgraph.checkpoint.memory import MemorySaver
# from langchain_core.messages import HumanMessage, AIMessageChunk
from ..vectorstore.get import retriever_ft

load_dotenv()
memory = MemorySaver()
app = None

llm = ChatOpenAI(
    temperature=0, model=os.environ["OPENAI_MODEL"], streaming=True)
graph = StateGraph(State)
chat_agent = ChatAgent(llm=llm)
rag_agent = RagAgent(llm=llm, retriever=retriever_ft)


def route(state):
    if state["new_context"]:
        return 'rag_agent'
    else:
        return END


graph.add_node('chat_agent', chat_agent)
graph.add_node('rag_agent', rag_agent)
graph.set_entry_point('chat_agent')
# graph.add_edge('context_agent', 'chatrag_agent')
graph.add_conditional_edges(
    'chat_agent',
    route,
    {END: END, 'rag_agent': 'rag_agent'}
)
graph.add_edge('rag_agent', END)


async def run():
    # async for event in app.astream_events({"messages":[("user", "What is Nist?")], "context":""},version="v2"):
    # print('EV', event)
    # first = True
    config = {"configurable": {"thread_id": "1"}}
    query = "What is NIST?"
    print("User:", query)
    state = app.get_state(config)
    print('STATE******', state.values)
    async for event in app.astream_events({"messages": [("user", query)], "context": ""}, config=config, version="v2"):
        if event['event'] == "on_chat_model_stream":
            data = event["data"]
            if data["chunk"].content:
                print(data["chunk"].content, end="|", flush=True)

    state = app.get_state(config)
    print('STATE 2******', state.values['context'])


if __name__ == '__main__':
    app = graph.compile(checkpointer=memory)
    asyncio.run(run())
