import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from IPython.display import Markdown

# Load variables from .env
load_dotenv()

# Initialize Client
client = Anthropic()
model = "claude-sonnet-4-5"

system_prompt = """
act as sifi author
"""
temperature = 0.1

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
        "stop_sequences":["```"]
    }
    message = client.messages.create(**params)
    return message.content[0].text

# Start with an empty message list
messages = []

add_user_messages(messages, "generate 3 different sample AWS CLI commands. Each should be very short")
add_assistant_messages(messages, "```bash")
print(chat (messages))

# print("--- RAW GENERATED Markdown CODE ---")
# print(Markdown(raw_code).data)