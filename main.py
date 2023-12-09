import asyncio
from chat_agent import ChatAgent
from tools.files import tool_list_files


agent = ChatAgent(tools=[tool_list_files], debug=False)


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
