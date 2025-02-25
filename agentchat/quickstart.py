import os
import asyncio
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core.models import ModelFamily

load_dotenv(dotenv_path='.env')

ENDPOINT = os.getenv('AOAI_ENDPOINT')
API_KEY = os.getenv('AOAI_API_KEY')
DEPLOYMENT = os.getenv('AOAI_DEPLOYMENT')
API_VERSION = os.getenv('AOAI_API_VERSION')

# Tool
async def get_weather(city: str):
  """Get the weather for a given city."""
  return f"Today's weather in {city} is 25 degrees Celsius."


async def main() -> None:
  azure_credential = AzureKeyCredential(API_KEY)

  az_model_client = AzureOpenAIChatCompletionClient(
      azure_deployment=DEPLOYMENT,
      model=DEPLOYMENT,
      api_version="2024-10-21",
      azure_endpoint=ENDPOINT,
      api_key=API_KEY
  )

  # model_client = AzureAIChatCompletionClient(
  #   endpoint=ENDPOINT,
  #   credential=azure_credential,
  #   model_info={
  #     "family": ModelFamily.GPT_4O,
  #     "function_calling": True,
  #     "json_output": True,
  #     "vision": True
  #   },
  #   model="DEPLOYMENT"
  # )


  agent = AssistantAgent(
    name="weather_agent",
    model_client=az_model_client,
    tools=[get_weather],
    system_message="You are a helpful assistant that provides help to the user.",
    reflect_on_tool_use=True
  )

  await Console(agent.run_stream(task="What is the weather in New York?"))

if __name__ == "__main__":
  asyncio.run(main())