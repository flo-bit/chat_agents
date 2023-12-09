from chat_agent.handlers import TerminalBot
from chat_agent import ChatAgentConfig
from chat_agent.tools import tool_add_task, tool_remove_task, tool_list_tasks, tool_change_task_status, tool_get_first_task_with_status

config = ChatAgentConfig(tools=[tool_add_task, tool_remove_task, tool_list_tasks,
                         tool_change_task_status, tool_get_first_task_with_status])
TerminalBot(config=config)
