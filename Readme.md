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