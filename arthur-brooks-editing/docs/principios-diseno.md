# Principios de diseño (destilados del video "17 Design Tips") → cómo los aplica VES

| # | Principio | Regla operativa | Dónde vive en VES |
|---|---|---|---|
| 1 | Tipografía | 1 sans moderna (80 % del edit) + 1 especial serif/script para palabras clave | `style.json → fonts`, `CinematicText` |
| 2 | Colocación (regla de tercios) | Centro = foco (speaker/gráfico principal). Bordes = secundarios | layout de cada escena |
| 3 | Balance | 2 objetos: uno en cada mitad (horizontal / vertical / diagonal). Vertical → balance vertical | `two_object`, `before_after` |
| 4 | Contraste | Dirige la atención por color, textura, tamaño o forma | acento sólo en el objeto principal |
| 5 | Color 60/30/10 | primario 60 / secundario 30 / acento 10. Paleta: color dominante del footage → vibrante claro, vibrante oscuro, blanco apagado, negro apagado | `ves.py palette`, `palette.roles` |
| 6 | Reglas de marca | Por cliente: colores, 2 fuentes, reglas de colocación, forma (aristas), lógica de animación (suave/lenta vs rígida/rápida) | un `style.json` por cliente/estilo |
| 7 | Diseño desde el guion | ¿1 objeto? foco + acento. ¿2 objetos? balance + secundario; contraste solo al destacar uno | `RECO_RULES` del plan.html |
| 8–10 | Horizontal / vertical / diagonal | Vertical: speaker tercio superior, caption tercio inferior; objeto arriba + texto abajo | `speaker.eyes_line`, `captions.zone` |
| 11 | Roba como artista | Copia layout, colores o fuentes de referencias | `styles/*/references/` |
| 12 | Tablero de 1000 inspiraciones | Tablero por categorías (1 objeto, diagonal, UI…) | `reverse/breakdown.py → board.html` |
| 13 | Desglosar inspiración | **ASSETS → EFFECTS → ANIMATION** | `cards.md` por plano |
| 14 | Planificar con inspiración | Cada línea del guion ↔ una referencia antes de editar | `plan.html` (pegar referencias) |
| 15 | Short-form | Fondo con grid fino o halftone; objeto en acento; frase sans + 1 palabra script; elementos borrosos en esquinas | `Backdrop`, `Texture` |
| 16 | Long-form | Objeto en un tercio, texto en otro; fondos claros + texto oscuro se ve más caro | (futuro estilo 16:9) |
| 17 | On-screen vertical | Captions en tercio inferior; UI bajo captions, mismo ancho o menor | Edit.tsx captions |
| 18 | On-screen horizontal | Mitad con sujeto, otra mitad blur+oscura con texto; texto pequeño = premium | `validate` limita palabras |
