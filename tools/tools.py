import json


class ToolChain:
    # pass in a list of tuples of (tool_dict, function)
    def __init__(self, tools, debug: bool = False, limit_return_value: int = 500) -> None:
        # dict of tool name to tool function
        self.methods = {}
        # list of tool dicts
        self.tool_dicts = []

        for tool_dict, function in tools:
            self.methods[tool_dict["function"]["name"]] = function
            self.tool_dicts.append(tool_dict)

        self.debug = debug
        self.limit_return_value = limit_return_value

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
            if is_json:
                return_value = await self.methods[toolcall.function.name](**args)
            else:
                return_value = await self.methods[toolcall.function.name](args)

            if self.limit_return_value:
                return_value = str(return_value)[-self.limit_return_value:]

            function_message = f"""Executed tool call {toolcall.function.name}({args}). Response: {
                return_value if (return_value is not None) else 'None'}."""
        except Exception as e:
            return_value = e
            function_message = f"""Could not execute tool call {
                toolcall.function.name}. Error: {return_value}."""

        if self.debug:
            print(function_message)

        return function_message
