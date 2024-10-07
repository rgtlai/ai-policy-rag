'''
Tests are invalid. Need to be refactored.
This tests the context agent. If the last user input is a question not related then it should return new_context as True. If the last user input is not a question or if it is a question that can be answered by the current context then new_context is False.
'''

import unittest
import sys
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
current_dir = os.path.dirname(os.path.abspath(__file__))
sys_dir = os.path.abspath(os.path.join(current_dir, '../..'))
# Get the parent directory
sys.path.append(sys_dir)
from src.agents.chat_agent import ChatAgent
from src.agents.state import State

load_dotenv()
model = os.environ["OPENAI_MODEL"]
with open('./data.json', 'r') as f:
    DATA = json.loads(f.read())
    
contexts = [data["context"] for data in DATA]
questions = [data["question"] for data in DATA]
outcontexts = [data["outcontext"] for data in DATA]
llm = ChatOpenAI(temperature=0, model=model)

class TestContextAgent(unittest.TestCase):
    def test_request_no_new_context(self):
        graph = StateGraph(State)
        agent = ContextAgent(llm=llm)
        graph.add_node('agent', agent)
        graph.set_entry_point('agent')
        graph.add_edge('agent', END)
        wf = graph.compile()
        for i, q in enumerate(questions):
            output = wf.invoke({"messages":[("user", q)], "context":contexts[i]})
            self.assertEqual(output['new_context'], False)
        
    def test_should_request_context(self):
        graph = StateGraph(State)
        agent = ChatAgent(llm=llm)
        graph.add_node('agent', agent)
        graph.set_entry_point('agent')
        graph.add_edge('agent', END)
        wf = graph.compile()
        for i, q in enumerate(questions):
            output = wf.invoke({"messages":[("user", q)], "context":outcontexts[i]})
            self.assertEqual(output['new_context'], True)
            
    def test_should_not_request_for_non_query(self):
        graph = StateGraph(State)
        agent = ChatAgent(llm=llm)
        graph.add_node('agent', agent)
        graph.set_entry_point('agent')
        graph.add_edge('agent', END)
        wf = graph.compile()
        for c in contexts:
            output = wf.invoke({"messages":[("user", "That is nice." )], "context":c})
            self.assertEqual(output['new_context'], False)
    
if __name__ == '__main__':
    unittest.main()