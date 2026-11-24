# Game Analyzer — Sincronizar el árbol de turnos con el replay

**Problema y evidencia.** Al navegar con las flechas, Play o la barra inferior, el replay cambia de turno y el árbol sigue resaltando el último turno seleccionado desde el árbol.

Para reproducirlo, abrir la [corrida 2 del 09/11](../sesiones/2026-11-09-corrida2.json), seleccionar **Turn 3 start** en el árbol y retroceder un paso con la flecha del replay. La barra pasa a la última jugada del turno 2 y el árbol sigue resaltando el turno 3.

**Alcance.** Sincronizar el resaltado del árbol con el turno activo al navegar el replay.

**Resultado esperado.** Al repetir el ejemplo, el árbol resalta el turno 2. Al avanzar o retroceder con las flechas, usar Play o mover la barra, el resaltado acompaña el turno activo.

**Responsable, colaboradores y compañero revisor.** Agustín como responsable propuesto.

**Próximo paso.** Mostrar el caso en la reunión y acordar si conviene tratarlo por separado o incluirlo en un trabajo sobre la navegación del Game Analyzer.
