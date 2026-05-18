import json
from textEditorTool import TextEditorTool
from helper import  add_user_message, add_assistant_message, chat, text_from_message, chat_stream, model
from tools import get_current_datetime, get_current_datetime_schema, add_duration_to_datetime, add_duration_to_datetime_schema, set_reminder, set_reminder_schema, save_article_schema


text_editor_tool = TextEditorTool()


def run_tool(tool_name, tool_input):
    if tool_name == "str_replace_editor":
        command = tool_input["command"]
        if command == "view":
            return text_editor_tool.view(
                tool_input["path"], tool_input.get("view_range")
            )
        elif command == "str_replace":
            return text_editor_tool.str_replace(
                tool_input["path"], tool_input["old_str"], tool_input["new_str"]
            )
        elif command == "create":
            return text_editor_tool.create(tool_input["path"], tool_input["file_text"])
        elif command == "insert":
            return text_editor_tool.insert(
                tool_input["path"],
                tool_input["insert_line"],
                tool_input["new_str"],
            )
        elif command == "undo_edit":
            return text_editor_tool.undo_edit(tool_input["path"])
        else:
            raise Exception(f"Unknown text editor command: {command}")
    else:
        raise Exception(f"Unknown tool name: {tool_name}")


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


# Make the text edit schema based on the model version being used
def get_text_edit_schema(model):
    return {
        "type": "text_editor_20250728",
        "name": "str_replace_based_edit_tool",
    }


# Run the conversation in a loop until the model doesn't ask for a tool use
def run_conversation(messages):
    while True:
        response = chat(
            messages,
            tools=[get_text_edit_schema(model)],
        )

        add_assistant_message(messages, response)
        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        add_user_message(messages, tool_results)

    return messages

messages = []

add_user_message(
    messages,
    """
        create phyton file ./pi.py with function to calculate pi to the 5th digits 
    """,
)

run_conversation(messages)