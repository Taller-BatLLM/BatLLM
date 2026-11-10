# Bitácora de trabajo

Una fila por sesión de trabajo, de la más antigua a la más reciente. Los detalles que no entran en la tabla (comandos, versiones, dificultades) están en [Notas por sesión](#notas-por-sesión).

**Total acumulado:** _12 h 50 min_ (actualizar en cada entrada)

| Fecha | Horas | Qué se hizo | Dudas |
| --- | --- | --- | --- |
| 2026-10-21 | 1 h 30 min<br>(19:30–21:00) | **Tareas 0 y 1.** Cloné `krahd/BatLLM`, creé el fork y configuré los remotes. Creé el entorno virtual con Python 3.12.10 e instalé las dependencias. Corrí los tests sin Ollama sobre `645189b`: 192 pasan, 2 se omiten, 1 falla ([propuesta 1](errores/propuestas.md)). Instalé Ollama 0.40.8 y descargué `smollm2`, `llama3.2:3b` y `qwen2.5:7b`. | Ninguna |
| 2026-10-22 | 2 h<br>(9:00–11:00) | **Tarea 0.** Creé [`scriptOllama.py`](scripts/scriptOllama.py) (con asistencia de IA) y probé `llama3.2:3b` sin memoria y con memoria, a temperatura 0 ([experimento](experimentos/2026-10-22-tarea0-memoria.md)). Sin memoria el modelo no recordó el nombre; con memoria, sí. Los tokens de entrada crecieron 38 → 110 → 178 → 347 en 4 turnos. Repasé tokens, ventana de contexto, roles, temperatura y la plantilla de chat del modelo. | ¿La mención a la fecha de corte viene de la plantilla o del entrenamiento del modelo? |
| 2026-10-24 | 1 h 30 min<br>(9:00–10:30) | **Tareas 0 y 1.** Actualicé modelito a la 1.4.6 (BatLLM seguía usando la 1.4.5). Leí el paper. | — |
| 2026-10-26 | 4 h 30 min<br>(19:00–23:30) | **Tareas 1, 2 y 4.** Jugué BatLLM y documenté las partidas ([experimento](experimentos/2026-10-26-primera-partida.md), [sesiones guardadas](sesiones/)). Empecé el recorrido del código. | — |
| 2026-10-26 | 1 h 15 min<br>(23:30–00:45) | **Tarea 2.** Completé la tabla del [recorrido 3](recorrido-codigo.md) (`HistoryManager` → Game Analyzer, commit `d86ae05`) y escribí el ejemplo de la jugada `A` → `ERR`. Creé el repositorio `guixe16/Documentos_BatLLM` y subí la bitácora. | — |
| 2026-11-01 | 1 h 45 min<br>(14:45–16:30) | **Tareas 1 y 5.** Actualicé BatLLM al commit `b8a7b91` (modelito 1.4.8). Tests sin Ollama: 312 pasan, 4 se omiten. Medí el problema de la pantalla Settings (con asistencia de IA): el contenido mide 1255 px y la ventana 1009 px, así que la barra de botones queda casi oculta ([propuesta 3](errores/propuestas.md)). | — |
| 2026-11-02 | 20 min<br>(17:40–18:00) | **Tareas 3 y 4.** Revisé qué faltaba para la clase, corregí fechas, tareas y total de la bitácora, y escribí la hipótesis del experimento de la primera partida. | Coordinar con los compañeros qué recorrido cubre cada uno. |

## Notas por sesión

### 2026-10-21

- Remotes: `origin` → fork, `upstream` → original.
- Dependencias instaladas: Kivy 2.3.1, kivymd 1.2.0, modelito 1.4.5, ollama 0.6.3.
- Test que falla: `test_shipped_llm_config_uses_smollm2_first_install_defaults`.
- Hardware: NVIDIA RTX 4060 (8 GB de VRAM), 16 GB de RAM.
- Dificultades:
  - En Windows, `python` abre el alias de la Microsoft Store; se usa `py -3.12` para crear el venv.
  - `python run_tests.py non-live` se detiene en el primer test que falla y no corre el resto; la suite completa se corrió con `pytest` directamente.
  - Al ejecutar `ollama` sin argumentos se abre un menú para conectar integraciones (Claude Code, Codex, VS Code…). No hace falta para BatLLM; se sale con `Esc`.
- Al probar la conexión con Ollama, le mandé al modelo "Hola, ¿quién sos?" y respondió: "¡Hola! Me llamo Luna, pero puedo responder a preguntas y proporcionar información sobre una amplia variedad de temas. Soy un modelo de inteligencia artificial, diseñado para ayudar y aprender contigo. ¿En qué puedo ayudarte hoy?"

### 2026-10-22

- El script estaba originalmente en `Taller/Script Ollama/`.
- Salidas crudas: [sin memoria](salidas/tarea0_2026-10-22_16-39-51_sin-memoria_llama3.2-3b.json), [con memoria](salidas/tarea0_2026-10-22_16-41-52_con-memoria_llama3.2-3b.json).
- La plantilla de chat (`ollama show llama3.2:3b --template`) convierte la lista de mensajes en un único texto con marcas de rol, y agrega siempre un bloque `system` con `Cutting Knowledge Date: December 2023`.
- Dificultades:
  - La biblioteca `ollama` no está instalada en el Python global; el script se ejecuta con el Python del venv de BatLLM (activándolo con `Activate.ps1`).
  - La ruta `Taller\Script Ollama` tiene un espacio, así que hay que escribirla entre comillas en la terminal.
- Pendiente: repetir las pruebas con `smollm2` y `qwen2.5:7b`, con mensajes idénticos en ambos modos; (opcional) hacer lo mismo con modelito.

### 2026-11-01

- Comando de los tests: `PYTHONPATH=src KIVY_WINDOW=mock .venv_BatLLM/Scripts/python.exe -m pytest -q src/tests`.
- El error de Settings sigue presente en `b8a7b91`.
