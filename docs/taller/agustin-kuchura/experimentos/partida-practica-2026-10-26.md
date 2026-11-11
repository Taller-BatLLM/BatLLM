# Partida de práctica del 2026-10-26

Autor: Agustín Kuchura. 
Primera partida de exploración, registrada en la bitácora (entrada del 2026-10-26). De esta partida sale la observación reproducible 1 (experimentos/observacion-reproducible-1.md).

## Pregunta

¿Cómo responde el modelo a prompts con instrucciones en secuencia, con y sin explicar los comandos válidos? Fue una exploración inicial, sin hipótesis cerradas.

## Entorno y configuración

- BatLLM 0.3.6, fork creado desde krahd/BatLLM (main en d86ae05).
- Ollama 0.40.11, modelo llama3.2:3b (100% en GPU, contexto 4096). La temperatura no se registró ese día.
- Windows, pantalla de 1920 por 1080 al 100%.
- Partida: 2 rondas, 8 turnos, vida 30, daño 5, escudo de 70° (los dos bots arrancan con el escudo levantado), paso 0.03, Independent Models y Prompt Augmentation activados.
- Estado inicial de la ronda 1: bot 1 en x 0.6127, y 0.6201, rot 223.55; bot 2 en x 0.1452, y 0.8601, rot 43.63. Los dos con escudo levantado y vida 30. En la ronda 2 las posiciones se mantienen y cada bot conserva el rot con el que terminó la ronda 1.

## Variables

Se cambiaron los prompts de los dos jugadores entre la ronda 1 y la ronda 2, así que la comparación entre rondas no aísla una sola variable. En la ronda 2 el historial de la ronda 1 seguía disponible para el modelo.

## Ronda 1

Prompt del jugador 1:

```
Tu respuesta debe ser un solo comando valido, sin ningun texto adicional.
Los comandos válidos son:
A<angulo>: girar en sentido antihorario, ej A90
S1: subir el escudo
S2: bajar el escudo
B: disparar

Lo que necesito que hagas es primero girar en sentido antihorario 90 grados. Luego disparar. Luego hasta que termine la ronda, repetir lo siguiente: subir el escudo, bajar el escudo, disparar.
```

Error en ese prompt: S2 no existe (bajar el escudo es S0) y no se listaron C, M ni S.

Prompt del jugador 2:

```
Respondé solamente utilizando comandos válidos. Primero girá en sentido antihorario 80 grados y luego dispará sin parar hasta que termine la ronda.
```

Expectativa: muchas instrucciones no se respetarían. Se esperaba que el jugador 2 fallara más, por tener menos detalles.

Resultado:

- Jugador 1: 8 ERR. Respuestas crudas, turno por turno: A90\nB, A180\nB, S1\nB, S2\nB, A180\nB, S1\nB, S2\nB, A180\nB. Son dos comandos separados por salto de línea, que el parser rechaza. No se movió.
- Jugador 2: A80.0, A80.0 y B seis veces, sin errores. Giró dos veces aunque se pidió una. Los B no tuvieron efecto porque tenía el escudo levantado. Nadie perdió vida.

Contra la expectativa: el jugador 2, sin explicación de los comandos, respondió todo válido, y el jugador 1, con explicación, falló en todos los turnos.

## Ronda 2

Prompt del jugador 1:

```
Respondé solo con un comando válido y nada más: ni texto, ni símbolos, ni saltos de línea.
Primero, rotá en sentido antihorario 90 grados.
Segundo, bajá el escudo.
Tercero, dispará.
Después, hasta que termine la ronda, repetí la secuencia: subí el escudo, bajá el escudo, dispará.
```

Prompt del jugador 2:

```
Girá en sentido horario hasta quedar apuntando al otro jugador. Después bajá el escudo y disparà sin parar hasta que termine la ronda.
```

Expectativa: el jugador 2 no iba a saber apuntar al otro jugador, y al jugador 1 le sería difícil mejorar por el historial de la ronda anterior.

Resultado:

- Jugador 1: 7 ERR y un A90 válido en el último turno (rot de 223.5° a 133.5°). Respuestas de varios comandos cada vez más largas, por ejemplo A90\nS2\nB\nS1\nB\nS2\nB y A90\nB\nS1\nB\nS1\nB.
- Jugador 2: A80.0, S0, B cinco veces y S0. Giró en sentido antihorario aunque se pidió horario, igual que en la ronda 1. Bajó el escudo y disparó, pero sin apuntar: nadie perdió vida.
- Al terminar la ronda 2 terminó la partida y arrancó otra sola, con posiciones nuevas.

## Observaciones

1. El juego ya le explica los comandos al modelo en su system prompt (src/assets/system_instructions/), por eso el jugador 2 los conocía sin que se los dijeran.
2. El modelo no se entera de que una respuesta fue ERR: el historial guarda la respuesta cruda y no avisa del error.
3. El historial cruza las rondas: es una ventana de 16 mensajes (el doble de los turnos), así que al empezar la ronda 2 el modelo todavía ve casi toda la ronda 1. En la ronda 2 el jugador 1 usó S2, que solo estaba en el prompt de la ronda 1.
4. El juego no reparte una respuesta en varios turnos: cada turno es una consulta separada y el parser exige exactamente un comando.
5. El comando A (antihorario) resta grados en el rot que muestra el juego.

## Interpretación provisional

- Con este modelo, describir una secuencia lleva a que mande todo el plan junto en cada respuesta, aunque se le pida un solo comando.
- La instrucción "ni saltos de línea" no alcanzó para corregirlo, posiblemente porque el historial le mostraba sus propias respuestas con ese formato.
- Que el jugador 1 respondiera bien en el último turno puede ser azar o que ya no quedaran mensajes de la ronda 1 en la ventana. No se sabe.

## Límites y qué no se evaluó

Una sola partida de dos rondas, un solo modelo, sin repeticiones y con dos variables cambiadas entre rondas. No se evaluaron otras temperaturas, otros modelos, el historial compartido ni la opción de Prompt Augmentation desactivada. Esta partida motivó la observación reproducible 1, que repite la situación con condiciones más controladas.

## Evidencia

Sesión completa (las dos rondas): docs/taller/agustin-kuchura/sesiones/2026-10-26-prueba1-completa.json (BatLLM 0.3.6). Este documento solo resume lo que contiene.
