"""
Tarea 0 — Prueba de concepto con Ollama.

Compara dos formas de conversar con un modelo:
  1 = sin memoria: en cada consulta se envía solo el último mensaje.
  2 = con memoria: en cada consulta se envía todo el historial + el último mensaje.

Permite elegir la biblioteca con la que se habla con Ollama:
  1 = modelito (la que usa BatLLM)
  2 = ollama   (la biblioteca oficial de Ollama para Python)

Al terminar, guarda en docs/taller/guillermo-mena/salidas/ un JSON con lo que se envió y recibió
en cada turno.
"""

import json
import time
from datetime import datetime
from pathlib import Path

import ollama
from modelito import Client, Message, OllamaProvider

# --- Configuración -----------------------------------------------------------

MODELO_POR_DEFECTO = "llama3.2:3b"
TEMPERATURA = 0  # 0 = respuestas casi deterministas (mejor para comparar)
HOST_OLLAMA = "http://localhost"
PUERTO_OLLAMA = 11434

# Carpeta donde se guardan los resultados: docs/taller/guillermo-mena/salidas
CARPETA_SALIDAS = Path(__file__).resolve().parents[1] / "salidas"


# --- Funciones auxiliares ------------------------------------------------------

def elegir_biblioteca() -> str:
    """Pide la biblioteca a usar. Enter = modelito."""
    opcion = input("Biblioteca — 1 = modelito, 2 = ollama (Enter = modelito): ").strip()
    while opcion not in ("", "1", "2"):
        opcion = input("Opción inválida. Ingresá 1 o 2: ").strip()
    return "ollama" if opcion == "2" else "modelito"


def elegir_modelo() -> str:
    """Pide el modelo a usar. Si el usuario solo aprieta Enter, usa el de por defecto."""
    modelo = input(f"Modelo (Enter = {MODELO_POR_DEFECTO}): ").strip()
    return modelo or MODELO_POR_DEFECTO


def elegir_modo() -> str:
    """Pide 1 o 2 hasta que la entrada sea válida."""
    modo = input("Modo — 1 = sin memoria, 2 = con memoria: ").strip()
    while modo not in ("1", "2"):
        modo = input("Opción inválida. Ingresá 1 o 2: ").strip()
    return modo


def consultar_con_modelito(cliente: Client, mensajes: list) -> dict:
    """Envía los mensajes con modelito, de la misma forma que lo hace BatLLM.

    modelito solo devuelve el texto de la respuesta: no informa tokens.
    """
    inicio = time.perf_counter()
    texto = cliente.summarize(
        [Message(role=m["role"], content=m["content"]) for m in mensajes],
        settings={"temperature": TEMPERATURA},
    )
    return {
        "respuesta": texto,
        "tokens_entrada": None,
        "tokens_salida": None,
        "duracion_segundos": round(time.perf_counter() - inicio, 2),
    }


def consultar_con_ollama(modelo: str, mensajes: list) -> dict:
    """Envía los mensajes con la biblioteca oficial de Ollama."""
    response = ollama.chat(
        model=modelo,
        messages=mensajes,
        options={"temperature": TEMPERATURA},
    )
    return {
        "respuesta": response.message.content,
        "tokens_entrada": response.prompt_eval_count,
        "tokens_salida": response.eval_count,
        "duracion_segundos": round((response.total_duration or 0) / 1e9, 2),
    }


def guardar_registro(biblioteca: str, modelo: str, modo: str, registro: list) -> None:
    """Guarda la conversación completa en un archivo JSON."""
    if not registro:
        print("No hubo turnos; no se guarda nada.")
        return

    CARPETA_SALIDAS.mkdir(parents=True, exist_ok=True)
    marca = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_modo = "sin-memoria" if modo == "1" else "con-memoria"
    nombre_modelo = modelo.replace(":", "-")  # ":" no es válido en nombres de archivo de Windows
    archivo = CARPETA_SALIDAS / f"tarea0_{marca}_{biblioteca}_{nombre_modo}_{nombre_modelo}.json"

    datos = {
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "biblioteca": biblioteca,
        "modelo": modelo,
        "modo": nombre_modo,
        "opciones": {"temperature": TEMPERATURA},
        "turnos": registro,
    }
    with open(archivo, "w", encoding="utf-8") as f:
        # ensure_ascii=False para que los acentos queden legibles
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"\nRegistro guardado en: {archivo}")


# --- Programa principal --------------------------------------------------------

def main() -> None:
    biblioteca = elegir_biblioteca()
    modelo = elegir_modelo()
    modo = elegir_modo()
    con_memoria = modo == "2"

    cliente_modelito = None
    if biblioteca == "modelito":
        proveedor = OllamaProvider(host=HOST_OLLAMA, port=PUERTO_OLLAMA, model=modelo)
        cliente_modelito = Client(provider=proveedor, model=modelo)

    print(f"\nBiblioteca: {biblioteca} | Modelo: {modelo} | "
          f"Modo: {'con' if con_memoria else 'sin'} memoria | Temperatura: {TEMPERATURA}")
    print("Escribí tus mensajes. Para terminar, escribí 'salir'.\n")

    historial = []  # Solo crece en el modo con memoria
    registro = []   # Lo que se guarda en el JSON, en ambos modos
    turno = 0

    try:
        while True:
            texto = input("Vos: ").strip()
            if texto.lower() == "salir":
                break
            if not texto:
                continue

            turno += 1
            mensaje_actual = {"role": "user", "content": texto}

            # --- La diferencia entre los dos experimentos está acá ---
            if con_memoria:
                a_enviar = historial + [mensaje_actual]  # todo lo anterior + lo nuevo
            else:
                a_enviar = [mensaje_actual]              # solo lo nuevo

            print(f"  [turno {turno}: se envían {len(a_enviar)} mensaje(s)]")

            try:
                if biblioteca == "modelito":
                    resultado = consultar_con_modelito(cliente_modelito, a_enviar)
                else:
                    resultado = consultar_con_ollama(modelo, a_enviar)
            except ConnectionError:
                print("  No se pudo conectar con Ollama. ¿Está corriendo? (probá 'ollama list')")
                break
            except ollama.ResponseError as error:
                print(f"  Ollama devolvió un error: {error.error}")
                break
            except Exception as error:  # modelito puede lanzar otros tipos de error
                print(f"  Error al consultar el modelo: {type(error).__name__}: {error}")
                break

            respuesta = resultado["respuesta"]
            print(f"Modelo: {respuesta}")
            if resultado["tokens_entrada"] is not None:
                print(f"  [tokens de entrada: {resultado['tokens_entrada']} | "
                      f"tokens de salida: {resultado['tokens_salida']}]")
            print(f"  [duración: {resultado['duracion_segundos']} s]\n")

            # En el modo con memoria, se agregan la pregunta y la respuesta al historial
            if con_memoria:
                historial.append(mensaje_actual)
                historial.append({"role": "assistant", "content": respuesta})

            registro.append({
                "turno": turno,
                "hora": datetime.now().isoformat(timespec="seconds"),
                "mensajes_enviados": a_enviar,
                **resultado,
            })
    except KeyboardInterrupt:
        # Ctrl+C también termina y guarda lo que haya
        print("\nInterrumpido.")
    finally:
        guardar_registro(biblioteca, modelo, modo, registro)


if __name__ == "__main__":
    main()
