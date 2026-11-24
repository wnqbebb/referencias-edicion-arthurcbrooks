# V1 · Prompts de assets (Talking head + minimal)

## Orden de generación y consistencia

Genera en este orden. Cada paso usa como imagen de referencia el archivo indicado, para que la prenda y la persona sean idénticas en todo el video.

1. **A01** Blusa hero: la prenda real del video (referencia de consistencia) — primero, es la referencia.
1. **A02** Modelo UGC con la blusa puesta, look completo — con referencia A01.
1. **A03** La misma modelo girando junto a la ventana (buena luz) — con referencia A02.
1. **A04** Pasillo de centro comercial: todas las vitrinas con el mismo -30 % — independiente.
1. **A05** Primer plano de carteles de descuento idénticos — independiente.
1. **P01** Pintura clásica de dominio público: una tienda de ropa elegante — independiente.
1. **A06** Papel rugoso de la marca — independiente.

**Reglas**

- Personas: hiperrealistas tipo UGC (piel con poros, luz de ventana, encuadre de celular). Si se ve a IA, se repite.
- Si tu generador no tiene el formato exacto, usa el más cercano y deja aire alrededor: yo recorto.
- Videos: genera primero el fotograma con el prompt y luego anímalo (image-to-video) con el movimiento indicado.
- No pongas texto dentro de las imágenes salvo donde el prompt lo pide: los textos los anima el sistema encima.
- Al recibirlos aplico el grado de marca a todo: contraste +8 %, saturación −15 %, tinte vino #5A0F21 en sombras (soft-light 12 %), grano fino.

## Prompts de imágenes: producto, modelos y escenas

### A01 · Blusa hero: la prenda real del video (referencia de consistencia)

| Campo | Valor |
|---|---|
| Archivo | `A01.png` |
| Tipo | Producto (referencia) |
| Formato | 4:5 · 1536×1920 |
| Dónde sale | s07 «Completa» |

**Prompt**

```
Product photo of a deep wine-red (#5A0F21 to #9E1C3A) satin wrap blouse with long sleeves on a slim wooden hanger, hanging against a warm off-white (#F7F3F2) plaster wall, soft directional window light from the left, gentle fabric folds and realistic satin sheen, small visible stitching at the cuffs, minimalist boutique aesthetic, centered, generous negative space above the hanger. shot on a full-frame camera with a 50mm lens, true-to-life fabric texture, accurate color, subtle natural shadows, real-world imperfections in the fabric, e-commerce boutique photography, not CGI
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

> Si tienes foto real de la blusa que vende, úsala como referencia de este prompt: la consistencia parte de aquí.

### A02 · Modelo UGC con la blusa puesta, look completo

| Campo | Valor |
|---|---|
| Archivo | `A02.png` |
| Tipo | Modelo UGC |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s07 «Puesta», s10 órbita final |
| Imagen de referencia | `A01` |

**Prompt**

```
Vertical UGC photo of a 28-year-old Latina woman with dark wavy shoulder-length hair wearing the exact wine-red satin wrap blouse from the reference image, tucked into high-waisted black tailored trousers, small gold hoop earrings, standing in a small bright boutique next to a window, relaxed natural pose with one hand in her pocket, looking slightly off camera, full body visible from head to knees, face in the upper third, plain warm wall behind her. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

## Prompts de ilustraciones, pinturas y texturas

### P01 · Pintura clásica de dominio público: una tienda de ropa elegante

| Campo | Valor |
|---|---|
| Archivo | `P01.png` |
| Tipo | Pintura |
| Formato | 4:5 · 1536×1920 |
| Dónde sale | s04 «donde la ropa se ve bonita» |

**Prompt**

```
PRIMERA OPCIÓN (dominio público, no generar): James Tissot, «The Shop Girl» (La demoiselle de magasin), 1883–85, Art Gallery of Ontario. Descárgala de Wikimedia Commons en la máxima resolución y recórtala 4:5 centrada en la dependienta. ALTERNATIVA generada: Oil painting in the style of late 19th-century French realism, an elegant Parisian boutique interior with a young woman in a fitted wine-red dress holding fabric ribbons, warm window light, visible brush strokes and canvas texture, muted palette with deep wine (#5A0F21) accents, museum reproduction look.
```

