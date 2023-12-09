def reset(agent, message):
    agent.reset()
    return "Agent reset"


def info(agent, message):
    return agent.info()


def history(agent, message):
    return str(agent)


def clear_memory(agent, message):
    agent.clear_memory()
    return "Memory cleared"


def read(agent, message):
    agent.add_memory_file(message.split("read ")[1])
    return f"Added file {message.split('read ')[1]} to memory"


def debug(agent, message):
    agent.set_debug("on" in message)
    return f"Debug mode {'on' if agent.config.debug else 'off'}"


def help(agent, message):
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
        "name": "read",
        "function": read,
        "description": "<file> - adds a file to the memory of the chat agent",
        "regex": "^read \S*$"
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
    }
]


class ChatAgentConfig:
    def __init__(self,
                 name: str = 'ChatAgent',
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
                 all_time_tokens_input=0,
                 all_time_tokens_output=0,
                 max_memory_files=3,
                 show_line_numbers=False,
                 check_for_commands=False,
                 tools=None):
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

        self.all_time_tokens_input = all_time_tokens_input
        self.all_time_tokens_output = all_time_tokens_output
        self.max_memory_files = max_memory_files
        self.show_line_numbers = show_line_numbers

        self.tools = tools or []