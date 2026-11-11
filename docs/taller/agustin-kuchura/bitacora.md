# Bitácora - Agustín Kuchura

Registro individual del taller BatLLM (FING, 2026). Una entrada por sesión de trabajo significativa, agregada al final.

---

## 2026-10-20 - Clase 1 y puesta a punto de la instalación en Windows

**Tiempo y participantes:**
1 h 30 min - Clase
1 h 30 min - Lectura de la propuesta y guía de instalación. Individual.

**Contexto:** Windows. Python 3.13

**Trabajo:** leí la propuesta del taller y el contexto, y seguí la guía de instalación para Windows: Python 3.12 en paralelo con el 3.13, entorno virtual y dependencias. En clase se presentó el juego, la arquitectura y el flujo de trabajo (fork, discusión en clase, implementación, tests y PR) y se pidió una bitácora formal, con tiempo dedicado.

**Evidencia:** Asistencia a clase.

**Resultado:** entendí el flujo de contribuciones y la tarea de la semana (jugar, comparar configuraciones y recorrer el código). El juego todavía no corría correctamente: los problemas de instalación se resolvieron el 26/10.

**Reflexión:** la instalación en Windows tiene varios problemas (versión de Python, entornos fuera del repo).

**Siguiente paso:** crear el fork, clonarlo de cero con el entorno adentro y arrancar la app.

---

## 2026-10-26 - Instalación completa y primera partida de exploración

**Tiempo y participantes:**
2 h 20 min - Puesta a punto y recorridos de código
1 h 30 min - Primera partida y análisis. Total 3 h 50 min. Individual.

**Contexto:** fork Agus7kr/BatLLM creado el 26/10 desde krahd/BatLLM (main en d86ae05). BatLLM 0.3.6. Python 3.12.10, Ollama 0.40.11, llama3.2:3b corriendo 100% en GPU, num_ctx 4096. Partida: 2 rondas, 8 turnos, vida 30, daño 5, escudo de 70°, paso 0.03, Independent Models y Prompt Augmentation activados.

**Trabajo:** instalé y resolví problemas:
(1) Python 3.13 por defecto. Solución: 3.12 en paralelo y py -3.12 -m venv .venv_BatLLM.
(2) Un clon viejo con el entorno fuera del repo daba No module named 'kivy'. Solución: clon nuevo con el entorno adentro.
(3) OneDrive con "archivos a petición". Solución: "Mantener siempre en este dispositivo".
(4) Activate.ps1 no funciona en Git Bash. Solución: usar PowerShell.
(5) En 1920 por 1080 al 100% los botones de Settings quedan fuera de la ventana y no hay scroll. Solución: $env:KIVY_METRICS_DENSITY="0.8".
(6) Avisos [CRITICAL] [Clock] too much iteration en la pantalla History.
(7) El modelo por defecto smollm2 no estaba instalado. Solución: elegí llama3.2:3b en Ollama Config.
Después jugué dos rondas con prompts distintos para cada jugador.

**Evidencia:** sesión completa de la partida (las dos rondas) en docs/taller/agustin-kuchura/sesiones/2026-10-26-prueba1-completa.json (BatLLM 0.3.6). El detalle de la partida está en experimentos/partida-practica-2026-10-26.md. Prompt del jugador 1, ronda 1: pedía un solo comando, listaba los comandos (con un S2 inventado en lugar de S0) y describía una secuencia ("primero girar 90°, luego disparar, luego repetir: subir el escudo, bajar el escudo, disparar").

**Resultado:** ronda 1: el jugador 1 dio 8 ERR (respuestas crudas A90\nB, A180\nB, S1\nB...: dos comandos separados por salto de línea, que el parser rechaza) y no se movió. El jugador 2, con un prompt corto y sin explicar los comandos, respondió todo válido (A80.0, B seis veces), aunque los B no tuvieron efecto por el escudo arriba. Ronda 2: el jugador 1 dio 7 ERR y un A90 válido en el último turno. El jugador 2 giró en sentido contrario al pedido. Nadie perdió vida. Esperado: que el jugador 2 fallara más. Se observó lo contrario.

