"""
Reproduce, paso a paso, el problema de modelito 1.4.5 con Ollama.

Requisitos: Ollama corriendo y el modelo llama3.2:3b descargado.
Ejecutar con el Python del venv de BatLLM:
    python reproducir_modelito.py
"""

import json
from urllib.request import Request, urlopen

import modelito
import modelito.ollama as modelito_ollama
from modelito import Client, Message, OllamaProvider

MODELO = "llama3.2:3b"
URL_CHAT = "http://localhost:11434/api/chat"


def post(payload: dict) -> str:
    """POST a /api/chat y devuelve el cuerpo crudo de la respuesta."""
    pedido = Request(
        URL_CHAT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(pedido, timeout=60) as respuesta:
        return respuesta.read().decode("utf-8")


def titulo(texto: str) -> None:
    print("\n" + "=" * 70 + f"\n{texto}\n" + "=" * 70)


print(f"modelito {modelito.__version__} | modelo {MODELO}")

mensajes = [{"role": "user", "content": "Decí solo: hola"}]

# ---------------------------------------------------------------------------
titulo('PASO 1: pedido SIN "stream": false (lo que hace modelito)')
cuerpo = post({"model": MODELO, "messages": mensajes})
lineas = cuerpo.strip().splitlines()
print(f"Ollama respondió {len(lineas)} líneas JSON (un pedazo de texto por línea):")
for linea in lineas[:3]:
    print("  ", linea[:120])
print("   ...")

# ---------------------------------------------------------------------------
titulo('PASO 2: el mismo pedido CON "stream": false')
cuerpo_unico = post({"model": MODELO, "messages": mensajes, "stream": False})
print(f"Ollama respondió {len(cuerpo_unico.strip().splitlines())} línea JSON:")
print("  ", json.loads(cuerpo_unico)["message"])

# ---------------------------------------------------------------------------
titulo("PASO 3: leer la respuesta del paso 1 como un único JSON (lo que hace modelito)")
try:
    json.loads(cuerpo)
    print("   Se pudo leer.")
except json.JSONDecodeError as error:
    print(f"   Falla: {error}")
    print("   modelito descarta este error y pasa a usar la línea de comandos.")

# ---------------------------------------------------------------------------
titulo("PASO 4: modelito con un mensaje system + uno user (como BatLLM)")

# Espiamos las funciones internas de modelito para ver qué hace realmente.
_json_post_original = modelito_ollama.json_post
_cli_original = modelito_ollama.run_ollama_command


def json_post_espia(url, payload, **kwargs):
    print(f"   [HTTP] POST {url}")
    print(f"          claves del pedido: {sorted(payload)}  "
          f"(¿'stream'? {'stream' in payload} | ¿'options'? {'options' in payload})")
    try:
        return _json_post_original(url, payload, **kwargs)
    except Exception as error:
        print(f"          -> falla: {type(error).__name__}: {str(error)[:70]}")
        raise


def cli_espia(*args, **kwargs):
    print(f"   [CLI]  ollama {' '.join(args[:-1])} {args[-1]!r}")
    proceso = _cli_original(*args, **kwargs)
    estado = "OK" if proceso.returncode == 0 else (proceso.stderr or "").strip()[:60]
    print(f"          -> {estado}")
    return proceso


modelito_ollama.json_post = json_post_espia
modelito_ollama.run_ollama_command = cli_espia

proveedor = OllamaProvider(host="http://localhost", port=11434, model=MODELO)
cliente = Client(provider=proveedor, model=MODELO)
respuesta = cliente.summarize(
    [
        Message(role="system", content="Respondé siempre con una sola palabra: PINGÜINO."),
        Message(role="user", content="Escribí la palabra canción."),
    ],
    settings={"temperature": 0},
)

titulo("RESULTADO")
print("Respuesta tal como la devuelve modelito (ascii muestra los caracteres ocultos):")
print("  ", ascii(respuesta))
print("¿Contiene códigos de control de la terminal (\\x1b)?", "\x1b" in respuesta)
print("¿Contiene acentos corruptos ('Ã' o 'Â')?", "Ã" in respuesta or "Â" in respuesta)
