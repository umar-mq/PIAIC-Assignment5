# ==================
# IMPORTS
# ==================
import os
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

# ==================
# INIT
# ==================
load_dotenv()

# Initialize the language model client
client = AsyncOpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client,
)

# Disable tracing
set_tracing_disabled(disabled=True)

# ==================
# TOOLS
# ==================
@function_tool
def search_internet(query: str, num_results: int = 5) -> str:
    """Search the internet using DuckDuckGo

    Args:
        query: A concise and specific query to search the internet
        num_results: The number of results to return (recommended: 1-5)
    """
    print(f"Calling tool 'search_internet' with query: '{query}'")
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=num_results)
        if not results:
            return "No results found."
        
        results_text = "\n--\n".join(
            [f"# {page['title']} [{page['href']}]\n{page['body']}" for page in results]
        )
        return results_text
    except Exception as e:
        print(f"An error occurred during search: {e}")
        return f"Error: Could not perform search due to {e}"

# ==================
# AGENT DEFINITION
# ==================
search_agent = Agent(
    name="SearchAgent",
    handoff_description="Agent for performing web searches and getting up to date information",
    instructions=(
        "You are an helpful assistant. Use the 'search_internet' tool to find "
        "relevant information on the web to answer user queries. Always provide accurate "
        "and concise responses based on the search results. Call the tool multiple times to "
        "gather sufficient information before answering."
    ),
    model=model,
    tools=[search_internet],
)

# ==================
# AGENT RUNNER
# ==================
async def get_agent_response(chat_history):
    output = await Runner.run(search_agent, chat_history)
    final_output = output.final_output if output.final_output else "Sorry, I couldn't process that request."
    updated_history = output.to_input_list()
    
    return final_output, updated_history