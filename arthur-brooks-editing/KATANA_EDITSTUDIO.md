# Higgsfield Katana + Edit Studio dentro de la skill

## 0. Regla número uno: no se genera nada
**La skill nunca genera imágenes, video, voz ni música con herramientas de pago** (Higgsfield, Katana, edit-gen, Seedance,
Soul, etc.). Siempre:
1. Escribe los **prompts** de todo lo que falta (con la estructura de Katana de la sección 3).
2. Tú generas y entregas un **zip** con los nombres de archivo de la lista.
3. La skill lo ingiere (`assetpack.py --ingest`), lo recorta, le aplica el color de marca y lo usa.

Katana y edit-gen se usan **solo como método**: cómo analizan, planifican, escriben prompts y verifican. Sus pasos de
generación, sus créditos y su modo «autónomo sin preguntar» quedan **desactivados**. Prevalecen nuestras 3 pausas
(plan → assets → vista previa).

## 1. Qué es cada cosa
| | Qué es | Qué trae que nos sirve | Qué NO usamos |
|---|---|---|---|
| **Katana** (flujo de Higgsfield) | Rehace un video de referencia con tu sujeto: analiza cada fotograma, planifica, genera escenas nuevas y monta | Lectura fotograma a fotograma con mapa de energía; contrato de bloqueos y libertades; roles de toma; **prompts en 7 bloques con una función por referencia**; lugares vacíos reutilizables; 3 revisiones de movimiento; control de calidad (lógica cada 0.5 s, sin fotogramas repetidos) | La generación con Seedance/Soul, el gasto de créditos y el modo sin pausas |
| **Edit Studio** (plugin `edit-studio`) | Edición en código (Python + ffmpeg) con 3 skills: director, voz y generación | **Biblioteca de 268 movimientos** (`moves/*.yaml`: zoom, whip, crash, speed ramp, freeze, flash…); **15 géneros** con estructura y ritmo (fashion, ugc, product, explainer, viral…); presets de estilo por palabras; ediciones puntuales por voz («crash zoom en 0:07», «whip entre #4 y #5»); vista previa con clips numerados; versiones que no se repiten; medir un efecto de un clip de ejemplo; QA medido (cortes en el beat, LUFS) | `edit-gen` (de pago) y descargar de YouTube o TikTok |

Va incluido en `plugins/edit-studio/`. Las instrucciones de Katana (método) están en `docs/katana/`.

## 2. Reglas generales que adopta la skill (todas las ediciones)
1. **Plan en 5 líneas antes de trabajar** (Edit Studio): partes en orden, puntos de corte (tiempos o palabras citadas), duración, formato y estilo. Luego se ejecuta.
2. **Contrato de bloqueos y libertades** (Katana): `analysis/task-contract.json` con lo que NO puede cambiar (la prenda, la palabra del CTA, la canción…) y lo que es libre. Cada pedido tuyo es un bloqueo.
3. **Analizar la referencia entera** (Katana): todos los fotogramas, notas por segundo, cortes corregidos a mano, y un **mapa de energía**: cuántos cortes, flashes, sacudidas, movimientos de cámara y golpes por segundo. **La edición nueva repite esas tasas.** Si baja la energía, el video se siente plano.
4. **Roles de toma** (Katana): cada escena tiene una función: gancho, contexto, héroe, acción, detalle, contraste, revelación, clímax, pausa o remate. El concepto lleva planteamiento y remate.
5. **Ritmo por género** (Edit Studio): para moda se aplica `genres/fashion.md` (gancho tipo portada de revista, detalles de tela, un cambio de look por beat, flash de foto con congelado). Para UGC y producto, sus géneros. Se combinan con el formato Arthur, que manda.
6. **Movimientos con nombre** (Edit Studio): las transiciones y efectos se eligen de `moves/` (`find_move.py crash zoom`), respetando los permitidos y prohibidos de cada género y de cada formato Arthur.
7. **Prompts de assets en 7 bloques** (Katana, sección 3), con la referencia de identidad y ropa siempre primero.
8. **Lugares vacíos** (Katana): cada lugar que aparezca en varias tomas generadas tiene un «plate» propio **sin personas** (tipo `location`), que se reutiliza en todas sus tomas. Así el fondo no cambia entre tomas.
9. **La ropa del hero está bloqueada**: en todas las tomas lleva exactamente la prenda de tu foto. Nunca la del video de referencia ni una inventada.
10. **Duración a generar = el doble de lo que sale en pantalla** (mín. 4 s; Seedance: Σ por toma de clamp(2 × segundos en pantalla, 2, 4)). Así se elige el mejor tramo.
11. **Nunca se retocan caras con código**: ni pegar, ni deformar, ni «embellecer». Si una cara sale mal, se pide otra generación (prompt nuevo) o se usa otra toma.
12. **3 revisiones de movimiento** (Katana), antes de renderizar y sobre el borrador: (1) tiempo y ritmo; (2) movimiento en el espacio y continuidad entre cortes (dirección, escala); (3) detalle y pulido (energía, easing, tipografía, acentos de sonido).
13. **Control de calidad del material que entregas** (Katana): un fotograma cada 0.5 s de cada video generado. Se revisan manos, objetos que se funden, identidad, ropa y texto parásito, y se usa solo el tramo limpio.
14. **Ediciones puntuales por voz** (Edit Studio): «#5» (el número del clip en la vista previa), «0:07» o «donde dice …» + qué hacer («crash zoom», «whip», «quita», «más fuerte»).
15. **Versiones que no se repiten** (Edit Studio): una segunda versión evita las transiciones, movimientos y tomas de la anterior.
16. **Sonido de bibliotecas reales** (Katana/Edit Studio): música y efectos grabados (Mixkit, YouTube Audio Library, CC0). Nunca sintetizados por código.

## 3. Prompts de assets en 7 bloques (Katana)
Cada prompt de imagen o video incluye solo los bloques que aclaran la toma:

| # | Bloque | Qué escribir | Ejemplo |
|---|---|---|---|
| 1 | **Función de cada referencia** | Qué controla cada imagen adjunta, en orden | `@image1` = A01 (diseño exacto de la blusa) · `@image2` = A02 (identidad de la modelo) · `@image3` = L01 (lugar vacío) |
| 2 | **Contexto** (opcional) | Qué pasó antes y su huella; estado inicial → estado final | «acaba de abrir la caja; la blusa sale doblada → la sostiene frente al espejo» |
| 3 | **Mapa espacial** | Primer plano, plano medio y fondo; posiciones; dirección del movimiento | «ella a la izquierda en plano medio, ventana al fondo a la derecha» |
| 4 | **Una sola acción clara** | Un cambio de estado por toma | «gira ¼ hacia la ventana» |
| 5 | **Cámara** | Encuadre y ángulo; si se mueve: un movimiento, su dosis y su límite | «push-in lento del 5 %, termina antes de cortar la cabeza» |
| 6 | **Luz y textura** | La gramática visual elegida + luz motivada | «luz dorada de ventana, satén con brillo real, grano fino» |
| 7 | **Bloqueos finales** | Identidad, la ropa de tu foto, sin texto, continuidad | «lleva exactamente la blusa de @image1 en toda la toma; sin texto ni logos» |

Más la ficha técnica: formato (más cercano soportado) y resolución, duración a generar, negativo, nombre de archivo y zip.
`pipeline/assetpack.py` ya añade solo los bloques 1 y 7, la función de cada referencia y la duración a generar.

## 4. El plus, en concreto
| Antes | Ahora |
|---|---|
| Prompts sueltos: la blusa podía cambiar de color entre tomas | Cada referencia controla una sola cosa y la ropa está bloqueada en todas las tomas |
| Fondos distintos en cada toma generada | Un lugar vacío reutilizable por cada sitio |
| La energía se elegía a ojo | Se mide la de la referencia (cortes, flashes y movimientos por segundo) y se iguala |
| Transiciones de una lista corta | 268 movimientos con nombre, filtrados por género |
| Revisión general | 3 revisiones de movimiento + control cada 0.5 s del material generado |
| «Cámbialo» | Ediciones puntuales con #clip, tiempo o palabra |
