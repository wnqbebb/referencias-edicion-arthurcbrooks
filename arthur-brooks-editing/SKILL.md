---
name: arthur-brooks-editing
description: Edita videos verticales cortos (30 s–3 min) en el estilo premium minimal de Arthur Brooks, con el método de Joseph (Ultimate Editors) — plan por beats con 3 diseños A/B/C sacados de 339 animaciones reales de Arthur, subtítulos con la regla del 75 %, 10 principios de diseño, animaciones sincronizadas a la palabra (gráficos, líneas, citas, ilustraciones, pinturas, b-roll), cortes fluidos, paleta por video, prompts de assets y diseño sonoro. Úsala para planificar, construir, revisar y entregar ediciones en este estilo con cualquier modelo (Claude, ChatGPT, Gemini).
---

# Skill de edición · estilo Arthur Brooks (método Joseph)

> **Antes de nada lee `REGLAS_GENERALES.md`**: 32 reglas obligatorias (pausas, no generar, Joseph, subtítulos, fluidez, prompts de 7 bloques, sonido, QA) y las herramientas que siempre van incluidas (plugin Edit Studio de Higgsfield, método Katana, Remotion, HyperFrames, Playwright).

Esta skill es **independiente del modelo**: Claude, ChatGPT y Gemini producen el mismo video porque el estilo vive en
estas reglas, en la biblioteca de referencias y en el código del render, no en el gusto del modelo.
**Tú no diseñas desde cero: eliges de la biblioteca, rellenas el contrato (`beats.json` → `edit_plan.json`) y el render
hace el resto.**

## 0. Qué hay en el paquete
| Carpeta / archivo | Qué es | Cuándo se usa |
|---|---|---|
| `SKILL.md` (este) | Reglas y flujo completo | Siempre, primero |
| `PROMPTS.md` | Prompts listos para copiar en cada etapa | Al operar la skill |
| `MODELOS.md` | Cómo instalarla en Claude, ChatGPT y Gemini | Al instalar |
| `HERRAMIENTAS.md` | Lo necesario: MCP Playwright, Remotion, HyperFrames, Edit Studio, ffmpeg; dónde buscar pinturas/b-roll/música/SFX | Al instalar y al buscar material |
| `CREAR_ESTILO_NUEVO.md` | Cómo crear otro estilo de edición (otro creador) con rea-video + el método de esta skill | Cuando quieras un estilo nuevo |
| `KATANA_EDITSTUDIO.md` + `docs/katana/` + `plugins/edit-studio/` | Método Katana (análisis con mapa de energía, prompts en 7 bloques, lugares vacíos, 3 revisiones, QA) y plugin Edit Studio (268 movimientos, 15 géneros, ediciones por voz) | Siempre: son reglas generales |
| `docs/JOSEPH_METODO.md` | Los 10 principios + cómo se entrena y se usa (fuente: video de Joseph, 21 min) | Siempre |
| `docs/RULEBOOK.md` | Desglose de cada principio con ejemplos reales (diseño, efectos, animación, porqué) | Al diseñar una escena |
| `docs/EDIT_LOGIC.md` | Qué elemento poner según lo que se dice, sincronía, transiciones por formato, ritmo, sonido | Al planificar |
| `docs/FORMATOS.md` + `docs/ANATOMIA_v01_my_life.md` | Los 5 formatos de Arthur y la referencia maestra | Al elegir formato |
| `docs/tecnicas-editor.md`, `principios-diseno.md`, `psicologia.md` | Técnicas generales de edición viral | Siempre (generales a todos los videos) |
| `ANIMACIONES.md` + `library/` | **339 animaciones** de Arthur con ID `VNN-ANN`, hoja de 5 keyframes (`.jpg`) y ficha (`.md`) | Para recomendar diseños A/B/C |
| `references/vNN/` | Los 20 videos desglosados: escenas, lógica, transcripción, `.srt`, hojas de estudio | Para justificar «visto en los reels» |
| `panel/` | **Panel de planificación por beats** (HTML) | STOP 1 |
| `EJEMPLOS.md` + `examples/` | 3 ediciones completas (V1 talking head, V2 podcast, V3 documental): beats, plan, assets, previews | Como modelo a imitar |
| `CONTRATO.md` | Formato de `beats.json`, `edit_plan.json` y catálogo de escenas con props | Al escribir el plan |
| `system/` | Código: pipeline Python (transcribir, cortar, captions, paleta, assets, render, sonido) + render Remotion | Si el modelo puede ejecutar código |
| `knowledge/` | Los mismos documentos fusionados en 9 archivos para subir a un GPT o a un Gem | ChatGPT / Gemini |

