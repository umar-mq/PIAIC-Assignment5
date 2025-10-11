# ==================
# IMPORTS
# ==================

import os
import chainlit as cl
from rich import print 
from agents import (
    Agent,
    Runner,
    function_tool,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)
from dotenv import load_dotenv
from ddgs import DDGS
from typing import cast


# ==================
# INIT
# ==================

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

set_tracing_disabled(disabled=True)


# ==================
# TOOLS 
# ==================

@function_tool
def search_internet(query: str, num_results: int = 5) -> str:
    """Search the internet using DuckDuckGo

    Args:
        query: A consise and specific query to search the internet
        num_results: The number of results to return (recommended: 1-5)
    """
    print("Calling tool 'search_internet' with parameters query = " + query + " | num_results = " + str(num_results))
    ddgs = DDGS()
    results = ddgs.text(query, max_results = num_results)
    
    print("results: ", results)

    results_text = "\n--\n".join([f"# {page['title']} [{page['href']}]\n{page['body']}" for page in results])
    print(results_text)
    return results_text


# ==================
# AGENTS
# ==================


agent = Agent(
    name = "SearchAgent",
    instructions = "You are an advanced geopolitical and socioeconomic research assistant. You use the tools provided to you to provide accurate and up-to-date information. You are persistent in your research, and do not respond until you have a complete and accurate answer. You use the search tool multiple times to narrow down and complete your information.\n\n The current date is 5th October 2025 in Pakistan",
    model=model,
    tools=[search_internet]
)

# ==================
# FRONTEND
# ==================

@cl.on_chat_start
async def on_start():
    # Chat history
    cl.user_session.set("chat_history", [])

@cl.on_message
async def on_msg(message: cl.Message):
    agent: Agent = cl.user_session.get("agent")
    chat_history: list[dict] = cl.user_session.get("chat_history", [])

    chat_history.append({"role": "user", "content": message.content})
    
    output = await Runner.run(agent, chat_history)
    msg = cl.Message(content=output.final_output)
    await msg.send()

    cl.user_session.set("chat_history", output.to_input_list())
