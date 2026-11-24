# Psicología de edición viral (1–3 min)

Sacado de los 3 videos de flujo (reels premium, podcast premium, talking head minimal).

## Las 5 claves de un short premium
1. **Captions**: tercio inferior con blur/oscuro; 2 fuentes; primero se colocan 1–2 palabras especiales al centro, luego el resto rellena huecos; animación pop + blur + fade.
2. **Listicles UI**: si el video es por capítulos, mostrar los N capítulos temprano y reusar el ícono al entrar a cada uno.
3. **UI pops y contadores**: antes/después con flecha, notificación con logo (software/evento/dinero), anillo contador para cifras, cuadro con lista.
4. **Hook = speaker + texto + visual**: ojos en tercio superior; texto = la razón para quedarse; visual que la apoya.
5. **Animaciones fullscreen** (~50 % del edit): timeline/listas, escena de un elemento, texto fullscreen contrastado, zoom fuera del A-roll.

## Reglas de ritmo
- A-roll para transiciones y descanso. B-roll para emoción y personajes. Animación para valor.
- Nunca > `max_aroll_streak_s` sin estímulo visual (lo valida `ves.py validate`).
- Romper patrón: tracking + desaturación + reverb en la frase de "problema".
- Primer borrador = 60–70 %. Siempre 1–2 rondas de revisión humana.

## Clips de podcast (cómo elegir el clip)
- Empieza con la **pregunta del entrevistador**, sigue con la respuesta del invitado, termina en una conclusión.
- Respuesta concisa: entrega valor o cuenta una historia; elimina rodeos.
- Cambia de ángulo cada pocas frases. Presenta al invitado con lower-third.

## Flujo humano + IA (lo que realmente da calidad)
Raw → corte (silencios + malas tomas, 30 ms de padding) → **plan humano (15 min)** → construcción por IA → revisión → sound design (cue sheet) → música → master.
La IA no planifica sola: "deja que la IA haga el trabajo pesado, no el creativo".
