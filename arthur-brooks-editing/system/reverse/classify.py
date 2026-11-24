#!/usr/bin/env python3
"""Clasificador de FORMATO de video (método REA: señales observadas → derivadas → formato inferido).

  python reverse/classify.py refs/arthur/*.mp4 [--labels styles/arthur-brooks/formats/labels.json]

Señales (observed, por fotograma a 2 fps):
  face      — hay cara (Haar frontal) y su tamaño relativo
  seam      — costura horizontal fuerte en 35–65 % del alto (pantalla dividida)
  flat      — ≥70 % de píxeles en ≤3 colores (fondo gráfico plano: animación / tarjetas)
  white     — brillo medio > 200 (escenas de papel blanco: collage, timeline)
  cuts/min  — cambios de plano (ffmpeg scene>0.32)
Reglas (derived → inferred) en FORMAT_RULES; si hay labels humanas, reporta acierto.
"""
import os
import argparse
import json
import re
import subprocess
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
STYLE = os.environ.get("VES_STYLE", "arthur-brooks")   # estilo que se está entrenando
REFS = ROOT / "refs" / os.environ.get("VES_REFS", "arthur")  # carpeta con los videos de referencia vNN.mp4
CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def frames(video, fps=2, w=180):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", f"fps={fps},scale={w}:320", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                       capture_output=True, check=True).stdout
    arr = np.frombuffer(p, np.uint8)
    return arr.reshape(-1, 320, w, 3)


def cuts_per_min(video):
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(video), "-vf", "select='gt(scene,0.32)',showinfo", "-an", "-f", "null", "-"], text=True, capture_output=True)
    n = len(re.findall(r"pts_time:", r.stderr))
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)], text=True, capture_output=True).stdout)
    return n / d * 60, d


PROFILE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")


def signals(video):
    F = frames(video, w=270)
    face, face_big, seam_rows, flat, white = [], [], [], [], []
    H = F.shape[1]
    for f in F:
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        fs = list(CASCADE.detectMultiScale(g, 1.1, 4, minSize=(22, 22))) + list(PROFILE.detectMultiScale(g, 1.1, 5, minSize=(22, 22)))
        face.append(len(fs) > 0)
        face_big.append(max([w * h for (x, y, w, h) in fs], default=0) / (g.shape[0] * g.shape[1]))
        # costura: fila donde CASI TODAS las columnas cambian fuerte (los captions no cubren todo el ancho)
        d = np.abs(np.diff(g.astype(float), axis=0)) > 22
        cover = d.mean(1)
        lo, hi = int(0.30 * H), int(0.80 * H)
        r = lo + int(np.argmax(cover[lo:hi]))
        seam_rows.append(r if cover[r] > 0.60 else -1)
        q = (f // 43).reshape(-1, 3)
        _, c = np.unique(q[:, 0] * 36 + q[:, 1] * 6 + q[:, 2], return_counts=True)
        flat.append(np.sort(c)[::-1][:3].sum() / c.sum() > 0.70 and g.mean() > 70)  # fondo gráfico (no oscuridad)
        white.append(g.mean() > 200)
    rows = [r for r in seam_rows if r >= 0]
    if rows:  # costura estable = misma fila (±3 px) en muchos fotogramas
        mode = max(set(rows), key=rows.count)
        seam = sum(1 for r in seam_rows if r >= 0 and abs(r - mode) <= 3) / len(seam_rows)
    else:
        seam = 0.0
    cpm, dur = cuts_per_min(video)
    m = lambda x: round(float(np.mean(x)), 3)
    return {"duration": round(dur, 1), "face": m(face), "face_size": round(float(np.median([x for x in face_big if x] or [0])), 3),
            "seam": round(seam, 3), "flat": m(flat), "white": m(white), "cuts_per_min": round(cpm, 1)}


FORMAT_RULES = [
    # (formato, condición, explicación) — el orden importa
    ("podcast_split", lambda s: s["seam"] > 0.12 and s["face"] > 0.4, "costura horizontal estable (30–80 % del alto) en parte del video + caras → pantalla dividida"),
    ("animacion_vo", lambda s: s["face"] < 0.25 and (s["flat"] > 0.3 or s["white"] > 0.3), "casi sin cara + fondos gráficos planos → animación con voz en off"),
    ("talking_head_minimal", lambda s: s["flat"] > 0.17 and s["face"] > 0.25, "A-roll alternado con escenas gráficas planas (azul/blanco)"),
    ("documental_bio", lambda s: s["white"] > 0.06 and s["face"] > 0.3 and s["cuts_per_min"] > 18, "A-roll + escenas de papel blanco + corte rápido → documental biográfico"),
    ("podcast_clip", lambda s: s["face"] >= 0.25, "predomina la cara, pocas gráficas → clip de podcast con zooms/cambios de cámara"),
]


def classify(s):
    for name, cond, why in FORMAT_RULES:
        if cond(s):
            return name, why
    return "desconocido", "ninguna regla aplica"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="+")
    ap.add_argument("--labels", default=None)
    ap.add_argument("--out", default=str(ROOT / "styles" / STYLE / "formats" / "classification.json"))
    a = ap.parse_args()
    labels = json.loads(Path(a.labels).read_text()) if a.labels else {}
    rows, ok = [], 0
    for v in a.videos:
        key = Path(v).stem
        s = signals(v)
        fmt, why = classify(s)
        lab = labels.get(key, {}).get("format")
        ok += int(lab == fmt) if lab else 0
        rows.append({"video": key, "observed": s, "inferred_format": fmt, "why": why, "human_label": lab})
        print(f"{key:5s} {fmt:22s} humano={lab or '-':22s} {s}")
    if labels:
        print(f"acierto vs etiquetas humanas: {ok}/{sum(1 for r in rows if r['human_label'])}")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
