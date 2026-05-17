import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

# Load variables from .env
load_dotenv()

# Initialize Client
client = Anthropic()
model = "claude-sonnet-4-5"


def add_user_messages(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_messages(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages
    )
    return message.content[0].text

# Start with an empty message list
messages = []

# Add the initial user question
add_user_messages(messages, "Define quantum computing in one sentence")

# Get Claude's response
answer = chat(messages)

# Add Claude's response to the conversation history
add_assistant_messages(messages, answer)

# Add a follow-up question
add_user_messages(messages, "Write another sentence")

# Get the follow-up response with full context
final_answer = chat(messages)
add_assistant_messages(messages, final_answer)


print(json.dumps(messages, indent=4, ensure_ascii=False))



