from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chat_agent import ChatAgent


async def add_task(agent, task: str, status: str = "todo", data: dict = None):
    if not hasattr(agent, 'tasks') or agent.tasks is None:
        agent.tasks = []

    if data is None:
        data = {}

    data['status'] = status

    agent.tasks.append((task, data))

    return f"Task {task} added to tasks\n\n" + await list_tasks(agent)


async def remove_task(agent, task: str):
    if not hasattr(agent, 'tasks') or agent.tasks is None:
        agent.tasks = []

    agent.tasks = [t for t in agent.tasks if t[0] != task]

    return f"Task {task} removed from tasks\n\n" + await list_tasks(agent)


async def change_task_status(agent, task: str, status: str):
    if not hasattr(agent, 'tasks') or agent.tasks is None:
        agent.tasks = []

    for i, t in enumerate(agent.tasks):
        if t[0] == task:
            agent.tasks[i][1]['status'] = status

    return f"Task {task} changed to status {status}\n\n" + await list_tasks(agent)


async def list_tasks(agent):
    if not hasattr(agent, 'tasks') or agent.tasks is None:
        agent.tasks = []

    tasks = '\n'.join([f'{t[0]}: {t[1]}' for t in agent.tasks]) if len(
        agent.tasks) > 0 else 'No tasks'
    return f"All tasks:\n{tasks}"


async def get_first_task_with_status(agent, status: str):
    if not hasattr(agent, 'tasks') or agent.tasks is None:
        agent.tasks = []

    for t in agent.tasks:
        if t[1]['status'] == status:
            return f"Task: {t[0]}: {t[1]['status']}"

    return None

tool_add_task = {
    "info": {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Adds a task to the agent's task list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Task to add"
                    },
                    "status": {
                        "type": "string",
                        "description": "Status of the task, will be added to the task data",
                        "default": "todo"
                    },
                    "data": {
                        "type": "object",
                        "description": "Data to add to the task arguments",
                        "default": {}
                    }
                },
                "required": ["task"],
            },
        }
    },
    "function": add_task,
    "arguments": {}
}

tool_get_first_task_with_status = {
    "info": {
        "type": "function",
        "function": {
            "name": "get_first_task_with_status",
            "description": "Gets the first task with a given status",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Status of the task to find"
                    }
                },
                "required": ["status"],
            },
        }
    },
    "function": get_first_task_with_status,
    "arguments": {}
}

tool_change_task_status = {
    "info": {
        "type": "function",
        "function": {
            "name": "change_task_status",
            "description": "Changes the status of a task in the agent's task list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Task to change"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status of the task"
                    }
                },
                "required": ["task", "status"],
            },
        }
    },
    "function": change_task_status,
    "arguments": {}
}

tool_remove_task = {
    "info": {
        "type": "function",
        "function": {
            "name": "remove_task",
            "description": "Removes a task from the agent's task list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Task to remove"
                    }
                },
                "required": ["task"],
            },
        }
    },
    "function": remove_task,
    "arguments": {}
}

tool_list_tasks = {
    "info": {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Lists all tasks in the agent's task list",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        }
    },
    "function": list_tasks,
    "arguments": {}
}
