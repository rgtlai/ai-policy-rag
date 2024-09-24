from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain.schema.runnable import RunnablePassthrough

SYSTEM_PROMPT = """\
You are an expert in answering questions succintly and correctly only within context. If the last user response is a question use the context in "Context" to answer the question. If you are not able to answer the question based on the context reply with "I don't know" or if the question is not related to the current context answer "I don't know". If the last user response is not a question or query respond accordingly based on the current context if possible.
"""

CONTEXT_PROMPT = """\
Context:
{context}
"""

class RagChat:
    def __init__(self, llm: ChatOpenAI, retriever):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ('user', CONTEXT_PROMPT),
            MessagesPlaceholder(variable_name="messages")
        ])
        
        self.llm_chain_new = ({"context": itemgetter("question") | retriever, "question": itemgetter("question"), "messages":itemgetter("messages")}
                          | RunnablePassthrough.assign(context=itemgetter("context"))
                          | {"response": self.prompt | self.llm, "context": itemgetter("context")}
                         )
        self.llm_chain = self.prompt | self.llm 

    def __call__(self, state):
        user_input = state["messages"][-1]
        print('USER INPUT*******', user_input)
        if state["new_context"]:
            result = self.llm_chain_new.invoke({**state, "question":user_input.content})
            ai_message = result["response"]
            context = result["context"]
            print('****Adding new context:', context)
        else:
            print('Keeping current context')
            ai_message = self.llm_chain.invoke(state)
            context = state["context"]
       
        return {**state, "messages":[ai_message], "context":context}

    