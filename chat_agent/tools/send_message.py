from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chat_agent import ChatAgent


async def send_message(agent, other_agent: "ChatAgent", message: str, role: str = "user"):
    return f"Sent message to {other_agent.config.name}\nAnswer: " + await other_agent.send_message(message, role)


def create_send_message_tool(chat_agent: "ChatAgent"):
    description = f"Sends a message to another chat agent named {chat_agent.config.name}\nchat agent description: {chat_agent.config.description}"

    return {
        "info": {
            "type": "function",
            "function": {
                "name": "send_message",
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message to send"
                        },
                        "role": {
                            "type": "string",
                            "description": "Role of the message",
                            "default": "user"
                        }
                    },
                    "required": ["message"],
                },
            }
        },
        "function": send_message,
        "arguments": {
            "other_agent": chat_agent
        }
    }
