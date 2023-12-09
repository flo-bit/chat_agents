# python starter chatgpt

starter code for using chatgpt agents, includes:

- system prompt
- debug logging
- token counting
- tool calling
- some tools
- agent communication
- saving and loading agent from file
- instruct through telegram or terminal

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

### ChatAgentConfig

### Sending Messages between Agents

## Todo

- [ ] add tool input to token count
- [ ] add better logging (LOGGING LEVELS)