# Prompts listos para copiar (cualquier modelo)

Sustituye lo que va entre `<…>`. Funcionan igual en Claude, ChatGPT y Gemini con esta skill cargada.

## 1. Entrenar un estilo nuevo (como hizo Joseph con Arthur)
```
Quiero enseñarte un estilo de edición nuevo. Analiza este estilo premium minimal usando los <20> videos de referencia.
Empieza con una transcripción palabra a palabra y un desglose fotograma a fotograma de cada video para estudiar tres
cosas: 1) dónde van las animaciones respecto al guion, 2) cómo está compuesto el diseño y qué elementos lo forman,
3) la lógica de la animación: cuánto dura y cómo se siente, para poder recrearla. Usa el tablero de inspiración como
referencia del desglose de los elementos del estilo y domina el estilo con las dos cosas. Guarda cada animación en su
carpeta con su ID, su hoja de keyframes y su ficha, y empaquétalo todo como una skill.
```

## 2. Editar un video nuevo — plan (STOP 1)
```
Usa la skill de edición Arthur Brooks para editar este clip <nombre.mp4> en su estilo premium.
Empieza con una transcripción palabra a palabra al milisegundo y corta todos los silencios dejando 30 ms.
Elige el formato y propón 3–6 paletas sacadas del material.
Luego dame el panel de planificación: guion a la derecha con el clip y, a la izquierda, por cada beat, 3 diseños
recomendados (A/B/C) sacados de la biblioteca de animaciones de Arthur (con Ref VNN-ANN, categoría, descripción
concreta y la nota "visto en los reels"), para que yo decida qué se construye en cada escena.
Recuerda: cuando anuncia algo nuevo, va su cara; cuando lo describe, se muestra.
```

## 3. Construir (después de elegir en el panel)
```
Este es mi plan: <pega lo que copia el botón "Copiar plan">.
Construye todas las animaciones y crea la edición. Si necesitas assets, dame la lista completa con prompts en la marca
del video (formato, referencia de consistencia, negativo, nombre de archivo) para generarlos y te los paso en <p>.zip.
Muéstrame la vista previa de todo el video en una sola imagen antes de renderizar.
```

## 4. Revisiones (el primer borrador está al 60–70 %)
```
Revisiones:
1. <0:01> el diseño del texto de la primera escena no está bien; deja "<palabra>" arriba en la misma escena.
2. <0:06> corte brusco entre el gráfico y el siguiente plano: mantén el texto del gráfico hasta 0:06 y corta.
3. <0:11> la textura de pintura está muy fuerte y no se mueve con la pintura: a la mitad y que se mueva con ella.
4. <0:24> mal corte: quita el clip de "Pero".
5. <0:25> deja la espiral más tiempo, hasta "7 a 12 años", con el zoom-out lento.
6. Pon comillas en la escena de texto del final.
```

## 5. Sonido
```
El video está perfecto. Haz el diseño sonoro basándote en los 20 videos de referencia: música cinematográfica de base,
clics para los textos, highlighter para los gráficos y whooshes para las transiciones. Mezcla a −14 LUFS.
```

## 6. Assets (pedir la lista)
```
Dame un documento con TODOS los assets que necesitas para este video (imágenes, b-roll, ilustraciones, texturas,
gráficos), con prompts completos y optimizados en la marca del video: formato más cercano soportado y resolución,
imagen de referencia para la consistencia (primero el producto/persona hero), prompt, negativo, nombre de archivo y
el nombre del zip.
```
