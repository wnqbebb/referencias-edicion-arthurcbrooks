# Herramientas necesarias

Todo se instala con un comando, desde `system/`:
```bash
bash instalar_herramientas.sh
```

## 1. MCP
| MCP | Para qué | Cómo |
|---|---|---|
| **Playwright** (`@playwright/mcp`) | Navegar por internet: buscar y descargar pinturas, b-roll, música, efectos y referencias | Ya va en `system/.mcp.json`; Claude Code lo carga al abrir la carpeta |

En ChatGPT y Gemini se usa su navegador o búsqueda integrada con las mismas instrucciones (sección 3).

## 2. Skills y plugin
| Qué | Para qué | Viene |
|---|---|---|
| **Edit Studio** (plugin de Higgsfield, `plugins/edit-studio/`) | 268 movimientos con nombre, 15 géneros (fashion, ugc, product…), ediciones puntuales por voz, vista previa con clips numerados, versiones sin repetir, medir efectos de un clip | **Incluido.** El instalador lo copia a `.claude/skills/`. Su parte de generación (`edit-gen`) no se usa |
| **Katana** (método) | Análisis fotograma a fotograma con mapa de energía, prompts en 7 bloques, lugares vacíos, 3 revisiones de movimiento, control de calidad | **Incluido** en `docs/katana/` y `KATANA_EDITSTUDIO.md`. No se genera nada con él |
| **Remotion** (`remotion-dev/skills`) | Motor del render: subtítulos, escenas, exportación | El instalador lo descarga |
| **HyperFrames** (`heygen-com/hyperframes`) | `reverse-any-video` (clonar una animación de un reel), `hyperframes-registry` (~450 bloques: grano, glitch, gráficos, cámara), `media-use` (sonido, imágenes, recortes) | El instalador lo descarga |
| **ffmpeg** y **gallery-dl** (skills) | Convertir, recortar y comprimir; descargar imágenes y galerías | El instalador lo descarga |

Programas: Python 3.11+, Node 18+, `ffmpeg`, `yt-dlp` y `gallery-dl`.

## 3. Buscar material en internet
| Material | Dónde | Regla |
|---|---|---|
| **Pinturas** | Wikimedia Commons, Met Open Access, Art Institute of Chicago (CC0) | Solo dominio público; créditos en `CREDITOS.json` |
| **B-roll** | Pixabay (`pipeline/stock_api.py`, clave en la variable `PIXABAY_API_KEY`) | Literal al guion y con el color de marca |
| **Música** | Mixkit (`node pipeline/gen/fetch_music.mjs`), YouTube Audio Library | Grabada, nunca sintetizada; ~10 dB bajo la voz |
| **Efectos** | Mixkit (`node pipeline/gen/fetch_sfx.mjs`), Freesound CC0 | Pocos y en su evento |
| **Referencias** | Instagram con `gallery-dl`; YouTube con `yt-dlp` en tu computador (bloquea servidores en la nube) | Se mide su ritmo y energía; no se copia su material |

Pídelo así:
> Busca una pintura de dominio público de una tienda elegante del siglo XIX, descárgala en máxima resolución y anota los créditos.

## 4. Remotion, HyperFrames y Edit Studio: quién hace qué
| Motor | Hace |
|---|---|
| **Remotion** | El video final: subtítulos, escenas `j_*`, transiciones, render |
| **Edit Studio** | Elegir movimientos y ritmo por género; ediciones puntuales; QA medido. Su motor ffmpeg sirve para cortes rápidos y versiones |
| **HyperFrames** | Clonar una animación concreta de un reel; entra al video como asset o como escena nueva de Remotion |

**Nada se genera con IA de pago.** La skill entrega los prompts; tú generas y devuelves el zip.
