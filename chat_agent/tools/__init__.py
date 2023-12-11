from .coding import tool_commit_all, tool_execute_python_code, tool_format_file, tool_run_command, tool_run_python_test, tool_see_git_diff
from .files import tool_add_to_file, tool_change_file, tool_forget_file, tool_list_files, tool_read_file, tool_read_files, tool_replace_file, tool_replace_lines
from .image_creation import tool_create_image, tool_create_images
from .send_message import create_send_message_tool
from .text_to_speech import tool_text_to_speech, tool_texts_to_speeches
from .speech_to_text import tool_speech_to_text, tool_speeches_to_texts
from .tasks import tool_add_task, tool_change_task_status, tool_get_first_task_with_status, tool_list_tasks, tool_remove_task
from .tools import ToolChain
from .vision import tool_describe_image, tool_describe_images
from .gmail import tool_mark_email_as_read, tool_read_email, tool_search_emails, tool_send_email
from .pdf import tool_get_pdf_text

import importlib

module_names = ['coding', 'files', 'image_creation', 'send_message',
                'text_to_speech', 'speech_to_text', 'tasks', 'tools', 'vision', 'gmail', 'pdf']
tool_functions = {}

for name in module_names:
    # Dynamically import the module
    module = importlib.import_module('.' + name, package='chat_agent.tools')

    for item in dir(module):
        if item.startswith('tool_'):
            tool = getattr(module, item)
            tool_functions[tool["info"]["function"]["name"]] = tool["function"]
