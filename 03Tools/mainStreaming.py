import json

from helper import  add_user_message, add_assistant_message, chat, text_from_message, chat_stream
from tools import get_current_datetime, get_current_datetime_schema, add_duration_to_datetime, add_duration_to_datetime_schema, set_reminder, set_reminder_schema, save_article_schema



def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    elif tool_name == "add_duration_to_datetime":
        return add_duration_to_datetime(**tool_input)
    elif tool_name == "set_reminder":
        return set_reminder(**tool_input)


def run_tools(message):
    tool_requests = [block for block in message.content if block.type == "tool_use"]
    tool_result_blocks = []

    for tool_request in tool_requests:
        try:
            tool_output = run_tool(tool_request.name, tool_request.input)
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False,
            }
        except Exception as e:
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True,
            }

        tool_result_blocks.append(tool_result_block)

    return tool_result_blocks


def run_conversation(messages, tools=[], tool_choice=None, fine_grained=False):
    while True:
        with chat_stream(
                messages,
                tools=tools,
                betas=["fine-grained-tool-streaming-2025-05-14"] if fine_grained else [],
                tool_choice=tool_choice,
        ) as stream:
            for chunk in stream:
                if chunk.type == "text":
                    print(chunk.text, end="")

                if chunk.type == "content_block_start":
                    if chunk.content_block.type == "tool_use":
                        print(f'\n>>> Tool Call: "{chunk.content_block.name}"')

                if chunk.type == "input_json" and chunk.partial_json:
                    print(chunk.partial_json, end="")

                if chunk.type == "content_block_stop":
                    print("\n")

            response = stream.get_final_message()

        add_assistant_message(messages, response)

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        add_user_message(messages, tool_results)

        if tool_choice:
            break

    return messages



messages = []

add_user_message(
    messages,
    "Create and save a fake computer science article"
)

run_conversation(
    messages,
    tools=[save_article_schema],
    fine_grained=True,
    tool_choice={"type": "tool", "name": "save_article"},
)
result = run_conversation(messages)


print ("------------------")
print (result)