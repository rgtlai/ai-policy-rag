from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_openai import ChatOpenAI

#This agent checks if the current user message is a new query or not. If yes then retrieve a new context
SYSTEM_PROMPT = """\
You are to look over context to determine if the last user input is a query that can be answered from the context information below. If it is a query and it can be answered based on only the current context then return new_context as false. If the user input is not a query nor a question return new_context as false. Otherwise return new_context as true as a new context is required to answer the question.

Context:
{context}

User Input:
{question}
"""
class ContextAgent:
    def __init__(self, llm:ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
        
        schema_func = {
        "name": "new_context_call",
        "description": "Determine if last user message requires a new context or not",
        "parameters": {
            "title": "New Context",
            "type": "object",
            "properties": {
                "new_context": {
                    "title": "New context",
                    "type": "boolean"
                },
            },
            "required": ["new_context"],
        },
    }
        
        self.llm_chain = self.prompt | self.llm.bind_functions(functions=[schema_func], function_call="new_context_call") | JsonOutputFunctionsParser()
        
    def __call__(self, state):
        if not state.get("context"):
            print('NO CONTEXT!!!!')
            return {**state, "new_context": True}
        user_input = state["messages"][-1]
        output = self.llm_chain.invoke({**state, "question":user_input.content})
        new_context = output.get("new_context", True)
        return {**state, "new_context": new_context}
        
       
        