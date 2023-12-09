from chat_agent.handlers import TerminalBot
from chat_agent import ChatAgentConfig
from chat_agent.tools import tool_add_task, tool_remove_task, tool_list_tasks, tool_change_task_status, tool_get_first_task_with_status
from chat_agent import default_commands


def hello(agent, message):
    return "Hello!"


commands = [{
    "name": "hello",
    "description": "Says hello",
    "function": hello,
}]

config = ChatAgentConfig(
    commands=commands + default_commands,
    tools=[tool_add_task, tool_remove_task, tool_list_tasks,
           tool_change_task_status, tool_get_first_task_with_status], save_file="test.json", check_for_commands=True, debug=True)
TerminalBot(config=config)
