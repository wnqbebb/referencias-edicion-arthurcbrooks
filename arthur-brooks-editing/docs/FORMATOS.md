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
