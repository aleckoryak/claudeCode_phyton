import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

# 1. Load environment variables
load_dotenv()
client = Anthropic()

# 2. Define your prompt and the prefill string
user_prompt = "Generate a very short event bridge rule as json."
prefill_string = "```json"

# 3. Create the multi-turn message history
messages = [
    {
        "role": "user",
        "content": user_prompt
    },
    {
        "role": "assistant",
        "content": prefill_string
    }
]

# 4. Make the request with stop_sequences
# We tell Claude to stop generating immediately if it tries to close the markdown block
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=messages,
    stop_sequences=["```"]
)

# 5. Extract and clean the final text
raw_code = response.content[0].text

print("--- RAW GENERATED JSON  ---")
print(json.loads(raw_code.strip()))
