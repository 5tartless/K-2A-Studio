import os
import subprocess
import sys
import tempfile

# Mapa de extensión de archivo -> comando de intérprete/compilador.
# Por ahora el editor está pensado sobre todo para Python (así lo tiene fijado Monaco),
# pero dejamos esto como diccionario para poder agregar más lenguajes fácilmente.
RUNNERS = {
    ".py": [sys.executable],
}
DEFAULT_EXTENSION = ".py"


def run_code(code: str, extension: str = DEFAULT_EXTENSION, timeout: int = 20) -> dict:
    """
    Ejecuta 'code' en un proceso aparte (no bloquea la UI si se llama desde un Worker/hilo).
    Devuelve: {"stdout": str, "stderr": str, "exit_code": int|None, "timed_out": bool}
    """
    command = RUNNERS.get(extension, RUNNERS[DEFAULT_EXTENSION])
    result = {"stdout": "", "stderr": "", "exit_code": None, "timed_out": False}

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=extension or DEFAULT_EXTENSION, delete=False, encoding="utf-8"
        ) as tmp_file:
            tmp_file.write(code)
            tmp_path = tmp_file.name

        process = subprocess.run(
            [*command, tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        result["stdout"] = process.stdout
        result["stderr"] = process.stderr
        result["exit_code"] = process.returncode

    except subprocess.TimeoutExpired:
        result["timed_out"] = True
        result["stderr"] = f"El código tardó más de {timeout} segundos en ejecutarse y fue detenido."
    except Exception as e:
        result["stderr"] = f"No se pudo ejecutar el código: {e}"
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    return result