## 1. Reglas de oro
1. **Anuncia algo nuevo → su cara (A-roll con subtítulos). Lo describe → se muestra.** Abrir siempre en la cara.
2. **Todo se sincroniza a la palabra.** El elemento entra en la palabra que lo nombra (imágenes 0.1–0.3 s antes; texto 1 frame antes); el corte de vuelta cae en la palabra que abre la frase siguiente. Nunca a mitad de palabra.
3. **Cortes secos el 70–85 % de las veces.** Transiciones solo con motivo (cambio de tema o capítulo), las de su formato y separadas ≥ 8 s. «Decorar no es editar.»
4. **El primer borrador está al 60–70 %.** Se revisa con tiempos exactos y se corrige.
5. **Nunca renderizar el final sin mostrar antes la vista previa y recibir el OK.** Los borradores de revisión sí.
6. **Si el cliente describe cómo quiere algo, se hace así**, aunque no siga estas reglas al pie de la letra.
7. **Nunca se genera nada con IA de pago** (Higgsfield, Katana, Seedance…): la skill escribe los prompts, el humano genera y entrega un zip, la skill lo usa.
8. **Nada genérico.** Cada imagen sale de un asset con prompt específico, en la marca del video, o de stock con el mismo grado de color.

## 2. Flujo obligatorio (con STOPs)
| Paso | Qué haces | Salida | STOP |
|---|---|---|---|
| 1 | Transcripción palabra a palabra al milisegundo; cortar silencios dejando **30 ms**; corregir palabras mal oídas | `transcript_cut.json` | |
| 2 | Elegir **formato** (árbol de `docs/FORMATOS.md`) y **paleta** del material (3–6 opciones) | estilo + `palette.json` | |
| 3 | Partir el guion en **beats** (una idea = un beat, 1.5–6 s) y para cada uno proponer **3 diseños A/B/C** de `ANIMACIONES.md`, con su `Ref VNN-ANN`, categoría, descripción concreta y la nota «visto en los reels» | `beats.json` → **panel** | ⏸ **STOP 1**: el humano elige en el panel y pega el plan |
| 4 | Aplicar el plan; lista de **assets** con prompts (formato/AR, referencia de consistencia, negativo) | `edit_plan.json`, `ASSETS_<p>.md` | ⏸ **STOP 2**: pedir el zip de assets + música |
| 5 | Ingerir assets (recorte al AR, grado de marca); recortes sin fondo para ilustraciones | `media/assets/` | |
| 6 | Vista previa de TODO el video en **una imagen** + hoja de subtítulos | `PREVIEW_<p>.jpg` | ⏸ **STOP 3**: OK del humano |
| 7 | Borrador con sonido → revisiones con tiempos → final 1080×1920 + versión comprimida | `master.mp4`, `master_web.mp4` | |