**Negativo**

```
modern clothing, photographic look, text, frame, watermark, oversaturated
```

### A06 · Papel rugoso de la marca

| Campo | Valor |
|---|---|
| Archivo | `A06.png` |
| Tipo | Textura |
| Formato | 1:1 · 1920×1920 |
| Dónde sale | fondos de todas las escenas minimal |

**Prompt**

```
Seamless high-resolution scan of off-white (#F7F3F2) cotton rag paper, visible fibers and fine grain, very soft uneven lighting, faint warm tint, no folds, flat scan, tileable.
```

**Negativo**

```
text, objects, shadows, wrinkles, strong color, vignette
```

## Prompts de video b-roll y movimiento

### A03 · La misma modelo girando junto a la ventana (buena luz)

| Campo | Valor |
|---|---|
| Archivo | `A03.mp4` |
| Tipo | Video |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s07 «Buena luz» |
| Duración | 5 s |
| Imagen de referencia | `A02` |
| Movimiento | Push-in lento 5 %, giro de ¼ de la modelo, la luz recorre la tela. Sin cortes, sin cámara lenta. |

**Prompt**

```
Image-to-video from the reference image: the same woman in the wine-red satin blouse slowly turns a quarter towards a large window, soft golden afternoon light sweeps across the satin and shows its sheen, she smooths the front of the blouse with one hand, gentle handheld camera with a subtle push-in. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays
```

### A04 · Pasillo de centro comercial: todas las vitrinas con el mismo -30 %

| Campo | Valor |
|---|---|
| Archivo | `A04.mp4` |
| Tipo | Video |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s02 «todas bajan los precios» |
| Duración | 5 s |
| Movimiento | Travelling lateral de izquierda a derecha a paso de persona; las vitrinas pasan una tras otra. |

**Prompt**

```
Vertical handheld video walking past several clothing store windows in a shopping mall at night, every window shows the same generic red 'SALE -30%' sign, blurred shoppers crossing the frame, warm mall lighting, slight motion blur, realistic documentary feel. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays
```

### A05 · Primer plano de carteles de descuento idénticos

| Campo | Valor |
|---|---|
| Archivo | `A05.mp4` |
| Tipo | Video |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s02 segunda toma |
| Duración | 4 s |
| Movimiento | Rack focus del cartel 1 al cartel 3, cámara casi fija. |

**Prompt**

```
Vertical close-up video, slow rack focus across a row of identical red paper 'BLACK FRIDAY -30%' signs taped to shop glass, reflections of the mall lights on the glass, shallow depth of field, moody evening light. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays
```

## Entrega

Mete todos los archivos en un zip llamado **`v1.zip`**, sin carpetas dentro, con estos nombres exactos:

| Archivo | Qué es | Formato |
|---|---|---|
| `A01.png` | Blusa hero: la prenda real del video (referencia de consistencia) | 4:5 |
| `A02.png` | Modelo UGC con la blusa puesta, look completo | 9:16 |
| `A03.mp4` | La misma modelo girando junto a la ventana (buena luz) | 9:16 |
| `A04.mp4` | Pasillo de centro comercial: todas las vitrinas con el mismo -30 % | 9:16 |
| `A05.mp4` | Primer plano de carteles de descuento idénticos | 9:16 |
| `P01.png` | Pintura clásica de dominio público: una tienda de ropa elegante | 4:5 |
| `A06.png` | Papel rugoso de la marca | 1:1 |

Al recibirlo ejecuto `assetpack.py v1 --ingest v1.zip`: valida que estén todos, recorta al formato, aplica el grado de marca y monta la vista previa con los elementos integrados, el diseño sonoro y la música para tu aprobación antes de renderizar.
