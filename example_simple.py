import asyncio
from chat_agent import ChatAgent
from tools.files import tool_list_files, tool_read_file, tool_replace_file
from tools.text_to_speech import tool_text_to_speech
from tools.image_creation import tool_create_image

# give your agent some tools to work with
agent = ChatAgent(
    tools=[tool_list_files, tool_read_file, tool_replace_file, tool_text_to_speech, tool_create_image], debug=False)


async def run_loop():
    while True:
        question = input("> ")
        if question == "reset":
            agent.reset()
            continue
        if question == "exit":
            break
        if question == "info":
            print(agent.info())
            continue
        if question == "history":
            print(agent)
            continue
        if question == "help":
            print("""Commands:
- reset: resets the chat agent
- exit: exits the chat agent
- info: prints info about the chat agent
- history: prints the chat history
- help: prints this help message
""")
            continue

        message = await agent.send_message(question)
        print(message)

if __name__ == "__main__":
    asyncio.run(run_loop())