**Reflexión:**
(a) el juego ya le explica los comandos al modelo con su system prompt, así que listarlos en el prompt no hacía falta.
(b) El modelo no se entera de que una respuesta fue ERR: el historial guarda la respuesta cruda.
(c) El historial cruza las rondas y contamina.
(d) El juego no reparte una respuesta en varios turnos: cada turno es una consulta y el parser exige exactamente un comando.
(e) A resta grados en el rot que muestra el juego.
(f) El orden en que juegan los dos bots dentro de un turno se sortea. En esta partida jugaba primero el bot 2, y en las partidas del 09/11 jugaba primero el bot 1.
Con este modelo, describir una secuencia lleva a mandar el plan entero en cada respuesta.

**Siguiente paso:** recorrer el código del tramo 1 (del botón de enviar hasta la llamada a Ollama) y repetir el caso del ERR con condiciones controladas.

---

## 2026-10-27 - Recorrido de código: arranque y home_screen

**Tiempo y participantes:**
3 h - Recorrido de código. Individual, con Claude Code en VS Code. La clase del 27/10 se suspendió.

**Contexto:** fork al día con upstream en d86ae05 (incluye un cambio del 26/10 en src/game/ollama_connector.py).

**Trabajo:** recorrí el arranque (run_batllm.py, luego main.py y luego BatLLM(MDApp).build()) y home_screen (.py y .kv): cómo un botón del .kv llama a un método de Python.

**Evidencia:** Fork sincronizado con upstream en el commit d86ae05. Resumen de apuntes del recorrido:  la app arranca con run_batllm.py, que llama a main() y esta a BatLLM(MDApp).build(), que arma las pantallas. En home_screen.kv, el botón de enviar tiene un on_press que llama a un método de home_screen.py. 


**Resultado:** el camino de arranque y de la pantalla principal quedó entendido. Falta el tramo que va de home_screen hasta bot.submit_prompt_to_llm y el conector.

**Reflexión:** el .kv y el .py se conectan por on_press y por self.ids. El debugger ayuda mucho para seguir un recorrido que cruza hilos y el Clock de Kivy.

**Siguiente paso:** seguir el camino hasta _build_user_message.

---

## 2026-10-28 - Conceptos de LLM, paper y modelito

**Tiempo y participantes:**
2 h 45 min - Individual.

**Contexto:** lectura de docs/papers/BatLLM_URUCON2026_CameraReady_A2.pdf del repo de los profes y de modelito.

**Trabajo:** repasé tokens, ventana de contexto (num_ctx), roles (system, user, assistant), memoria (la lista de mensajes que arma el *harness*) y temperatura. Leí el paper (traza por turno, contrato, verificadores V1 a V4) y el rol de modelito como intermediario entre BatLLM y Ollama.

**Evidencia:** Resumen de mis apuntes: el modelo no recuerda nada por sí mismo, porque en cada llamada se reenvía la lista de mensajes con los roles system, user y assistant, y la ventana de contexto (num_ctx) limita cuántos tokens entran. El paper propone que cada turno deje una traza verificable, y modelito es el intermediario entre BatLLM y Ollama.

**Resultado:** el modelo no tiene memoria propia: la lista completa se reenvía en cada llamada. Surgieron tres ideas de contribución: avisar cuando el prompt se acerca a num_ctx, mejorar el system prompt y decidir qué tan permisivo debe ser el parser.

**Reflexión:** conviene separar lo que decide el jugador, el modelo y el código. El paper formaliza esa separación con trazas verificables.

**Siguiente paso:** comprobar en el código el armado del historial.

---

## 2026-11-03 - Recorrido 1 completo y clase 3

**Tiempo y participantes:**
3 h 30 min - Trabajo antes de la clase
1 h - Clase 3.

**Contexto:** main del fork al día con upstream. BatLLM 0.3.6.

**Trabajo:** completé el recorrido 1 (del botón de enviar a self.client.chat), la comunicación .kv ↔ .py y continué con los apuntes. En clase: cómo funciona un LLM (autorregresión, embeddings, atención, temperatura, contexto), Ollama y modelito, la organización del taller y el fork, y las tareas para el 10/11.

**Evidencia:** ejemplo real de un turno: el modelo recibió [GAME_STATE] + JSON + [PLAYER_INPUT] con "Respondé solo A100" y devolvió A100, que el parser aceptó. 
Resumen de mis apuntes sobre el recorrido completo: el prompt va del botón de enviar de home_screen.kv a home_screen.py, que lo pasa a game_board.py. Cuando los dos bots tienen su prompt, game_board.py agenda el turno con el Clock de Kivy. Después bot.py manda el trabajo a otro hilo y llama a ollama_connector.py, que arma la lista de mensajes (el system, el historial y un mensaje user con el estado del juego y el prompt) y llama a self.client.chat, que habla con Ollama a través de modelito. El modelo no tiene memoria: en cada turno se reenvía la lista completa.

