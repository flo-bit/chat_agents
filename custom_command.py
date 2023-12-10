from chat_agent.handlers import TerminalBot
from chat_agent import ChatAgentConfig, default_commands

# command function always have to be async with two parameters: agent and message


async def hello(agent, message):
    return "Executing command!\nHello world!"

# command definition: name, function, description, regex (optional)
# if regex is not given, the command will be matched by name
# description is used for the help command
hello_command = {
    "name": "hello",
    "function": hello,
    "description": "- greets the world",
}


async def goodbye(agent, message):
    # we could also call any agent function here
    return "Executing command!\nGoodbye world! (your message was: " + message + ")"


# use regex to match the command
goodbye_command = {
    "name": "goodbye",
    "function": goodbye,
    "description": "<word> - says goodbye to the world",
    # will match a message with the format "bye <word>"
    "regex": "^bye \S*$"
}

config = ChatAgentConfig(
    commands=[hello_command, goodbye_command] + default_commands)
TerminalBot(config=config)
