##
# BE VERY CAREFUL WITH THESE TOOLS AS THEY CAN BE
# USED TO LET CHAD DO ANYTHING ON YOUR COMPUTER ^^
##


import contextlib
import subprocess
import io


async def execute_python_code(agent, code: str):
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


async def run_command(agent, command: str):
    process = subprocess.Popen(command.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    content, error = process.communicate()

    if process.returncode == 0:
        return ('ok', content.decode())
    else:
        return ('error', error.decode())


async def format_file(agent, path: str):
    return run_command(agent, f"npx prettier {path} --write")


async def run_python_test(agent, path: str, test: str, class_name: str = "Tests"):
    status, error = await run_command(agent, f"python3 {path} {class_name}.{test}")
    print(status, error)
    return status == 'ok'


tool_execute_python_code = {
    "info": {
        "type": "function",
        "function": {
            "name": "execute_python_code",
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
    },
    "function": execute_python_code,
}

tool_format_file = {
    "info": {
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
    },
    "function": format_file,
}

tool_run_command = {
    "info": {
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
        },
    },
    "function": run_command,
}

tool_run_python_test = {
    "info": {
        "type": "function",
        "function": {
            "name": "run_python_test",
            "description": "Runs a python unit test.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to test file the test is in, relative to the current working directory"
                    },
                    "test": {
                        "type": "string",
                        "description": "Name of the test to run"
                    },
                    "class_name": {
                        "type": "string",
                        "description": "Name of the test class, defaults to Tests"
                    },
                },
                "required": ["path", "test"],
            },
        }
    },
    "function": run_python_test,
}
