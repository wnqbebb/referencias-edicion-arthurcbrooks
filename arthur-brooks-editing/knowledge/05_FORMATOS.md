# Arthur Brooks — los 5 formatos dentro de los 20 videos

Un solo creador, **cinco formatos distintos**. Cada formato es un estilo de VES (`styles/arthur-*/style.json`).
Clasificación hecha a mano (`labels.json`) y con un clasificador automático que da la primera sugerencia (`reverse/classify.py`, 12/20 aciertos): siempre la confirma un humano.

| # | Formato | Estilo VES | Videos | Cómo lo reconoces en 3 segundos |
|---|---|---|---|---|
| 1 | **Documental biográfico** ⭐ | `arthur-documental` | v01 (maestro), v11 | Habla a cámara en un set oscuro de noche + fotos de archivo + collages en papel blanco + línea de tiempo por edades + corte cada ~2 s |
| 2 | **Animación minimal con voz en off** | `arthur-minimal-vo` | v10, v12, v19 · variantes v03 (ilustración plana), v04 (tipografía manuscrita) | **Nunca aparece su cara.** Fondos blanco/azul pleno, íconos, cerebros, círculos y b-roll oscuro con texto serif |
| 3 | **Talking head + minimal** | `arthur-talking-minimal` | v06, v08, v16 | Entrevista o podcast que se intercala con escenas azules minimal, pinturas clásicas y b-roll de cine |
| 4 | **Clip de podcast** (zooms + cambios de cámara) | `arthur-podcast-clip` | v02, v07, v09, v13, v17, v18 | Multicámara de podcast, punch-ins, captions en MAYÚSCULAS condensadas palabra por palabra, casi sin gráficos |
| 5 | **Podcast en pantalla dividida** | `arthur-podcast-split` | v05, v14, v15, v20 | Arriba el primer plano del que habla (~66 %) y abajo el plano abierto de la mesa |

## Árbol de decisión (para el modelo y para ti)
```
¿Hay cara a cámara?
├─ NO → (2) animacion_vo
│        ├─ ¿solo dibujo plano con personajes?      → variante ilustración (v03)
│        └─ ¿solo palabras manuscritas en papel?     → variante kinetic_type (v04)
└─ SÍ → ¿la pantalla está partida arriba/abajo de forma estable?
         ├─ SÍ → (5) podcast_split
         └─ NO → ¿hay escenas gráficas (papel blanco/azul) intercaladas?
                  ├─ NO → (4) podcast_clip
                  └─ SÍ → ¿cuenta SU HISTORIA (pasado, edades, fotos de archivo)?
                           ├─ SÍ → (1) documental_bio
                           └─ NO (enseña una idea) → (3) talking_head_minimal
```

## Qué formato elegir para TU material en bruto
| Tu material | Formato |
|---|---|
| Hablas a cámara contando tu historia o trayectoria | **documental** (el top) |
| Solo tienes audio o voz (sin video tuyo) | **minimal con voz en off** |
| Hablas a cámara explicando un concepto | **talking head + minimal** |
| Grabaste un podcast o entrevista con 2+ cámaras | **clip de podcast** |
| Podcast con un primer plano y un plano abierto, sin mucho presupuesto de edición | **pantalla dividida** |

## Medidas (evidencia observada → `references/vNN/evidence.json`)
- Azul de marca: v10 `#0134ED`, v12 `#1B54F8`, v19 `#1369FA`, v08 `#0348E6` → token `#1B54F8`
- Papel: `#FAF7FA` (v10/v12/v19) · crema de v04: `#F2EDE1` · fondo oscuro de v04: `#343133` · azul marino de v03: `#17205A`
- Ritmo: v01 tiene 78 planos en 150 s (~1.9 s por plano); v10 tiene 68 planos en 111 s (~1.6 s). En los podcasts los cortes vienen de los cambios de cámara, de 1 a 7 por minuto.


---

# Anatomía de v01 "my life", la referencia maestra (documental biográfico)

Desglose fotograma a fotograma, con muestras cada 1.5 s. Las hojas de fotogramas están en `references/v01/shots/`.
Cada fila se lee así: **qué se ve → cómo está hecho → por qué va ahí**.

