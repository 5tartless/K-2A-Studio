import re
import requests

# --- Configuración de Ollama (local, gratis, sin API key) ---
# Requisitos en la máquina del usuario:
#   1. Instalar Ollama: https://ollama.com/download
#   2. Descargar el modelo (una sola vez):  ollama pull qwen3:4b
#   3. Tener el servicio corriendo (normalmente se inicia solo, si no: ollama serve)
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_BASE_URL}/api/chat"
DEFAULT_MODEL = "qwen3:4b"
MAX_HISTORY_MESSAGES = 12  # ~6 intercambios; evita saturar el contexto de un modelo chico

# --- Prompt para la conversación normal ---
# Texto libre, sin ningún formato forzado: el modelo escribe igual que en un chat normal.
CHAT_SYSTEM_PROMPT = (
    "Eres un asistente de programación integrado en un editor de código llamado K-2A Studio. "
    "Respondes siempre en español, de forma natural, clara y breve, como en un chat normal. "
    "No uses JSON ni ningún formato especial en tu respuesta, solo texto normal.\n\n"
    "IMPORTANTE sobre el entorno: por el momento K-2A Studio SOLO soporta y ejecuta código "
    "Python real y estándar (el mismo Python que se instala con python.org, sin funciones "
    "propias ni inventadas del editor). No existen funciones propias del editor como "
    "'showtext', 'showshow' ni nada similar — NUNCA inventes funciones que no sean de la "
    "librería estándar de Python o de paquetes públicos reales. Para mostrar texto en pantalla "
    "se usa la función nativa de Python `print()`, igual que en cualquier script de Python normal.\n\n"
    "Si el usuario te pide que escribas código, escríbelo completo directamente en tu "
    "respuesta, con sus saltos de línea normales. El usuario puede tener un archivo abierto "
    "en su editor; si te comparto su código como contexto, úsalo solo si es relevante para lo "
    "que te está preguntando. Sé conciso: evita repetir la misma idea o palabra dos veces."
)

# --- Prompt aparte, solo para la revisión puntual de código (resaltado amarillo) ---
# Antes esto pedía JSON estricto ("format": "json"), lo cual fuerza al modelo a generar
# token por token dentro de una gramática rígida y también le resta fluidez/calidad. Ahora
# le pedimos texto libre en un formato simple de una línea por sugerencia, y lo interpretamos
# nosotros con una expresión regular — sin atar al modelo a ninguna gramática.
SUGGESTIONS_SYSTEM_PROMPT = (
    "Eres un revisor de código Python. Se te va a dar un fragmento de código Python real y "
    "estándar. Señala, si las hay, mejoras puntuales: errores, malas prácticas, nombres poco "
    "claros, código repetido, rendimiento, seguridad, etc.\n\n"
    "Responde ÚNICAMENTE con una lista de sugerencias, una por línea, en este formato exacto "
    "y sin nada más (sin introducción, sin explicación aparte, sin markdown):\n"
    "[línea_inicio-línea_fin] explicación breve de la mejora\n\n"
    "Ejemplo de respuesta con dos sugerencias:\n"
    "[3-5] Esta función se puede simplificar usando una comprensión de listas.\n"
    "[10-10] Falta manejar el caso en que el archivo no exista.\n\n"
    "Las líneas se cuentan desde 1. No inventes números de línea que no existan en el código. "
    "Si no hay ninguna mejora que valga la pena señalar, responde únicamente con la palabra: "
    "NINGUNA"
)

# Reconoce líneas con formato "[3-5] texto de la sugerencia"
SUGGESTION_LINE_RE = re.compile(r"^\s*\[\s*(\d+)\s*-\s*(\d+)\s*\]\s*(.+?)\s*$", re.MULTILINE)