## 3. Qué poner según lo que se dice
| Lo que se dice | Elemento | Escena (render) | Ref |
|---|---|---|---|
| Abre / anuncia un punto / cambia de tema | A-roll con subtítulos (punch-in seco en el remate) | `aroll` | V11-A09 |
| Describe una escena o acción | B-roll literal, papel claro, bordes oscuros y desenfocados, texto fijo encima; varias tomas bajo el mismo texto | `j_broll` | V01-A03 |
| Emoción, belleza, idea filosófica | Pintura de dominio público + textura de pintura que se mueve con ella + slide de cámara + texto alrededor del sujeto | `j_painting` | V06 |
| Fases, progresión, enumeración | Línea gruesa de acento que el texto interrumpe; zigzag con fotos a los lados; la cámara sigue la punta | `j_line` | V10-A11, V10-A37 |
| Cifra, consecuencia, tendencia | Gráfico: fondo oscuro con textura, cuadrícula fina que brilla, bola de acento que avanza un punto por palabra; la cámara la sigue | `j_graph` | V19-A14 |
| Regla, tesis, pensamiento interior | Texto centrado con comillas sobre papel muy rugoso (blanco o de acento) | `j_quote` | V01-A27 |
| Presenta a una persona | Ilustración central: recorte de la persona en el color de marca, rugoso, que sangra desde abajo | `j_illus` | V10-A08 |
| Dos cosas a la vez / contraste | Ilustración lateral o media luna de tela con palabras rotando | `j_half`, `j_illus mode:side` | V10-A02 |
| Un objeto protagonista | Objeto + texto con revelado rugoso | `j_illus keep_color` | V01-A37 |
| Cifra de acción sobre la cara | Número gigante que cae | `arthur_number` | V17-A05 |
| Historia de vida / antes y después en el tiempo | Línea de tiempo (sobre papel o sobre el A-roll a la cintura) | `timeline` | V01-A13, V01-A16 |
| Recuerdo / pasado | Foto de archivo con aro y scanlines | `archival_photo` | V01-A10 |
| Llamado a la acción | Pantalla de acento con la palabra | `arthur_text` | V10-A59 |

## 4. Subtítulos (principio 1)
- Frases de **≤ 5 palabras**, cortadas **por sentido** (puntuación, pausas, antes de palabras funcionales); nunca una palabra sola; nunca partir «20 / descuentos».
- La palabra clave (1–2) **grande y negrita al centro**: Inter 800 o **Playfair Display Bold Italic** (alternan; nunca 3 iguales seguidas). **En el color de marca del video** (si el acento es muy oscuro para leerse sobre el A-roll, aclararlo lo justo).
- El resto **pequeño en Inter light, arriba y abajo**, ocupando el **75 % del ancho** de la palabra grande. Mín. 40 px / clave ≥ 100 px.
- 1 de cada 4 en serif va sobre **caja de acento** con texto blanco.
- **Sincronía:** la frase aparece **2 frames antes** de la primera palabra; cada palabra se enciende (gris → color) y termina **2 frames antes** de pronunciarse. Nunca tarde.
- **Nunca sobre la boca**: debajo del mentón (o sobre la cabeza si no cabe). Se ocultan bajo escenas a pantalla completa y vuelven en el tramo libre.

## 5. Fluidez entre escenas
- Ajuste automático a palabra (`fluidity()` en el render): entrada = inicio de palabra (imágenes −0.12 s, texto −1 frame); salida = inicio de la palabra que abre la frase siguiente.
- Huecos de A-roll < 0.6 s entre dos escenas se cierran: no hay «destellos» de cara.
- Salida de escena = corte seco (documental: fundido corto de 180 ms).
- Punch-in del A-roll = corte seco al encuadre cerrado (1.25–1.35), en el remate.

| Formato | Transiciones permitidas (además del corte) | Separación mín. | Ritmo (eventos visuales / 10 s) |
|---|---|---|---|
| Documental | crossfade, slide, destello dorado solo entre capítulos | 10 s | 10–12 |
| Animación con voz en off | slide, wipe, iris, flash blanco | 7 s | 9–19 |
| Talking head + minimal | wipe, inversión de color (sándwich) | 9 s | 6–9 |
| Clip de podcast | whip-pan, flash de tinte en cambio de tema | 8 s | 5–17 |
| Pantalla dividida | crossfade | 10 s | 1.7–4 |

