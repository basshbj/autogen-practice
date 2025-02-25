import os
import asyncio
from dotenv import load_dotenv
from typing import Sequence
from azure.core.credentials import AzureKeyCredential
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage, ChatMessage
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core import CancellationToken

load_dotenv(dotenv_path='.env')

ENDPOINT = os.getenv('AOAI_ENDPOINT')
API_KEY = os.getenv('AOAI_API_KEY')
DEPLOYMENT = os.getenv('AOAI_DEPLOYMENT')
API_VERSION = os.getenv('AOAI_API_VERSION')


async def team_run(team: RoundRobinGroupChat, message: str) -> TaskResult:
  stream = team.run_stream(task=TextMessage(content=message, source="user"))
  await Console(stream)
  

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

  primary=agent = AssistantAgent(
    name="primary",
    model_client=az_model_client,
    system_message="You are a helpful AI assistant.",
  )

  critic_agent = AssistantAgent(
    name="critic",
    model_client=az_model_client,
    system_message="Provide constructive feedback. Response with 'APPROVE' to when your feedbacks are addressed.",
  )

  user_proxy = UserProxyAgent(
    name="user_proxy",
    input_func=input,
  )

  text_termination = TextMentionTermination("APPROVE")

  team = RoundRobinGroupChat(
    participants=[primary, user_proxy, critic_agent],
    termination_condition=text_termination
  )  

  message = "What is the secreat of the universe?"

  stream = team.run_stream(task=TextMessage(content=message, source="user"))
  asyncio.run(Console(stream))

  #asyncio.run(team_run(team, "What is the secreat of the universe?"))


