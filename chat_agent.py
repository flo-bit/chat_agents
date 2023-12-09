from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Literal
import tiktoken
import json

from tools.tools import ToolChain

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

Role = Literal["user", "assistant", "system"]

enc = tiktoken.encoding_for_model("gpt-4")


class ChatAgent:
    def __init__(self,
                 system_prompt: str = '',
                 chat_file: str = '',
                 log_file: str = '',
                 model: str = "gpt-4-1106-preview",
                 tools=None,
                 answer_json: bool = False,
                 loop_function_call: bool = True,
                 reset_token_count: bool = False,
                 debug: bool = True):
        self.history = []
        self.system_prompt = system_prompt
        self.model = model

        if system_prompt:
            self.history.append({"role": "system", "content": system_prompt})

        self.chat_file = chat_file
        self.log_file = log_file
        self.debug = debug
        self.answer_json = answer_json
        self.loop_function_call = loop_function_call

        self.tools = ToolChain(tools) if tools else None

        self.reset_token_count = reset_token_count
        self.all_time_tokens_input = 0
        self.all_time_tokens_output = 0

    def info(self):
        info = f"ChatAgent: \n\nmodel: {self.model}\n"
        if self.system_prompt:
            info += f"system prompt: {self.system_prompt}\n\n"

        if self.tools:
            info += "available tools: \n"
            for tool_dict in self.tools.tool_dicts:
                info += f"- {tool_dict['function']['name']}\n"
            info += "\n"

        info += f"Input token count: {self.all_time_tokens_input}\n"
        info += f"Output token count: {self.all_time_tokens_output}\n"

        return info

    def __str__(self):
        string = "\n"
        for message in self.history:
            string += f"\n\n> {message['role']}:\n{message['content']}"
        string += "\n\n\n"
        return string

    def add_message_to_history(self, role: Role, content: str):
        self.print(f"{role}: {content}")

        self.history.append({"role": role, "content": content})

        # write to file
        if self.chat_file:
            os.makedirs(os.path.dirname(self.chat_file), exist_ok=True)

            with open(self.chat_file, "w") as f:
                f.write(str(self))

    def reset(self):
        self.history = []
        if self.system_prompt:
            self.history.append(
                {"role": "system", "content": self.system_prompt})

        if self.reset_token_count:
            self.all_time_tokens_input = 0
            self.all_time_tokens_output = 0

    def print(self, message: str):
        if self.debug:
            print(message)
        if self.log_file:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

            with open(self.log_file, "a") as f:
                f.write(message + "\n")

    async def react(self):
        messages = self.history[-10:]

        token_count = 0
        for message in messages:
            token_count += len(enc.encode(message['content']))

        self.all_time_tokens_input += token_count

        self.print(
            f"input token count: {token_count} ({self.all_time_tokens_input}) - current (total)")
        self.print('Sending request...')

        response_format = {"type": "json_object"} if self.answer_json else None
        completion = client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format=response_format,
            tools=self.tools.tool_dicts if self.tools else None,
        )
        self.print('Received response!')

        if completion.choices[0].message.content:
            output_tokens = len(enc.encode(
                completion.choices[0].message.content))

            self.all_time_tokens_output += output_tokens
            self.print(
                f"output token count: {output_tokens} ({self.all_time_tokens_output}) - current (total)")

            self.add_message_to_history("assistant",
                                        completion.choices[0].message.content)

            if self.answer_json:
                return json.loads(completion.choices[0].message.content)

            return completion.choices[0].message.content

        if completion.choices[0].message.tool_calls and self.tools:
            for tool_call in completion.choices[0].message.tool_calls:
                self.all_time_tokens_output += len(
                    enc.encode(tool_call.function.name)) + len(
                    enc.encode(tool_call.function.arguments))

                function_message = await self.tools.tool_call(tool_call)
                self.add_message_to_history("system", function_message)

            if self.loop_function_call:
                return await self.react()

    async def send_message(self, message: str, role: Role = "user"):
        self.add_message_to_history(role, message)
        return await self.react()
