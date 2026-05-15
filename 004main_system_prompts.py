import os
import json
from pprint import pprint
from dotenv import load_dotenv
from anthropic import Anthropic

# Load variables from .env
load_dotenv()

# Initialize Client
client = Anthropic()
model = "claude-sonnet-4-5"

system_prompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""


def add_user_messages(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_messages(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages):
    params = {
        "model":model,
        "max_tokens":1000,
        "messages":messages,
        "system" :system_prompt
    }
    message = client.messages.create(**params)
    return message.content[0].text

# Start with an empty message list
messages = []

while True:
    user_input = input("> ")
    print (">", user_input)

    add_user_messages(messages, user_input)

    # Get Claude's response
    answer = chat(messages)

    print (">>>", answer)
    # Add Claude's response to the conversation history
    add_assistant_messages(messages, answer)








