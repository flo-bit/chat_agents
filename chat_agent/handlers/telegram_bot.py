import os
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from dotenv import load_dotenv
import re

from chat_agent import ChatAgent
from chat_agent.chat_agent import ChatAgentConfig
from chat_agent.tools import tool_list_files, tool_read_file, tool_replace_file, tool_text_to_speech, tool_create_image

load_dotenv()

default_config = ChatAgentConfig(
    debug=False,
    check_for_commands=False,
    tools=[tool_list_files, tool_read_file, tool_replace_file,
           tool_text_to_speech, tool_create_image],
    system_prompt="You are a helpful chat bot. When you want to send a file to the user, send a message with the link to the file (e.g. image, audio) in markdown format (e.g. [file](https://example.com/file.txt)) it will be removed from the message and sent as a file. If you are sending a local file, start the link with 'file://' e.g. 'file://path/to/file'")


class TelegramBot():
    def __init__(self, config: ChatAgentConfig = default_config, start_message: str = "Hello! I am a chat bot. Send me a message and I will try to answer it."):
        self.sessions: dict[any, ChatAgent] = {}
        self.config = config
        self.start_message = start_message

        app = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()

        chat_handler = MessageHandler(
            filters.TEXT & (~filters.COMMAND), self.chat_fn)

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(chat_handler)

        app.run_polling()

    def get_agent(self, chat_id):
        if chat_id not in self.sessions:
            self.sessions[chat_id] = ChatAgent(config=self.config)
        return self.sessions.get(chat_id)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.get_agent(update.effective_chat.id).add_message_to_history(
            "assistant", self.start_message)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.start_message)

    async def chat_fn(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id

        msg = update.message.text
        agent = self.get_agent(chat_id)

        # check for command, we turned off check_for_commands in the config, so we need to check here
        # as our system prompt may be returned as an answer and that f*cks up the link searching below otherwise
        answer = await agent.check_for_commands(msg)
        if answer:
            await context.bot.send_message(chat_id=chat_id, text=answer)
            return

        answer = await agent.send_message(msg)
        print(answer)

        # find all links in the answer and send them as files, using regex
        links = re.findall(r"\[.*?\]\((http.*?)\)", answer)
        for link in links:
            await context.bot.send_document(chat_id=chat_id, document=link)
            # remove link from answer using regex looking for ![.*?](link) or [.*?](link)
            answer = re.sub(
                r"!\[.*?\]\(" + re.escape(link) + r"\)", "", answer)
            answer = re.sub(r"\[.*?\]\(" + re.escape(link) + r"\)", "", answer)

        # find all local files in the answer and send them as files, using regex
        links = re.findall(r"\[.*?\]\((file:.*?)\)", answer)
        for link in links:
            await context.bot.send_document(chat_id=chat_id, document=open(link[7:], "rb"))
            # remove link from answer using regex looking for ![.*?](link) or [.*?](link)
            answer = re.sub(
                r"!\[.*?\]\(" + re.escape(link) + r"\)", "", answer)
            answer = re.sub(r"\[.*?\]\(" + re.escape(link) + r"\)", "", answer)

        # only send answer if it is not empty or only contains whitespace
        if answer and not answer.isspace():
            await context.bot.send_message(chat_id=chat_id, text=answer)