| t | Qué se ve | Cómo está hecho (ASSETS / EFFECTS / ANIMATION) | Por qué |
|---|---|---|---|
| 0:00 | A-roll: set oscuro de noche, bokeh, reflejo en la mesa. Caption "Hi **friends.**" | Caption al **centro vertical**. "Hi" pequeño arriba a la izquierda y "friends." en bold sans apretada | Hook: cara + saludo directo, conexión inmediata |
| 0:01.5 | Foto de estudio sobre fondo blanco: "My name is / ***Arthur Brooks.***" | Nombre en serif itálica **azul**, "My name is" pequeño encima y alineado a la izquierda | Presenta al personaje (`name_card`) |
| 0:03 | Papel blanco con 3 fotos (escribe / habla / enseña) y la palabra "speak" en serif azul | Fotos impresas con borde y sombra, solapadas; etiqueta pequeña + palabra serif | Identidades, de una en una (`paper_collage`) |
| 0:04.5 | B-roll: siluetas en la playa al atardecer. "about the science of ***happiness.***" | Stock cálido, caption serif grande al centro | Le da imagen a la idea abstracta (la felicidad) |
| 0:06–0:07.5 | Papel blanco: "I'm a **professor**" con foto (fondo lila); después "professor" y "author" en las esquinas | Una foto centrada, luego dos fotos en diagonal (balance diagonal) | Más roles: primero uno solo, después el contraste entre dos |
| 0:09–0:10.5 | A-roll en primer plano y en plano medio: "***Thank*** … on" | **Punch-in con corte seco** al cambiar de frase | Ritmo sin necesidad de gráficos |
| 0:12–0:13.5 | Grabación de pantalla del perfil de Instagram; el cursor hace clic en Follow: "***follow me.***" | Interfaz real con poca profundidad de campo, cursor visible | Llamada a la acción mostrada de forma literal |
| 0:15 | A-roll: "Well, you might / **not know** / many things" | Contexto arriba y abajo, palabra clave en bold sans | Gancho de curiosidad |
| 0:16.5 | Archivo de video: él con toga y borlas: "how I got to ***where I am,***" | Video de archivo granulado | Prueba de autoridad |
| 0:18 | A-roll: "and I get these **questions** a lot." | — | — |
| 0:19.5–0:21 | Interfaz de DM desenfocada con una burbuja azul: "How do you wind up becoming a professor of happiness…?" | Pantalla de mensajes con el foco sobre la burbuja | **Pregunta de la audiencia = arranca la historia** |
| 0:22.5 | Papel blanco: fotos familiares antiguas apiladas | Fotos impresas que caen con una rotación leve | Empieza el flashback |
| 0:24 | Foto de archivo a pantalla completa con aro cian alrededor del niño: "I knew ***what I was*** going to…" | **Scanlines CRT** + aro con brillo | Señala al protagonista en el pasado (`archival_photo`) |
| 0:27–0:28.5 | Papel blanco: "the world's…" y foto en B/N con el corno francés → foto a color girada | Las fotos aparecen y rotan | — |
| 0:33 | Foto en B/N de joven: "and ***my dream*** was to," | Grano y B/N | Emoción y sueño |
| 0:34.5 | A-roll: "as soon as I / ***to go pro***" | — | — |
| 0:36 | **Línea de tiempo** sobre blanco: "BECAME A PROFESSIONAL MUSICIAN · 19 YEARS", marcador azul y foto debajo | Línea fina, ticks, versalitas, segmento azul que avanza | Ordena la vida por edades (`timeline`) |
| 0:45 | Negro con una tarjeta pequeña de video (casa) y "support a family," | Video dentro de una tarjeta redondeada | Escena íntima y pequeña (`video_card`) |
| 0:51–0:54 | La línea de tiempo baja **sobre el A-roll**: 19 → 24 años ("MET MY SOULMATE"), con fotos de pareja que caen encima | Timeline superpuesto (over_aroll) con fotos que caen | Un hito nuevo |
| 0:58.5 | B-roll: mano escribiendo, cálido: "First, to ***go back***" | — | — |
| 1:01.5 | Papel blanco: "I was a **musician,**" con etiqueta azul "OCCUPATION" y foto girada | Etiqueta de dato estilo ficha | — |
| 1:03 | A-roll: "had ***zero dollars*** in my" | Bloque serif de 2 palabras | Cifra emocional |
| 1:07–1:10 | Timeline: 30 años, "LEFT MUSIC AND PURSUED A DOCTORATE", foto con un bebé; después foto con borde de sello | Fotos que entran desde el borde | — |
| 1:16.5 | Timeline 40–50 años: "BECAME THE PRESIDENT OF THE AEI" + foto de podio | — | — |
| 1:21 | A-roll: "**Washington** helping policy" | — | — |
| 1:22.5 | Archivo: él en un atril del AEI | Video de archivo | Prueba |
| 1:24 | **Azul radial** con comilla: "“ I needed…" | Gradiente radial azul con comilla serif | Pensamiento interior (`blue_quote`) |
| 1:27 | A-roll: "You might sense ***a pattern*** here," | — | Momento de reflexión |
| 1:30 | "taking my whole ***career down*** to the studs." | — | Tesis del video |
| 1:34–1:36 | Tarjetas de video sobre negro (mano con pluma, papel) | `video_card` en vertical | — |
| 1:48–1:49.5 | Selfie en una iglesia → papel gris con un **óvalo azul** a mano alrededor de la cara: "I'm a ***Catholic***" | Marcado a mano en azul | Revela su identidad |
| 1:51–1:55 | B-roll del rosario → A-roll: "walked the ***Camino***… **pilgrimage,**" | La misma palabra cambia de tratamiento (bold → serif) | Repetición con variación |
| 2:01–2:04 | Archivo de conferencias y togas académicas | Montaje rápido | Prueba de autoridad acumulada |
| 2:07 | **Timeline sobre el A-roll**: 55 → 60 años, "BECAME A PROFESSOR AT HARVARD UNIVERSITY" | Over_aroll a la altura de la cintura | — |
| 2:10–2:12 | B-roll de playa/atardecer: "where I ***taught leadership*** and happiness" | — | — |
| 2:15–2:16.5 | A-roll: "And I've ***built the things*** that you see" | — | — |
| 2:18–2:21 | Portadas de sus libros + b-roll de él leyendo | Cámara macro | Producto y prueba |
| 2:24–2:27 | B-roll de felicidad (parejas, amigos): "science of **happiness**" | Bold sans sobre b-roll | Cierre emocional |
| 2:28.5 | A-roll: "**Thank you** for sharing" | — | Cierre con la cara |

