from langgraph.checkpoint.memory import MemorySaver
from src.agents.graph import graph
import uuid

# Chainlit
import chainlit as cl

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

def generate_unique_id():
    return str(uuid.uuid4())

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("app", app)
    user_id = generate_unique_id()
    print('Generated user id', user_id)
    cl.user_session.set('user_id', user_id)

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="AI Assistant",
            markdown_description="Your main assistant",
        )
    ]
    
@cl.on_message
async def main(message):
    _app = cl.user_session.get("app")
    user_id = cl.user_session.get('user_id')

    msg = cl.Message(content="")
    config = {"configurable": {"thread_id": user_id}}
    state = _app.get_state(config)
    astream = _app.astream_events({"messages": [message.content], "context": state.values.get(
        "context", "")}, config=config,  version="v2")

    async for event in astream:
        if event['event'] == "on_chat_model_stream":
            data = event["data"]
            if data["chunk"].content:
                await msg.stream_token(data["chunk"].content)

    await msg.update()
     
    # Add a button for showing logs
    state = _app.get_state(config)
    context = state.values.get("context")
    new_context = state.values.get("new_context")
    new_context = f"Updated Context: {new_context}"
    actions = [
        cl.Action(name="Show Context", value=new_context+'\n'+str(context), description="Click to view context")
    ]
    
    await cl.Message(
        content="Click the button to see context",
        actions=actions
    ).send()
    
# Function to show logs or metadata
async def show_context(data):
    await cl.Message(content=data).send()
    
# Event handler for the button action
@cl.action_callback("Show Context")
async def handle_show_context(action):
    log_data = action.value
    await show_context(log_data)
