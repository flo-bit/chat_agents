import json


class ToolChain:
    # pass in a list of tuples of (tool_dict, function)
    def __init__(self, tools, debug: bool = False, limit_return_value: int = 500, agent=None) -> None:
        # dict of tool name to tool object
        self.tools = {}
        # list of tool infos to pass to chatgpt
        self.tool_info = []

        for tool in tools:
            self.add_tool(tool)

        self.debug = debug
        self.limit_return_value = limit_return_value

        self.agent = agent

    def add_tool(self, tool):
        self.tools[tool["info"]["function"]["name"]] = tool
        self.tool_info.append(tool["info"])

    async def tool_call(self, toolcall):
        if self.debug:
            print('calling tool', toolcall.function.name,
                  toolcall.function.arguments)

        args = toolcall.function.arguments

        is_json = False
        try:
            args = json.loads(args)
            is_json = True
        except Exception:
            pass

        try:
            method = self.tools[toolcall.function.name]["function"]
            extra_args = self.tools[toolcall.function.name]["arguments"] if "arguments" in self.tools[
                toolcall.function.name] else {}

            if is_json:
                return_value = await method(agent=self.agent, **args, **extra_args)
            else:
                return_value = await method(args, agent=self.agent, **extra_args)

            if self.limit_return_value:
                return_value = str(return_value)[-self.limit_return_value:]

            function_message = f"""Executed tool call {toolcall.function.name}({args}). Response: {
                return_value if (return_value is not None) else 'None'}."""

            self.agent.log(function_message)
        except Exception as e:
            return_value = e
            function_message = f"""Could not execute tool call {
                toolcall.function.name}. Error: {return_value}."""

            self.agent.log(function_message, 'error')

        return function_message
