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
        "system" :system_prompt,
        "temperature" : temperature,
        "stream":True
    }
    stream = client.messages.create(**params)
    for event in stream:
        print(event)
    # return message.content[0].text
    return ''
# Start with an empty message list
messages = []
add_user_messages(messages, "write one sentence sifi story")

with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages
) as stream:
    for text in stream.text_stream:
        print (text, end="")

print("---------------------")
print (stream.get_final_message())
print("---------------------")
print (stream.get_final_text())
add_assistant_messages(messages, stream.get_final_text())

