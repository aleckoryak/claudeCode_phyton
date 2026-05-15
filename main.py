import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load variables from .env
load_dotenv()

# Initialize Client
client = Anthropic()
model = "claude-sonnet-4-5"

# Create Request
message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What is quantum computing? Answer in one sentence"
        }
    ]
)

# Output result
print(message)
# Output result text
print(message.content[0].text)