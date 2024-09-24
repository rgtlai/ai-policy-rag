from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

class State(TypedDict):
    messages: Annotated[list, add_messages]
    question: str #current user input. It may or may not be a 'question'
    context: str
    new_context: bool #True means it must do a retrieval