**Resultado:** entendí el camino completo desde el prompt hasta la llamada al modelo. 

**Reflexión:** el ejemplo "bueno" (A100) sirve de caso base, pero es poco interesante para explicar. Los casos útiles son los que fallan.

**Siguiente paso:** preparar el fork del taller, revisar una respuesta de BatLLM y reproducir una observación.

---

## 2026-11-09 - Observación reproducible, preparación del entorno, revisión de una respuesta y estudio de las diapositivas sobre LLM
**Tiempo y participantes:** Total 7 h 25 min. Individual.
45 min - Organización del trabajo de la semana (lectura de mails y diapositivas, planificación)
1 h  - Tarea 2 (preparar el fork, los remotos y los chequeos)
4 h 40 min - Tareas 1 y 3 (revisar una respuesta de BatLLM y observación reproducible), pausas descontadas.
1 h - Estudio de las diapositivas del profe. 


**Contexto:** clon _FORKBATLLM, origin = Agus7kr/BatLLM, upstream = Taller-BatLLM/BatLLM, canonical = krahd/BatLLM (push deshabilitado). main = upstream/main = 5e3ed55. Python 3.12.10, modelito 1.4.8, Ollama 0.40.15, modelo llama3.2:3b (2.6 GB, 100% GPU, contexto 4096), temperatura sin configurar (default de Ollama). Lanzado con el debugger de VS Code y KIVY_METRICS_DENSITY=0.8. BatLLM 0.3.6.

**Trabajo:**
- *Tarea 2, preparación:* cambié upstream al repo del taller (reutilizando mi fork), agregué canonical, reinstalé las dependencias y corrí los chequeos de docs/CONTRIBUTING.md: python run_tests.py non-live (313 passed, 4 skipped), python tools/check_docs.py (OK) y python -m pip check (sin errores).
- *Tarea 3, observación reproducible* (el detalle está en experimentos/observacion-reproducible-1.md): jugué dos partidas con los mismos prompts y capturé las respuestas crudas, y en la segunda también la entrada real con un breakpoint en src/game/ollama_connector.py (línea 416, antes de self.client.chat).
- *Tarea 1, revisión de una respuesta* (turno 1 del bot 1, partida 2) y análisis del system prompt.

### Observación reproducible (tarea 3): varios comandos en una respuesta dan ERR
El documento completo, con pasos exactos, entorno, tablas por turno y límites, está en experimentos/observacion-reproducible-1.md, y las sesiones completas en docs/taller/agustin-kuchura/sesiones/. En resumen: en dos partidas con los mismos prompts (corrida 1 y corrida 2), el parser rechazó por varios comandos en una misma respuesta (ERR) los 16 turnos del jugador 1. El jugador 2 tuvo 7 ERR de 8 en la corrida 1 y 0 de 8 en la corrida 2.

### Revisión de una respuesta (tarea 1): turno 1 del bot 1, partida 2
- **Entrada disponible:** un mensaje system de 1446 caracteres (el texto del archivo src/assets/system_instructions/augmented_independent_1.txt) y un mensaje user con cuatro partes, una debajo de otra:

  1. La etiqueta [GAME_STATE].

  2. El estado del juego en JSON: {"bots":{"1":{"x":0.17551452454083177,"y":0.5749941518633832,"rot":199.10208164484297,"health":30,"shield":1},"2":{"x":0.4265433360621854,"y":0.16437706283629566,"rot":230.8656014093261,"health":30,"shield":1}},"current_turn":0,"current_round":1}

  3. La etiqueta [PLAYER_INPUT].

  4. El prompt del jugador 1, tal como figura arriba.

  El historial estaba vacío: la lista tenía solo esos dos mensajes.
- **Salida textual:** 'A66\nS\nB'.
- **Comando:** ERR.
- **Efecto:** ninguno (rot 199.10° y escudo ON antes y después).
- **Explicación:**
  - *Reglas:* el parser exige exactamente un comando. El modelo mandó tres, separados por saltos de línea, y se rechaza todo.
  - *Contexto:* el modelo entendió el contenido del pedido (girar, bajar el escudo, disparar) pero el system no le explica que cada respuesta es un turno ni cuántos turnos hay, ni qué significa cada campo del estado. Tampoco se le avisa del ERR: su respuesta cruda queda en el historial como assistant y la ve como precedente en los turnos siguientes.
  - *Decodificación:* la temperatura no está configurada y el resultado no es determinista: con el mismo texto, el jugador 2 dio 7 ERR de 8 en la corrida 1 y 0 de 8 en la 2.

