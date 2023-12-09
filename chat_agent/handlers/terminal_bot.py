import asyncio
from dotenv import load_dotenv

from chat_agent import ChatAgent
from chat_agent.chat_agent import ChatAgentConfig
from chat_agent.tools import tool_list_files, tool_read_file, tool_replace_file, tool_text_to_speech, tool_create_image

load_dotenv()

default_config = ChatAgentConfig(
    check_for_commands=True,
    debug=False,
    tools=[tool_list_files, tool_read_file, tool_replace_file,
           tool_text_to_speech, tool_create_image],
    system_prompt="You are a helpful chat bot.")


class TerminalBot():
    def __init__(self, config: ChatAgentConfig = default_config, start_message: str = "Hello! I am a chat bot. Send me a message and I will try to answer it."):
        self.agent = ChatAgent(config=config)
        self.config = config
        self.start_message = start_message

        self.start()

    def start(self):
        self.agent.add_message_to_history(
            "assistant", self.start_message)
        print(self.start_message)

        asyncio.run(self.chat())

    async def chat(self):
        while True:
            question = input("> ")

            # ChatAgent checks if the question is a command for us, we only need to check for empty or exit
            if question == "" or question == "exit":
                break
            print("thinking...")

            answer = await self.agent.send_message(question)
            print(answer)

        print("Bye! See you soon!")
