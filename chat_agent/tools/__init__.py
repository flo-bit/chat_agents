from .coding import *
from .files import *
from .image_creation import *
from .send_message import *
from .text_to_speech import *
from .speech_to_text import *
from .tasks import *
from .tools import *

import importlib

module_names = ['coding', 'files', 'image_creation', 'send_message',
                'text_to_speech', 'speech_to_text', 'tasks', 'tools']
tool_functions = {}

for name in module_names:
    # Dynamically import the module
    module = importlib.import_module('.' + name, package='chat_agent.tools')

    for item in dir(module):
        if item.startswith('tool'):
            tool = getattr(module, item)
            tool_functions[tool["info"]["function"]["name"]] = tool["function"]
