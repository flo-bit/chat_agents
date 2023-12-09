import os
import re


async def add_to_file(path: str, content: str, at_start: bool = False):
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


async def change_file(path: str, new: str, old_string: str = "", old_regex: str = None):
    with open(path, "r") as f:
        content = f.read()

    if old_regex:
        content = re.sub(old_regex, new, content)
    else:
        content = content.replace(old_string, new)

    with open(path, "w") as f:
        f.write(content)

    return f"file at {path} changed"


async def read_file_direct(path: str):
    with open(path, "r") as f:
        content = f.read()

    return f"file at {path}: {content}\n\n"


async def read_files_direct(paths: list):
    content = ""
    for path in paths:
        content += await read_file_direct(path)

    return content


async def list_files(path: str):
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    return f"Files in {path}:\n" + "\n".join(files)

tool_list_files = ({
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
}, list_files)

tool_read_file = ({
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
}, read_file_direct)

tool_read_files = ({
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
    }
}, read_files_direct)

tool_add_to_file = ({
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
}, add_to_file)

tool_change_file = ({
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
        },
    }
}, change_file)
