import os, json, shutil
from pathlib import Path

# Raíz del proyecto (la carpeta que contiene "src"), calculada desde la ubicación real
# de este archivo. Así no importa desde dónde se lance la app (VS Code, doble clic,
# una terminal en otra carpeta, etc.): los archivos internos del proyecto siempre se
# encuentran, en vez de depender del directorio de trabajo actual (cwd).
PROJECT_ROOT = Path(__file__).resolve().parents[3]

def resolve(relative_path: str) -> str:
    """Convierte una ruta relativa a la raíz del proyecto (ej: 'src/app/web/editor.html')
    en una ruta absoluta real, sin depender del directorio de trabajo actual."""
    return str(PROJECT_ROOT / relative_path)

def read(path: str, useJson=False):
    content = None
    try:
        with open(path, "r") as file:
            content = file.read() if not useJson else json.load(file)
    except UnicodeDecodeError:
        content = "Couldn't read file properly."
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

def abspath(path) -> str:
    return os.path.abspath(path)