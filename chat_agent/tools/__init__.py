from .coding import *
from .files import *
from .image_creation import *
from .send_message import *
from .text_to_speech import *
from .speech_to_text import *
from .tasks import *
from .tools import *
from .vision import *
from .gmail import *
from .pdf import *

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
