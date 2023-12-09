##
# BE VERY CAREFUL WITH THESE TOOLS AS THEY CAN BE
# USED TO LET CHAD DO ANYTHING ON YOUR COMPUTER ^^
##


import contextlib
import subprocess
import io


async def execute_code(code: str):
    # we should do something like this to prevent malicious code execution
    # import builtins
    # safe_builtins = {name: getattr(builtins, name) for name in ['range', 'len', 'int', 'float', 'str']}
    # safe_namespace = {'__builtins__': safe_builtins}
    # exec(code, safe_namespace)

    # Buffer to capture print statements
    output_buffer = io.StringIO()

    # Redirect standard output to the buffer
    with contextlib.redirect_stdout(output_buffer):
        try:
            exec(code)
        except Exception as e:
            return f"Error during execution: {e}\n"

    # Handle the last line for possible output
    last_line = code.split("\n")[-1]
    if last_line.lstrip() == last_line:
        try:
            result = eval(last_line)
            if result is not None:
                output_buffer.write(str(result) + '\n')
        except Exception as e:
            output_buffer.write(f"Error on last line: {e}\n")

    return output_buffer.getvalue()


def run_command(command: str):
    process = subprocess.Popen(command.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    content, error = process.communicate()

    if process.returncode == 0:
        return ('ok', content.decode())
    else:
        return ('error', error.decode())


def format_file(path: str):
    return run_command(f"npx prettier {path} --write")


tool_execute_code = ({
    "type": "function",
    "function": {
        "name": "execute_code",
        "description": "Executes python code.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Code to execute",
                },
            },
            "required": ["code"],
        },
    }
}, execute_code)

tool_format_file = ({
    "type": "function",
    "function": {
        "name": "format_file",
        "description": "Formats a file using prettier.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to file to format, relative to the current working directory"
                }
            },
            "required": ["path"],
        },
    }
}, format_file)

tool_run_command = ({
    "type": "function",
    "function": {
        "name": "run_command",
        "description": "Runs a command in the shell.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Command to run",
                },
            },
            "required": ["command"],
        },
    }
}, run_command)
