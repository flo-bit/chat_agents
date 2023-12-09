import gradio as gr
from chat_agent.chat_agent import ChatAgent
from chat_agent.tools.files import tool_list_files, tool_read_file, tool_replace_file
from chat_agent.tools.text_to_speech import tool_text_to_speech
from chat_agent.tools.image_creation import tool_create_image

# give your agent some tools to work with
agent = ChatAgent(
    tools=[tool_list_files, tool_read_file, tool_replace_file, tool_text_to_speech, tool_create_image], debug=False)

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    async def respond(message, chat_history):
        answer = await agent.send_message(message)
        chat_history.append((message, answer))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    tabs = gr.TabbedInterface([demo])

    tabs.launch()
