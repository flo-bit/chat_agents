from chat_agent.handlers import TerminalBot
from chat_agent import ChatAgentConfig


async def fibonacci(agent, n):
    if n < 0:
        raise ValueError("Negative arguments not implemented")
    if n <= 1:
        return n
    else:
        return await fibonacci(agent, n-1) + await fibonacci(agent, n-2)

tool_fibonacci = {
    "info": {
        "type": "function",
        "function": {
            "name": "fibonacci",
            "description": "Calculates the n-th fibonacci number",
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {
                        "type": "number",
                        "description": "n-th fibonacci number to calculate"
                    }
                },
                "required": ["n"],
            },
        }
    },
    "function": fibonacci,
}

config = ChatAgentConfig(tools=[tool_fibonacci])
TerminalBot(config=config)
