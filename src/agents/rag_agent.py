from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain.schema.runnable import RunnablePassthrough

SYSTEM_PROMPT = """\
You are an expert in answering questions succintly and correctly only within context. If you are not able to answer the question based on the context reply with "I don't know". Never make up an answer.
"""

CONTEXT_PROMPT = """\
Context:
{context}

Question:
{question}
"""

def map_messages(messages):
    text=""
    for message in messages:
        if isinstance(message, HumanMessage):
            text += f"Human: {message.content}\n"
        elif isinstance(message, AIMessage):
            text += f"AI: {message.content}\n"
    return text

class RagAgent:
    def __init__(self, llm: ChatOpenAI, retriever):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ('user', CONTEXT_PROMPT)
        ])

        self.llm_chain = ({"context": itemgetter("question") | retriever, "question": itemgetter("question")}
                          | RunnablePassthrough.assign(context=itemgetter("context"))
                          | {"response": self.prompt | self.llm, "context": itemgetter("context")}
                          )

    def __call__(self, state):
        user_input = state["question"]
        print('USER INPUT*******', user_input)
        result = self.llm_chain.invoke(
            {"question": map_messages(state["messages"])+f'Human: {user_input}'})
        ai_message = result["response"]
        context = result["context"]
        return {**state, "new_context": True, "messages": [ai_message], "context": context}

    def get_chain(self):
        return self.llm_chain
    

