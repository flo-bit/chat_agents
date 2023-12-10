from chat_agent import ChatAgent
from chat_agent.chat_agent import ChatAgentConfig
from chat_agent.tools import tool_list_files, tool_read_file, tool_replace_file, tool_text_to_speech, tool_create_image

import gradio as gr

default_config = ChatAgentConfig(
    debug=False,
    tools=[tool_list_files, tool_read_file, tool_replace_file,
           tool_text_to_speech, tool_create_image],
    system_prompt="You are a helpful chat bot. When you want to send a file to the user, send a message with the link to the file (e.g. image, audio) in markdown format (e.g. [file](https://example.com/file.txt)). Local files are not supported, just tell the user the path and that they have to open it themselves")


class WebBot():
    def __init__(self, config: ChatAgentConfig = default_config) -> None:
        self.agent = ChatAgent(config=config)
        self.create_interface()

    def create_interface(self):
        CSS = """
.contain { display: flex; flex-direction: column; }
.gradio-container { height: 100vh !important; }
#component-0 { height: 100%; }
#chatbot { flex-grow: 1; overflow: auto;}
"""
        with gr.Blocks(css=CSS) as demo:
            chatbot = gr.Chatbot(
                elem_id="chatbot", bubble_full_width=False, scale=2)
            msg = gr.Textbox()

            async def respond(message, chat_history):
                answer = await self.agent.send_message(message)
                chat_history.append((message, answer))
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])

        demo.launch()
