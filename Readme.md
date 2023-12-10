# python starter chatgpt

starter code for using chatgpt agents, includes:

- system prompt
- debug logging
- token counting
- tool calling
- some tools
- agent communication
- saving and loading agent from file
- chat using telegram or terminal

## Usage

create and switch to the virtual environment:

```bash
python3 -m venv .venv && source .venv/bin/activate
```

install the requirements:

```bash
pip3 install -r requirements.txt
```

add `.env` file with the following content:

```bash
OPENAI_API_KEY=<your openai api key>

# if you want to use the telegram bot
TELEGRAM_TOKEN=<your telegram bot token, get one by writting @BotFather on Telegram>
```

run the agent, e.g. by using one of the quickstart scripts:

```bash
python3 quickstarts/terminal_bot.py
```

## Tools

### Files

> [!WARNING]
> be very careful with these, Chad can really mess up your system with these, also don't share your bot with anyone if you use these (e.g. using telegram) as it's very easy to read out your OPENAI_API_KEY from the bot otherwise

- Read files into memory (=> every chat processed will contain the file read from disk at the end, until removed)
- Remove files from memory
- Add to file (append to file on disk, appending at the end or at the beginning of the file)
- replace lines of file from X to Y with new array of lines
- Replace file with new file (replace file on disk with new file)
- List files in folder (recursively)

### Coding 

> [!WARNING]
> be very careful with these, Chad can really mess up your system with these, also don't share your bot with anyone if you use these (e.g. using telegram) as it's very easy to read out your OPENAI_API_KEY from the bot otherwise

- run python code
- run bash command
- format file (uses `npx prettier`)
- run python test method from class in file (unittests)

### Image creation

- Create image using dall-e-2 or dall-e-3 from a prompt, different sizes available
- Create multiple images from multiple prompts

### Send message

- Send a message to another agent

### Tasks

- Create a task (task list is in ChatAgent memory)
- Mark a task as done
- Delete a task
- List all tasks

### Text to speech

- Convert text to speech using openai tts, choose model and voice
- Convert multiple texts to speeches

### Speech to text

- Convert speech to text using openai whisper
- Convert multiple speeches to texts

### Vision

- Describe image using gpt-4 vision
- Describe multiple images

# Commands

Commands are used to get info about a agent or change it's behaviour, the default commands are:

- `help` - show help
- `debug <on/off>` - set debug logging
- `info` - show info about the agent (token count, files in memory, commands, system prompt, model)
- `history` - show chat history
- `save <file>` - save agent to file
- `load <file>` - load agent from file (overwrites current agent, will not import custom tools and custom commands that are not in the current agent)
- `reset` - reset agent (clears chat history, files in memory, system prompt, data saved by tools)
- `clear memory` - clear files in memory
- `clear history` - clear chat history
- `messages`- show all messages that will be sent with the next chat message

# Documentation

## ChatAgentConfig

The `ChatAgentConfig` class is used to configure the agent, it has the following arguments:

- `commands` - list of commands, see `custom_command.py` for an example, default: `default_commands`
- `tools` - list of tools, see `custom_tool.py` for an example, default: []
- `debug` - debug logging to console, default: `False` can be turned on during chat with `debug on` command
- `name` - name of the agent, default: `Chad`
- `description` - description of the agent, default `None`
- `model` - model to use, default: `gpt-4-1106-preview`
- `system_prompt` - system prompt, default: `None`
- `history_max_messages` - max number of messages to send with prompt, default: `10`
- `answer_json` - if the answer should be json, default: `False`
- `loop_function_call` - if the response of a function call should be inputed as a new prompt, default: `True`
- `log_file` - log file, saving all logs to, default: `None`
- `chat_file` - chat file, saving chat to, default: `None`
- `start_memory_files` - files to start with in memory, default: `[]`
- `always_in_memory_files` - files that should always be in memory, default: `[]`
- `max_memory_files` - max number of files in memory (without always_in_memory_files), default: `3`, will remove oldest files first
- `show_line_numbers` - show line numbers when sending chad a memory file, default: `False`
- `check_for_commands` - check for commands in chat, default: `True`
- `save_file` - file to save agent to, default: `None`
- `load_from_file` - whether to load agent from save_file on startup, default: `True` (but only has an effect if save_file is given and exists)
- `save_to_file` - whether to save agent to save_file on any change, default: `True` (but only has an effect if save_file is given)
- `warning_token_count` - send a warning if the input token count is higher than this (in the last prompt), default: `100,000`


## Handlers

Handlers are used to get messages from the user to the agent and back. There are currently 3 handlers available:

- `TerminalHandler` - used to chat with the agent in the terminal
- `TelegramHandler` - used to chat with the agent using telegram
- `WebHandler` - used to chat with the agent using a web interface (built with gradio)

See how to use these handlers in the quickstart scripts.

## Custom handler

You need a custom handler if you want more than just one agent or if you want a different method of communication. If you just want different tools or commands, you can use the `ChatAgentConfig` class.

See `custom_handler.py` for an example.

1. Create a ChatAgent instance passing in an optional config
2. Get a user question and call `await agent.send_message(question)` on the agent to get a response
3. Repeat

```python
import asyncio
from chat_agent import ChatAgent

agent = ChatAgent()

async def chat():
    while True:
        question = input("> ")
        if question == "": # exit on empty input
            break
        answer = await agent.send_message(question)
        print(answer)

asyncio.run(chat())
```

## Custom commands

See `custom_command.py` for an example.

1. Create an async function that takes the agent and the message as arguments and returns a string
2. Create a command definition with the following keys: `name`, `function`, `description`, `regex` (optional, if not given, the command will be matched by name)
3. Add the command to the config

```python
from chat_agent import ChatAgentConfig, default_commands

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

# create a new config
config = ChatAgentConfig(commands=default_commands + [hello_command])
# use the config to create a new agent
```

## Custom tools

See `custom_tool.py` for an example.

1. Create an async function that takes the agent and some arguments as arguments and returns a string
2. Create

```python
from chat_agent import ChatAgentConfig

# has to be async and agent as argument
async def fibonacci(agent, n):
    if n < 0:
        raise ValueError("Negative arguments not implemented")
    if n <= 1:
        return n
    else:
        return await fibonacci(agent, n-1) + await fibonacci(agent, n-2)

# has to have the following keys: info, function
# info should be the json schema that will be passed to the chatgpt api 
# see existing tools for how this can look
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
# use the config to create a new agent
```



## Todo

- [ ] better documentation
- [ ] prebuilt agents

# Future tool ideas

- wikipedia search
- internet search
- vector database (add, remove, update, search)
- convert different file types (e.g. pdf to txt)
- combine audio files
- combine image + audio to video
- combine video + audio to video
- background removal from image
- image face swap
- find right tool
- find icon from list

# Agent ideas

- code review bot (review code, give feedback)
- input image with person and get generated image with that person (using description)
- create slideshows using sli.dev (markdown slideshows)
- create simple games
- create simple websites
- create simple machine learning models


## License

MIT

## Waranty

None, use at your own risk