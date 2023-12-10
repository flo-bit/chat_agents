import re


async def reset(agent, message):
    agent.reset()
    return "Agent reset"


async def info(agent, message):
    return agent.info()


async def history(agent, message):
    return str(agent)


async def clear_memory(agent, message):
    agent.clear_memory()
    return "Memory cleared"


async def clear_history(agent, message):
    agent.clear_history()
    return "History cleared"


async def read(agent, message):
    agent.add_memory_file(message.split("read ")[1])
    return f"Added file {message.split('read ')[1]} to memory"


async def debug(agent, message):
    agent.set_debug("on" in message)
    return f"Debug mode {'on' if agent.config.debug else 'off'}"


async def save(agent, message):
    # get file using regex
    file_name = re.match(r"save (\S*)", message)
    if file_name:
        file_name = file_name.group(1)
        agent.save_to_file(file_name)

        return f"Saved agent to file {file_name}"
    else:
        return "No file name given"

# shows the messages that will be sent with the next message


async def show_prompt_messages(agent, m):
    messages = agent.get_prompt_messages()
    string = "\n"
    for message in messages:
        string += f"\n\n> {message['role']}:\n{message['content']}"
    if len(messages) == 0:
        string += "No messages yet"
    string += "\n\n"
    return string


async def load(agent, message):
    # get file using regex
    file_name = re.match(r"load (\S*)", message)
    if file_name:
        file_name = file_name.group(1)
        agent.load_from_file(file_name)

        return f"Loaded agent from file {file_name}"
    else:
        return "No file name given"


async def help(agent, message):
    return agent.all_commands()


default_commands = [
    {
        "name": "reset",
        "function": reset,
        "description": "- resets the chat agent"
    },
    {
        "name": "info",
        "function": info,
        "description": "- prints info about the chat agent"
    },
    {
        "name": "history",
        "function": history,
        "description": "- prints the chat history"
    },
    {
        "name": "clear memory",
        "function": clear_memory,
        "description": "- clears the memory of the chat agent"
    },
    {
        "name": "clear history",
        "function": clear_history,
        "description": "- clears the history of the chat agent"
    },
    {
        "name": "read",
        "function": read,
        "description": "<file> - adds a file to the memory of the chat agent",
        "regex": "^read \S*$"
    },
    {
        "name": "save",
        "function": save,
        "description": "<file> - saves the chat agent to a file",
        "regex": "^save \S*$"
    },
    {
        "name": "load",
        "function": load,
        "description": "<file> - loads the chat agent from a file",
        "regex": "^load \S*$"
    },
    {
        "name": "debug",
        "function": debug,
        "description": "<on/off> - turns debug mode on or off",
        "regex": "^debug (on|off)$"
    },
    {
        "name": "help",
        "function": help,
        "description": "- prints all available commands"
    },
    {
        "name": "messages",
        "function": show_prompt_messages,
        "description": "- shows the messages that will be sent with the next message"
    }
]


class ChatAgentConfig:
    def __init__(self,
                 name: str = 'Chad',
                 description: str = '',
                 system_prompt: str = None,
                 model: str = "gpt-4-1106-preview",
                 history_max_messages: int = 10,
                 debug: bool = False,
                 answer_json: bool = False,
                 loop_function_call: bool = True,
                 reset_token_count: bool = False,
                 log_file: str = None,
                 chat_file: str = None,
                 commands: list = default_commands,
                 start_memory_files=None,
                 always_in_memory_files=None,
                 max_memory_files=3,
                 show_line_numbers=False,
                 check_for_commands=True,
                 save_file=None,
                 load_from_file=True,
                 save_to_file=True,
                 tools=None,
                 warning_token_count=100000):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.model = model
        self.history_max_messages = history_max_messages

        self.debug = debug
        self.answer_json = answer_json
        self.loop_function_call = loop_function_call
        self.reset_token_count = reset_token_count
        self.log_file = log_file
        self.chat_file = chat_file

        self.check_for_commands = check_for_commands
        self.commands = commands or []

        self.start_memory_files = start_memory_files or []
        self.always_in_memory_files = always_in_memory_files or []

        self.max_memory_files = max_memory_files
        self.show_line_numbers = show_line_numbers

        self.save_file = save_file
        self.load_from_file = load_from_file
        self.save_to_file = save_to_file
        self.tools = tools or []

        self.warning_token_count = warning_token_count
