# Observación reproducible 1: varios comandos en una respuesta dan ERR

Autor: Agustín Kuchura. 
Observación del 2026-11-09, registrada en la bitácora (entrada del 2026-11-09). Este archivo registra la primera observación. 

## Origen

Esta observación nace de una partida de práctica anterior (2026-10-26), en la que el modelo respondía varios comandos válidos encadenados con saltos de línea en una misma respuesta (por ejemplo A90\nB) y el parser la rechazaba (ERR). Se repitió la misma situación para comprobar si había sido casualidad o si señalaba un problema del sistema. El detalle de esa partida está en experimentos/partida-practica-2026-10-26.md y su sesión completa en docs/taller/agustin-kuchura/sesiones/2026-10-26-prueba1-completa.json.

## Pregunta

¿El modelo responde a veces varios comandos en una misma respuesta, aunque se le pida un solo comando por respuesta?

## Entorno

- BatLLM 0.3.6, commit 5e3ed55 (main de upstream), modelito 1.4.8.
- Ollama 0.40.15, modelo llama3.2:3b (2.6 GB, 100% GPU, contexto 4096), temperatura sin configurar (default de Ollama).
- Windows, lanzado con el debugger de VS Code y KIVY_METRICS_DENSITY=0.8.
- Configuración de la partida: 2 rondas, 8 turnos, vida 30, daño 5, escudo 70° (empieza levantado), paso 0.03, Independent Models y Prompt Augmentation activados.

## Variables

- **Fijas en las dos partidas:** versión, modelo, temperatura, configuración de la partida y el texto de los dos prompts.
- **Lo que cambia entre una partida y otra:** las posiciones y ángulos iniciales de los bots (BatLLM los sortea en cada partida) y la respuesta del modelo, que no es determinista.
- **Condición manipulada a propósito:** ninguna. Es una repetición de la misma condición, no una comparación entre condiciones.

## Estado inicial

Valores de la sesión guardada (rot en grados). En las dos partidas los dos bots arrancan con el escudo levantado y vida 30.

| | Bot 1 (x, y, rot) | Bot 2 (x, y, rot) |
| --- | --- | --- |
| Corrida 1 | 0.2006, 0.1101, 71.09 | 0.9433, 0.1567, 121.21 |
| Corrida 2 | 0.1755, 0.5750, 199.10 | 0.4265, 0.1644, 230.87 |

## Esperado y observado

- **Esperado:** una respuesta con un solo comando por turno. El system prompt pide "strictly a command" y la guía (docs/USER_GUIDE.md) dice "exactly one recognised command".
- **Observado:** el modelo devuelve el plan entero, varios comandos juntos, y el parser rechaza la respuesta (ERR). El bot no cambia de estado.

## Pasos exactos

1. python run_batllm.py (en 1920 por 1080 al 100%, con $env:KIVY_METRICS_DENSITY="0.8" para ver los botones de Settings).
2. En Settings, en Ollama Config, elegir llama3.2:3b. Config: 2 rondas, 8 turnos, vida 30, daño 5, escudo 70°, paso 0.03, Independent Models y Prompt Augmentation activados.
3. Pegar estos prompts (uno por jugador) y dar Submit. Jugador 1:

   ```
   Tu respuesta debe ser un solo comando valido, sin ningun texto adicional.

   Lo que necesito que hagas es primero girar en sentido antihorario 66 grados. Luego bajar el escudo y disparar. Luego hasta que termine la ronda, repetir lo siguiente: subir el escudo, bajar el escudo, disparar.
   ```

   Jugador 2:

   ```
   Tu respuesta debe ser un solo comando valido, sin ningun texto adicional.

   Lo que necesito que hagas es primero girar en sentido horario 60 grados. Luego bajar el escudo y disparar. Luego hasta que termine la ronda, repetir lo siguiente: subir el escudo, bajar el escudo, disparar.
   ```