**Evidencia (resto):** capturas de history con el debugger en turnos intermedios (largo 4, 8, 10 y 12): cada turno agrega un par user/assistant y la lista llega al tope de 16 mensajes (el doble de la cantidad de turnos) en el turno 8.

**Resultado:** observación reproducida con el jugador 1. Reproducción parcial con el jugador 2. Hallazgos sobre el system prompt:
(1) llega con [BULLET_DAMAGE] y [STEP_LENGTH] literales, sin reemplazar (verificado con '[BULLET_DAMAGE]' in history[0]['content'] devuelve True. Ningún .py del repo los sustituye).
(2) No explica los campos de [GAME_STATE] (por ejemplo, que shield: 1 es escudo arriba) ni cuántos turnos y rondas hay.
(3) No explica que cada respuesta es un turno.

**Reflexión:**
(a) si la primera respuesta es inválida, las siguientes tienden a conservar el formato, pero con 4 casos no lo puedo afirmar: como un ERR no cambia el estado, el mensaje user es casi idéntico turno a turno, y no se separa "copia su formato" de "misma entrada, misma salida".
(b) Mi hipótesis de que el modelo toma cada \n como un cambio de turno es coherente con el jugador 1, pero el jugador 2 de la corrida 1 pegó los comandos sin \n.
(c) No sé si el system prompt fijo es parte del diseño pedagógico del juego o es mejorable.

**Siguiente paso:** Diseñar un experimento con el mismo prompt, agregandole una explicación del protocolo de turnos en el system, contando los ERR. Probar también el prompt sin la línea en blanco.

---

## 2026-11-10 - Estudio de las diapositivas, documentos de experimentos y preparación de la entrega

**Tiempo y participantes:**
30 min - Estudio de las diapositivas 2 a 7
4h - Trabajo con Claude en la bitácora, los documentos de experimentos y la preparación y apertura del PR. Individual.

**Contexto:** el main de mi fork es igual a upstream/main (commit 5e3ed55), sin cambios del taller desde el 09/11. No había ningún PR abierto en el repositorio del taller. En mi clon creé la rama docs/primera-bitacora desde upstream/main.

**Trabajo:**

- Estudio de las diapositivas 2 a 7 (qué es un LLM, tokenización, embeddings, posición y capas), comparando con lo que ya había visto en BatLLM.
- Revisión y finalización del análisis de los experimentos anteriores (la partida del 26/10 y las dos partidas del 09/11) para terminar de documentar la observación reproducible: variables, estado inicial, respuestas por turno, cómo contar los ERR y qué no se evaluó.
- Armado de la bitácora y de la carpeta docs/taller/agustin-kuchura/ (bitacora.md, experimentos/ y sesiones/), con las tres sesiones guardadas.
- Acepté la invitación a la organización Taller BatLLM y quedé como miembro.
- Copia de la carpeta al clon, revisión del diff, commit y push de la rama docs/primera-bitacora a mi fork, y apertura del PR hacia Taller-BatLLM/BatLLM (rama main), sin mergearlo.

**Evidencia:** esta bitácora, experimentos/observacion-reproducible-1.md, experimentos/partida-practica-2026-10-26.md y las tres sesiones de la carpeta sesiones. 

**Resultado:** analicé la observación reproducible 1 y la dejé documentada en experimentos/observacion-reproducible-1.md, junto con la partida de práctica de la que surgió. El análisis apunta a posibles causas en el system prompt y en el historial, que quedan como hipótesis para probar en experimentos futuros. La bitácora, los dos documentos y las tres sesiones se entregan en el PR hacia Taller-BatLLM/BatLLM. El enlace al PR se entrega aparte. De las diapositivas quedó pendiente afianzar el concepto de activación y seguir desde la 8.

**Reflexión:** al preparar la explicación del turno de la corrida 2 vi que me faltaba entender mejor la decodificación, y por eso estudié las diapositivas. Todavía me cuesta el concepto de activación.

**Siguiente paso:** esperar la revisión y el consenso del grupo para integrar el PR, sin mergearlo yo. Retomar las diapositivas desde la 8.