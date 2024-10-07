from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
#from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_openai import ChatOpenAI



SYSTEM_PROMPT = """\
You are a friendly assistant that helps users answer their questions or responds to their comments. Only answer questions or respond to the comments with the context and message history. Do not make up information. If the user initiates with a greeting return with a greeting including "How can I help you today?". Any queries by the user that cannot be answered by you must call the 'rag_tool' function.

Context:
{context}
"""

@tool
def rag_tool(**args):
    '''
    This function is used to call the RAG tool.
    '''
    return 'rag_tool'

class ChatAgent:
    def __init__(self, llm:ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages")
        ])
        
        schema_func = {
        "name": "chatbot_output",
        "description": "Determine if last user message requires a new context or not",
        "parameters": {
            "title": "Outpput",
            "type": "object",
            "properties": {
                "new_context": {
                    "title": "New context",
                    "type": "boolean"
                },
                "message": {
                    "title": "Message",
                    "description": "The response to the last user message",
                    "type": "string"
                }
            },
            "required": ["new_context", "message"],
        },
    }
        
        #self.llm_chain = self.prompt | self.llm.bind_functions(functions=[schema_func], #function_call="chatbot_output") | JsonOutputFunctionsParser()
        self.llm_chain = self.prompt | self.llm.bind_tools([rag_tool])
        
        
    def __call__(self, state):
        user_input = state["messages"][-1]
        response = self.llm_chain.invoke(state)
        #new_context = True if response.tool_calls else False
        if response.tool_calls:
          output = {**state, "question":user_input.content, "new_context": True}
        else:  
          output = {**state, "messages":[response], "new_context": False, "question": user_input.content}
       
        return output


    
    
       
        