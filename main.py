import asyncio
from chat_agent import ChatAgent, ChatAgentConfig
from tools.coding import tool_run_python_test
from tools.files import tool_list_files, tool_change_file, tool_add_to_file
from tools.text_to_speech import tool_text_to_speech, tool_texts_to_speeches
from tools.speech_to_text import tool_speech_to_text
from tools.image_creation import tool_create_image
from tools.send_message import create_send_message_tool


creative_agent = ChatAgent(tools=[tool_create_image], config=ChatAgentConfig(
    name="Creative Agent", description="Ask this agent to create images.", debug=True))

agent = ChatAgent(
    tools=[create_send_message_tool(creative_agent)], debug=True)

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
