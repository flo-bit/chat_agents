import asyncio
from chat_agent.chat_agent import ChatAgent
from chat_agent.tools import tool_add_task, tool_remove_task, tool_list_tasks, tool_change_task_status, tool_get_first_task_with_status

# give your agent some tools to work with
agent = ChatAgent(
    tools=[tool_add_task, tool_remove_task, tool_list_tasks, tool_change_task_status, tool_get_first_task_with_status], debug=True)


# run the agent in a loop
async def run_loop():
    while True:
        question = input("> ")
        print("thinking...")
        message = await agent.send_message(question)
        if message:
            print(message)

if __name__ == "__main__":
    asyncio.run(run_loop())
