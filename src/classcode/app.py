# ==================
# IMPORTS
# ==================
import chainlit as cl
from agent.agent import get_agent_response # <-- Import the agent runner

# ==================
# FRONTEND
# ==================
@cl.on_chat_start
async def on_start():
    cl.user_session.set("chat_history", [])
    await cl.Message(content="Hello! I am your research assistant. How can I help you today?").send()

@cl.on_message
async def on_msg(message: cl.Message):
    chat_history = cl.user_session.get("chat_history", [])
    chat_history.append({"role": "user", "content": message.content})
    final_output, updated_history = await get_agent_response(chat_history)
    await cl.Message(content=final_output).send()
    cl.user_session.set("chat_history", updated_history)
