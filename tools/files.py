import os
import re

from chat_agent import ChatAgent


async def add_to_file(agent, path: str, content: str, at_start: bool = False):
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    if at_start:
        with open(path, "a") as f:
            f.write(content)
    else:
        with open(path, "r") as f:
            file_content = f.read()

        file_content += content

        with open(path, "w") as f:
            f.write(file_content)

    return f"content added to file at {path}"


async def replace_lines(agent, path: str, new_lines: list, start_line: int = 0, end_line: int = None):
    with open(path, "r") as f:
        content = f.read()

    lines = content.split("\n")

    if end_line is None:
        end_line = len(lines)

    lines = lines[:start_line] + new_lines + lines[end_line:]

    content = "\n".join(lines)

    with open(path, "w") as f:
        f.write(content)

    return f"file at {path} changed"


async def change_file(agent, path: str, new: str, old_string: str = "", old_regex: str = None):
    with open(path, "r") as f:
        content = f.read()

    if old_regex:
        content = re.sub(old_regex, new, content)
    else:
        content = content.replace(old_string, new)

    with open(path, "w") as f:
        f.write(content)

    return f"file at {path} changed"


async def read_file(agent: ChatAgent, path: str):
    # check if file can be read
    with open(path, "r") as f:
        _ = f.read()

    agent.add_memory_file(path)

    return f"file at {path} memory\n"


async def read_files(agent, paths: list):
    content = ""
    for path in paths:
        content += await read_file(agent, path)

    return content


async def forget_file(agent: ChatAgent, path: str):
    agent.remove_memory(path)

    return f"file at {path} forgotten"

async def replace_file(agent, path: str, content: str):
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

    return f"file at {path} replaced"


async def list_files(agent, path: str):
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    return f"Files in {path}:\n" + "\n".join(files)

tool_list_files = {
    "info": {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lists all files in a directory and its subdirectories",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to directory to list files in, relative to the current working directory"
                    }
                },
                "required": ["path"],
            },
        }
    },
    "function": list_files,
}

tool_read_file = {
    "info": {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads a file into memory (= will be added to the chat)",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to read from, relative to the current working directory"
                    }
                },
                "required": ["path"],
            },
        }
    },
    "function": read_file,
}

tool_read_files = {
    "info": {
        "type": "function",
        "function": {
            "name": "read_files",
            "description": "Reads files into memory (= will be added to the chat)",
            "parameters": {
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "Path to read from, relative to the current working directory"
                        },
                        "description": "Files to read into memory"
                    }
                },
                "required": ["path"],
            },
        },
    },
    "function": read_files,
}

tool_forget_file = {
    "info": {
        "type": "function",
        "function": {
            "name": "forget_file",
            "description": "Forgets a file from memory (= will be removed from the chat)",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to forget, relative to the current working directory"
                    }
                },
                "required": ["path"],
            },
        }
    },
    "function": forget_file,
}

tool_add_to_file = {
    "info": {
        "type": "function",
        "function": {
            "name": "add_to_file",
            "description": "Adds something to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to file to add content to"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to add to file"
                    },
                    "at_start": {
                        "type": "boolean",
                        "description": "If true, content will be added at the start of the file instead of the end, defaults to false"
                    }
                },
                "required": ["path", "content"],
            },
        }
    },
    "function": add_to_file,
}

tool_replace_file = {
    "info": {
        "type": "function",
        "function": {
            "name": "replace_file",
            "description": "Replaces a file with new content, will create the file if it does not exist",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to file to replace"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to replace file with"
                    }
                },
                "required": ["path", "content"],
            },
        }
    },
    "function": replace_file,
}

tool_change_file = {
    "info": {
        "type": "function",
        "function": {
            "name": "change_file",
            "description": "Replaces all occurences of either a given string or regular expression with a new string in a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to file to change"
                    },
                    "old_string": {
                        "type": "string",
                        "description": "String to replace"
                    },
                    "old_regex": {
                        "type": "string",
                        "description": "Regular expression to replace"
                    },
                    "new": {
                        "type": "string",
                        "description": "String to replace with"
                    }
                },
                "required": ["path", "new"],
            },
        }
    },
    "function": change_file,
}

tool_replace_lines = {
    "info": {
        "type": "function",
        "function": {
            "name": "replace_lines",
            "description": "Replaces a range of lines in a file with new lines",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to file to change"
                    },
                    "new_lines": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                        "description": "New lines to replace with"
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "Line to start replacing at, defaults to 0"
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "Line to end replacing at, defaults to the end of the file"
                    },
                },
                "required": ["path", "new_lines"],
            },
        }
    },
    "function": replace_lines,
}