## Reglas extraídas del video (son las que aplica el estilo `arthur-documental`)
1. **Captions siempre en el centro vertical** (~50 %), centrados. La zona segura se respeta por diseño.
2. **Dos tratamientos para la palabra grande:** bold sans apretada (palabras sueltas, concretas) y serif itálica bold (frases de 2–3 palabras, más emocionales). Se alternan y nunca se repite el mismo tres veces seguidas.
3. **Las palabras de contexto son pequeñas:** las de antes de la palabra clave van arriba a la izquierda y las de después, abajo a la derecha.
4. **Punch-in con corte seco** entre plano medio y primer plano en cada oración nueva.
5. **Cuenta la vida por edades:** línea de tiempo con hitos y fotos que caen encima. La primera vez va sobre papel; después, sobre el A-roll.
6. **Papel blanco = identidad y archivo personal.** Negro con tarjeta = momento íntimo. Azul = pensamiento interior.
7. **Archivo = prueba de autoridad** (togas, atriles, portadas de libros), siempre antes o después de la frase que lo afirma.
8. **Estructura:** hook con saludo → presentación del nombre → identidades → pregunta de la audiencia → flashback por edades → giro ("I needed…") → lección ("a pattern", "career down to the studs") → cierre con prueba y gracias.
9. El **azul de acento** solo aparece en el nombre, en las palabras de las etiquetas, en el marcador del timeline y en el óvalo marcado a mano: es ~10 % de la imagen.
