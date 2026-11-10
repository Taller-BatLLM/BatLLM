# Bitácora — Módulo de Taller BatLLM

Registro de trabajo del módulo de taller *"Desarrollo y evaluación de BatLLM: una plataforma lúdica para alfabetización en inteligencia artificial"* (InCo – FING / CU Boulder).

## Enlaces

- Repositorio original: https://github.com/krahd/BatLLM
- Repositorio del taller: https://github.com/Taller-BatLLM/BatLLM
- Mi fork: https://github.com/guixe16/BatLLM
- Hasta el 2026-11-02 esta documentación estuvo en https://github.com/guixe16/Documentos_BatLLM; desde el 2026-11-09 vive en esta carpeta.

## Estructura

| Ruta | Contenido |
| --- | --- |
| [bitacora.md](bitacora.md) | Registro cronológico: una entrada por sesión de trabajo, con tiempos y participantes. |
| [experimentos/](experimentos/) | Un archivo por experimento o prueba documentada. Partir de [la plantilla](experimentos/_plantilla-experimento.md). |
| [salidas/](salidas/) | Salidas crudas: JSON con los mensajes enviados y las respuestas, logs, capturas. |
| [sesiones/](sesiones/) | Sesiones guardadas de BatLLM, copiadas desde `BATLLM_HOME`. |
| [recorrido-codigo.md](recorrido-codigo.md) | Notas del recorrido de código asignado (tarea 2). |
| [errores/propuestas.md](errores/propuestas.md) | Problemas encontrados e ideas de contribución (tarea 5). |
| [scripts/](scripts/) | Scripts propios: prueba de concepto con Ollama (tarea 0), reproducción del error de modelito y prueba de escritura en Kivy. |

## Convenciones

- Anotar la hora de inicio y de fin **en el momento**, no reconstruirla después.
- Nombrar los experimentos como `AAAA-MM-DD-descripcion-corta.md`.
- Registrar siempre: versión del código (commit), modelo, configuración y condición de contexto.
- Separar **lo observado** de **la interpretación**.
- Conservar los casos fallidos y los que no apoyan la hipótesis.
- Hacer commit al terminar cada sesión de trabajo.
