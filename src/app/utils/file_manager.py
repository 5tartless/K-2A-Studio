import os, json
from pathlib import Path

def read(path: str, useJson=False):
    content = None
    with open(path, "r") as file:
        content = file.read() if not useJson else json.load(file)

    return content

def write(path: str, content, string_mode: bool = False):
    with open(path, "w") as file:
        if not string_mode:
            json.dump(content, file, indent=4)
        else:
            try:
                raw_content = json.loads(content)
            except json.JSONDecodeError:
                raw_content = content
            file.write(raw_content)

def path_exists(path) -> bool: 
    return os.path.exists(path) if path else False

def get_file_name(path) -> str:
    if path_exists(path):
        return os.path.basename(path)
    return ""
