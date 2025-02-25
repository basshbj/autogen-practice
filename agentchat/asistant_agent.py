import os
import asyncio
from dotenv import load_dotenv
from typing import Sequence
from azure.core.credentials import AzureKeyCredential
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage, ChatMessage
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core.models import ModelFamily
from autogen_core import CancellationToken


load_dotenv(dotenv_path='.env')

ENDPOINT = os.getenv('AOAI_ENDPOINT')
API_KEY = os.getenv('AOAI_API_KEY')
DEPLOYMENT = os.getenv('AOAI_DEPLOYMENT')
API_VERSION = os.getenv('AOAI_API_VERSION')


# Tools
async def web_search(query: str):
  """Search the web for the given query."""
  return f"The answer is 42."

async def generate_random_string():
  """Generate a random string."""
  return "This is a random string generated with the power of the universe."


async def assistant_run(agent: AssistantAgent, message: str) -> None:
  messages = [
    TextMessage(content=message, source="user")
  ]
  
  response = agent.on_messages_stream(
    messages=messages,
    cancellation_token=CancellationToken()
  )

  await Console(response)

  

if __name__ == "__main__":
  # Set up agent
  azure_credential = AzureKeyCredential(API_KEY)

  az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=DEPLOYMENT,
    model=DEPLOYMENT,
    api_version="2024-10-21",
    azure_endpoint=ENDPOINT,
    api_key=API_KEY
  )

  agent = AssistantAgent(
    name="weather_agent",
    model_client=az_model_client,
    tools=[web_search, generate_random_string],
    system_message="You have the power of the universe. Act like a scy fi character.",
    reflect_on_tool_use=True
  )

  while True:
    user_prompt = input("USER>>> ")

    if user_prompt == "exit":
      break

    asyncio.run(assistant_run(agent, user_prompt))


