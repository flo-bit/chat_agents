import subprocess


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