## 6. Diseño (5 pilares: tamaño · composición · texturas · formas · colores)
- **Colores:** paleta por video sacada del material (ropa, set, labial): acento + acento oscuro + papel + negro. Inversión Arthur: fondo de acento con texto blanco ↔ fondo blanco con texto de acento. También se permiten **gráficos en color sólido**.
- **Texturas:** papel rugoso en fondos planos; pintura + papel en pinturas; tela en siluetas y medias lunas; grano y viñeta en b-roll; halftone en podcast.
- **Zona segura:** contenido centrado y cerca del medio (arriba 14 %, abajo 26 %, derecha 15 % los tapa la app).
- **Tipografía:** tres voces — Playfair Display Bold Italic (emoción), Inter 800 (dato), Inter light pequeña (enlace).

## 7. Sonido
- Música de base desde el segundo 0, ~10 dB bajo la voz, con ducking; volumen final **−14 LUFS**, pico ≤ −1.5 dB.
- Efectos escasos (Arthur: 1 cada 10–20 s): **clic** en textos/citas, **trazo (highlighter)** en gráficos, **whoosh** en transiciones, pop en fotos, golpe en cifras. Separación mínima entre efectos de 4–6 s.

## 8. Assets
- Lista completa con prompts en la marca del video: formato más cercano soportado (9:16, 4:5, 1:1…), resolución, imagen de referencia, negativo y nombre de archivo (`A01.png`…), entregados en `<p>.zip`.
- **Consistencia:** primero el producto hero; todo lo que lo muestra lo usa como referencia. Personas hiperrealistas tipo UGC (sin look de IA).
- Pinturas solo de dominio público (Wikimedia); stock de Pixabay con el mismo grado de marca.

## 9. Revisión (cómo pedir y aplicar cambios)
Formato: «`0:24` corte brusco» · «la espiral debe durar más, hasta "7 a 12 años"» · «textura de pintura muy fuerte y no se mueve con la pintura». Se cambia SOLO `edit_plan.json`/`beats.json` y se vuelve a renderizar el borrador.

## 10. Si el modelo no puede ejecutar código (ChatGPT/Gemini en chat)
Entrega igualmente: (1) `beats.json` y la tabla de beats con A/B/C; (2) `edit_plan.json` completo; (3) los prompts de assets; (4) la hoja de subtítulos (frases, palabra clave, tratamiento). El render se hace después con `system/` en una máquina con Python + Node (ver `MODELOS.md`).

## 11. Herramientas → `HERRAMIENTAS.md`
MCP Playwright para buscar en internet; Remotion (render), HyperFrames (clonar animaciones, bloques), Edit Studio (movimientos y géneros), ffmpeg. Instalación: `system/instalar_herramientas.sh`.

## 12. Reglas generales de Katana + Edit Studio → `KATANA_EDITSTUDIO.md`
1. Plan en 5 líneas antes de trabajar · contrato de **bloqueos y libertades**.
2. Referencia analizada **fotograma a fotograma** con **mapa de energía** (cortes, flashes, sacudidas, movimientos y golpes por segundo): la edición repite esas tasas.
3. **Roles de toma** (gancho, contexto, héroe, acción, detalle, contraste, revelación, clímax, pausa, remate) y concepto con planteamiento y remate.
4. Ritmo del **género** de Edit Studio (moda: `genres/fashion.md`) dentro del formato Arthur; movimientos con nombre de `moves/`.
5. **Prompts en 7 bloques:** función de cada referencia (`@image1` = identidad/ropa…), contexto, mapa espacial, una acción, cámara (movimiento + dosis + límite), luz/textura, bloqueos finales.
6. **Ropa del hero bloqueada** en todas las tomas; **lugares vacíos sin personas** reutilizables; generar el **doble** de duración de lo que sale en pantalla.
7. **Nunca retocar caras con código.**
8. **3 revisiones de movimiento** (ritmo · espacio y continuidad · detalle) + **QA cada 0.5 s** del material entregado (manos, objetos, identidad, ropa, texto parásito).
9. Ediciones puntuales por **#clip / tiempo / palabra**; versiones nuevas que no repiten la anterior.
