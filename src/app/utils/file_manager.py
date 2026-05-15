import os, pathlib, json

def read(path: str, useJson=False):
    content = None
    with open(path, "r") as file:
        content = file.read() if not useJson else json.load(file)

    return content

def write(path: str, content: any):
    with open(path, "w") as file:
        json.dump(content, file)

def path_exist(path) -> bool:
    return os.path.exists(path)