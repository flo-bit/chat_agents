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


async def log_level(agent, message):
    new_level = message.split("log ")[1]
    agent.config.logging_level = new_level
    return f"Logging level set to {new_level}"


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
        "name": "log",
        "function": log_level,
        "description": "<debug/info/warning/error> - sets the logging level of the chat agent",
        "regex": "^log (debug|info|warning|error)$"
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
                 answer_json: bool = False,

                 history_max_messages: int = 40,

                 logging_level: str = "info",

                 log_file: str = None,
                 chat_file: str = None,

                 show_line_numbers: bool = False,
                 max_memory_files: int = 3,
                 start_memory_files: list = None,
                 always_in_memory_files: list = None,
                 always_in_memory_folders: list = None,

                 save_file: bool = None,
                 load_from_file: bool = True,
                 save_to_file: bool = True,

                 commands: list = default_commands,
                 check_for_commands: bool = True,
                 reset_token_count: bool = False,

                 tools: list = None,
                 loop_tool_call: bool = True,
                 max_tool_return_length=1000,

                 warning_token_count: int = 100000,):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.model = model
        self.history_max_messages = history_max_messages

        self.logging_level = logging_level
        self.logging_levels = ["debug", "info", "warning", "error"]
        self.answer_json = answer_json
        self.loop_tool_call = loop_tool_call
        self.reset_token_count = reset_token_count
        self.log_file = log_file
        self.chat_file = chat_file

        self.check_for_commands = check_for_commands
        self.commands = commands or []

        self.start_memory_files = start_memory_files or []
        self.always_in_memory_files = always_in_memory_files or []
        self.always_in_memory_folders = always_in_memory_folders or []

        self.max_memory_files = max_memory_files
        self.show_line_numbers = show_line_numbers

        self.save_file = save_file
        self.load_from_file = load_from_file
        self.save_to_file = save_to_file
        self.tools = tools or []

        self.max_tool_return_length = max_tool_return_length

        self.warning_token_count = warning_token_count