4. Dejar correr la ronda 1 (8 turnos), abrir History y guardar la sesión.

## Cómo contar los ERR y qué esperar

- En el panel Commands de cada jugador aparece, turno por turno, el comando que interpretó el parser. Los ERR se ven en rojo.
- En History, cada turno muestra la respuesta cruda del modelo (llm response) y el comando (cmd). Ahí se ve si el ERR fue por varios comandos en una sola respuesta.
- El resultado no es determinista. En nuestras dos partidas el jugador 1 dio ERR en todos los turnos, y el jugador 2 varió (7 de 8 en la primera, 0 de 8 en la segunda).
- Consideramos reproducida la observación si, en una partida, el jugador 1 da ERR en la mayoría de los turnos con respuestas de varios comandos.

## Resultado

Dos corridas, es decir, dos partidas diferentes con historial limpio. Las posiciones iniciales cambian en cada partida.

| | Corrida 1 | Corrida 2 |
| --- | --- | --- |
| Jugador 1, turnos con ERR | 8 de 8 | 8 de 8 |
| Jugador 2, turnos con ERR | 7 de 8 | 0 de 8 |

Respuestas crudas, turno por turno (entre paréntesis, lo que interpretó el parser):

| Turno | Corrida 1, jugador 1 | Corrida 1, jugador 2 | Corrida 2, jugador 1 | Corrida 2, jugador 2 |
| --- | --- | --- | --- | --- |
| 1 | A66\nS\nB\nS\nB (ERR) | A60S1B (ERR) | A66\nS\nB (ERR) | A60 (válido) |
| 2 | A66\nS\nB\nS\nB (ERR) | A60S1B (ERR) | A66\nS\nB\nS\nB (ERR) | B (válido) |
| 3 | A66\nS\nB\nS\nB (ERR) | S0B (ERR) | A66\nS\nB (ERR) | S0 (válido) |
| 4 | A66\nS\nB\nS\nB (ERR) | S0B (ERR) | A66\nS\nB\nS\nB (ERR) | S (válido) |
| 5 | A66\nS\nB (ERR) | S0B (ERR) | A66\nS\nB\nS\nB (ERR) | S (válido) |
| 6 | A66\nS\nB (ERR) | A60 (válido) | A66\nS\nB\nS\nB (ERR) | B (válido) |
| 7 | A66\nS\nB (ERR) | S0B (ERR) | A66\nS\nB\nS\nB (ERR) | S0 (válido) |
| 8 | A66\nS\nB (ERR) | S0B (ERR) | A66\nS\nB\nS\nB (ERR) | S (válido) |

- Jugador 1: siempre varios comandos separados por salto de línea, y nunca se movió.
- Jugador 2, corrida 1: comandos pegados, sin separador (A60S1B, S0B).
- Jugador 2, corrida 2: todos válidos. Pidió horario 60 y el modelo respondió A60 (antihorario).

## Límites

Dos corridas, un solo modelo, temperatura por defecto, posiciones distintas en cada partida. El jugador 1 reproduce de forma consistente (16 de 16), el jugador 2 no.

## Qué no se evaluó

- Otros modelos, otros tamaños de modelo y otras temperaturas.
- Historial compartido entre los jugadores, o la opción de Prompt Augmentation desactivada.
- Otros prompts: por ejemplo, listando o no los comandos, o dando reglas según el estado en lugar de una secuencia.
- Cambios en el system prompt, por ejemplo explicar que cada respuesta es un turno.
- La ronda 2 y más de dos repeticiones.

Esta primera observación buscó repetir la misma condición lo más parecida posible para comprobar si el fenómeno se reproduce. Los cambios de condición quedan para experimentos futuros.

## Evidencia

Sesiones completas de las dos corridas, en docs/taller/agustin-kuchura/sesiones/: 2026-11-09-corrida1.json y 2026-11-09-corrida2.json (BatLLM 0.3.6). Las tablas de este documento muestran solo un resumen de lo que contienen.