def _strip_think(text: str) -> str:
    """Quita el razonamiento interno ('thinking') de Qwen3 antes de mostrar la respuesta.
    Cubre dos casos: el bloque completo <think>...</think>, y el caso más común en Qwen3
    donde la etiqueta de apertura viene precargada en la plantilla interna del modelo (no
    llega como texto) y lo único que aparece en el contenido generado es el cierre </think>
    suelto, con todo el razonamiento antes de él."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    if "</think>" in text:
        text = text.split("</think>", 1)[1]
    return text.strip()


class AIManager:
    """Cliente simple para conversar con un modelo corriendo localmente en Ollama.
    Ninguna de las dos llamadas (chat / sugerencias) usa 'format: json': ambas dejan al
    modelo generar texto libre, para no sacrificar fluidez por estructura."""

    def __init__(self, model: str = DEFAULT_MODEL, base_url: str = OLLAMA_CHAT_ENDPOINT):
        self.model = model
        self.base_url = base_url
        self.history: list[dict] = []

    def reset_history(self) -> None:
        self.history = []

    def is_available(self) -> bool:
        """Comprueba rápidamente si Ollama está corriendo."""
        try:
            requests.get(OLLAMA_BASE_URL, timeout=2)
            return True
        except requests.RequestException:
            return False

    def _call_ollama(self, messages: list, temperature: float) -> dict:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "think": False,  # Qwen3 es un modelo híbrido "thinking"; lo desactivamos para
                              # que no meta bloques <think>...</think> antes de responder
            "options": {
                "temperature": temperature,
                "top_p": 0.9,
                "repeat_penalty": 1.1,   # valor estándar de Ollama; 1.15+ puede empujar al
                                         # modelo hacia sustituciones/repeticiones raras
                "repeat_last_n": 128,
                "num_predict": 1500,      # SIN tope artificial: antes esto (900) cortaba la
                                        # generación aparte de num_ctx, sin importar qué tan
                                        # grande fuera este último. Ahora el único límite real
                                        # es el espacio que quede dentro de num_ctx.
                "num_ctx": 8192,        # tu valor: de sobra para prompt + código + historial
            },
        }
        response = requests.post(self.base_url, json=payload, timeout=600)
        response.raise_for_status()
        data = response.json()
        message = data.get("message", {}) or {}
        return {
            "content": (message.get("content") or "").strip(),
            # si Ollama sí soporta separar el pensamiento del lado del servidor, viene aquí
            # limpio y aparte; si no, seguirá embebido dentro de 'content' como texto plano
            "thinking": (message.get("thinking") or "").strip(),
            # "length" = se acabó el espacio de num_ctx antes de que el modelo terminara por
            # su cuenta; "stop" = el modelo terminó normalmente
            "done_reason": data.get("done_reason", ""),
        }

    def chat(self, user_message: str, code: str = "", file_name: str = "") -> dict:
        """
        Envía un mensaje al modelo, opcionalmente adjuntando el código actual del editor.
        Devuelve: {"reply": str, "suggestions": [{"start_line", "end_line", "message"}]}
        """
        context = ""
        has_code = bool(code and code.strip())
        if has_code:
            context = (
                f"\n\n(El usuario tiene abierto el archivo '{file_name or 'sin nombre'}' con "
                f"este código, por si es relevante para tu respuesta:\n```\n{code}\n```)"
            )

        self.history.append({"role": "user", "content": user_message + context + "\n\n/no_think"})
        self.history = self.history[-MAX_HISTORY_MESSAGES:]

        messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}] + self.history

        try:
            result = self._call_ollama(messages, temperature=0.6)
        except requests.exceptions.ReadTimeout:
            return {
                "reply": (
                    " Ollama está tardando demasiado en responder (más de 10 minutos). "
                    "Sí está conectado, pero el modelo está siendo muy lento en tu equipo — "
                    "puede pasar la primera vez que lo cargas, o si tu PC no tiene GPU. "
                    "Puedes intentar de nuevo, cerrar otros programas que usen mucha RAM/CPU, "
                    "o probar un modelo más liviano."
                ),
                "suggestions": [],
            }
        except requests.RequestException as e:
            return {
                "reply": (
                    "⚠️ No pude conectar con Ollama. Verifica que esté instalado y corriendo, "
                    f"y que tengas el modelo descargado (`ollama pull {self.model}`).\n\n"
                    f"Detalle técnico: {e}"
                ),
                "suggestions": [],
            }

        raw_reply = result["content"]
        self.history.append({"role": "assistant", "content": raw_reply})

        if result["thinking"]:
            # Ollama separó el pensamiento del lado del servidor: 'content' ya viene limpio.
            reply = raw_reply
        elif "</think>" in raw_reply:
            # el pensamiento vino embebido como texto; lo recortamos nosotros
            reply = _strip_think(raw_reply)
        elif result["done_reason"] == "length":
            # se acabaron los tokens (num_predict) y no hay ninguna señal de que haya
            # terminado de pensar: NO es seguro asumir que 'raw_reply' sea ya la respuesta
            # real, así que avisamos en vez de mostrar ese texto (probablemente sea
            # razonamiento interno a medio terminar).
            reply = (
                "🤔 Se me acabó el tiempo pensando la respuesta antes de llegar a "
                "escribirla. ¿Puedes probar de nuevo, o hacer la pregunta un poco más "
                "corta/directa?"
            )
        else:
            # terminó normalmente y no hay ninguna señal de pensamiento de por medio
            reply = raw_reply

        reply = reply.strip() or (
            "🤔 No obtuve una respuesta con contenido. ¿Puedes probar de nuevo?"
        )

        # La revisión de código es una llamada aparte, y solo se hace si hay código real.
        suggestions = self._get_suggestions(code, file_name) if has_code else []

        return {"reply": reply, "suggestions": suggestions}

    def _get_suggestions(self, code: str, file_name: str) -> list:
        messages = [
            {"role": "system", "content": SUGGESTIONS_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Archivo '{file_name or 'sin nombre'}':\n```\n{code}\n```\n\n/no_think"
            }
        ]
        try:
            result = self._call_ollama(messages, temperature=0.3)
        except requests.RequestException:
            return []  # si falla, simplemente no hay sugerencias esta vez, no rompe el chat

        raw = result["content"]
        if result["thinking"]:
            cleaned = raw  # ya viene limpio del lado del servidor
        elif "</think>" in raw:
            cleaned = _strip_think(raw)
        elif result["done_reason"] == "length":
            return []  # se cortó a medio pensar; mejor no mostrar nada a inventar líneas
        else:
            cleaned = raw

        if not cleaned or cleaned.strip().upper().startswith("NINGUNA"):
            return []

        suggestions = []
        for match in SUGGESTION_LINE_RE.finditer(cleaned):
            start, end, message = match.groups()
            suggestions.append({
                "start_line": int(start),
                "end_line": int(end),
                "message": message,
            })
        return suggestions


# instancia única compartida por toda la app
ai_manager = AIManager()
