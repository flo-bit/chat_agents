import asyncio
from chat_agent import ChatAgent
from chat_agent.chat_agent import ChatAgentConfig
from chat_agent.tools import tool_list_files, tool_read_file, tool_replace_file, tool_text_to_speech, tool_create_image

default_config = ChatAgentConfig(
    tools=[tool_list_files, tool_read_file, tool_replace_file,
           tool_text_to_speech, tool_create_image],
    system_prompt="You are a helpful chat bot.")

agent = ChatAgent(config=default_config)


async def chat():
    while True:
        question = input("> ")

        # ChatAgent checks if the question is a command for us
        # we only need to check for empty or exit
        if question == "" or question == "exit":
            break
        print("thinking...")

        answer = await agent.send_message(question)
        print(answer)

    print("Bye! See you soon!")

if __name__ == "__main__":
    asyncio.run(chat())
