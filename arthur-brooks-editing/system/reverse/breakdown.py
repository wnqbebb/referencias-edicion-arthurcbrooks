#!/usr/bin/env python3
"""Ingeniería inversa de un video de referencia (método REA aplicado a edición).

  python reverse/breakdown.py REF.mp4 --style-id mi-estilo [--transcribe]

Produce en styles/<style-id>/references/<video>/:
  evidence.json   — hechos con su nivel epistémico (observed / derived / inferred / unknown)
  shots/NNN.jpg   — hoja de keyframes por plano (inicio, 25%, 50%, 75%, fin)
  cards.md        — una ficha por plano: ASSETS / EFFECTS / ANIMATION (principio 13) a completar
  board.html      — tablero de inspiración (reemplazo local de Figma), agrupable por categoría

Regla REA: el modelo NO puede escribir en el rulebook nada que no esté respaldado por
evidencia 'observed' o 'derived'. Lo 'inferred' necesita confirmación humana.
"""
import argparse
import colorsys
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def sh(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def duration(v):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)]).stdout)


def detect_cuts(v, thr):
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(v), "-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"],
                       text=True, capture_output=True)
    return [float(m) for m in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def frame_at(v, t, w=270):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(v), "-frames:v", "1", "-vf", f"scale={w}:-2",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    from io import BytesIO
    return Image.open(BytesIO(raw)).convert("RGB") if raw else None


def palette(img, k=5):
    a = np.asarray(img.resize((80, 140))).reshape(-1, 3).astype(float)
    q = (a // 32).astype(int)
    keys, counts = np.unique(q[:, 0] * 64 + q[:, 1] * 8 + q[:, 2], return_counts=True)
    top = keys[np.argsort(counts)[::-1][:k]]
    out = []
    for t in top:
        m = (q[:, 0] * 64 + q[:, 1] * 8 + q[:, 2]) == t
        c = a[m].mean(0)
        out.append({"hex": "#%02X%02X%02X" % tuple(int(x) for x in c), "share": round(float(m.mean()), 3)})
    return out


def motion_energy(frames):
    if len(frames) < 2:
        return 0.0
    arr = [np.asarray(f.resize((64, 112)).convert("L"), dtype=float) for f in frames]
    return round(float(np.mean([np.abs(x - y).mean() for x, y in zip(arr, arr[1:])])), 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--style-id", required=True)
    ap.add_argument("--threshold", type=float, default=0.32)
    ap.add_argument("--transcribe", action="store_true")
    a = ap.parse_args()
    v = Path(a.video).absolute()  # sin resolve(): conserva el nombre del enlace (vNN)
    out = ROOT / "styles" / a.style_id / "references" / v.stem
    (out / "shots").mkdir(parents=True, exist_ok=True)
    D = duration(v)
    cuts = [0.0] + [c for c in detect_cuts(v, a.threshold) if 0.15 < c < D - 0.15] + [D]
    words = []
    if a.transcribe:
        from faster_whisper import WhisperModel
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(v), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
        segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(np.frombuffer(pcm, np.float32), word_timestamps=True)
        words = [{"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)} for s in segs for w in (s.words or [])]
    shots = []
    for i, (s, e) in enumerate(zip(cuts, cuts[1:])):
        ts = [s + (e - s) * f for f in (0.04, 0.25, 0.5, 0.75, 0.96)]
        frames = [f for f in (frame_at(v, t) for t in ts) if f]
        if not frames:
            continue
        W, H = frames[0].size
        sheet = Image.new("RGB", (W * len(frames) + 4 * (len(frames) - 1), H), "white")
        for j, f in enumerate(frames):
            sheet.paste(f, (j * (W + 4), 0))
        sheet.save(out / "shots" / f"{i:03d}.jpg", quality=85)
        said = " ".join(w["w"] for w in words if s <= w["start"] < e)
        shots.append({
            "id": i, "start": round(s, 3), "end": round(e, 3), "length": round(e - s, 3),
            "observed": {"palette": palette(frames[len(frames) // 2]), "motion_energy": motion_energy(frames), "script": said or None},
            "inferred": {"scene_type": None, "layer": None, "animation": None, "why_here": None},
            "unknown": ["easing exacta", "assets fuente", "fuentes tipográficas exactas"],
        })
    lengths = [x["length"] for x in shots]
    ev = {
        "video": v.name, "duration": round(D, 2),
        "derived": {
            "shots": len(shots), "avg_shot_len": round(float(np.mean(lengths)), 2) if lengths else None,
            "cuts_per_min": round(len(shots) / D * 60, 1), "hook_shots_first_3s": sum(1 for x in shots if x["start"] < 3),
            "high_motion_shots": [x["id"] for x in shots if x["observed"]["motion_energy"] > 12],
        },
        "method": "ffmpeg scene>{} + keyframes 5/plano + paleta cuantizada + energía de movimiento".format(a.threshold),
        "words": words, "shots": shots,
    }
    (out / "evidence.json").write_text(json.dumps(ev, ensure_ascii=False, indent=2))
    cards = [f"# Fichas — {v.name}\n\nCompleta cada ficha mirando `shots/NNN.jpg`. Lo que escribas aquí es INFERENCIA hasta que lo confirmes.\n"]
    for x in shots:
        cards.append(f"""## Plano {x['id']:03d} · {x['start']:.2f}s–{x['end']:.2f}s ({x['length']:.2f}s)
![](shots/{x['id']:03d}.jpg)
- Guion: {x['observed']['script'] or '—'}
- Paleta observada: {' '.join(c['hex'] for c in x['observed']['palette'])} · movimiento: {x['observed']['motion_energy']}
- **Tipo de escena** (schemas/scenes.json):
- **ASSETS** (fondo, objeto, forma, texto, fuentes):
- **EFFECTS** (blur, desaturación, textura, viñeta, glow):
- **ANIMATION** (pop-fade, blur reveal, slide, write-on, cámara; duración y curva):
- **¿Por qué aquí?** (psicología respecto al guion):
""")
    (out / "cards.md").write_text("\n".join(cards))
    tiles = "".join(f'<figure><img src="shots/{x["id"]:03d}.jpg"><figcaption>{x["id"]:03d} · {x["start"]:.1f}s · {x["length"]:.1f}s<br><i>{(x["observed"]["script"] or "")[:90]}</i></figcaption></figure>' for x in shots)
    (out / "board.html").write_text(f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Board {v.stem}</title>
<style>body{{margin:0;padding:16px;background:#111;color:#ddd;font:13px Inter,system-ui}}main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:12px}}figure{{margin:0;background:#1b1b1f;border-radius:10px;padding:8px}}img{{width:100%;border-radius:6px}}</style>
<h2>{v.name} — {len(shots)} planos · ASL {ev['derived']['avg_shot_len']}s · {ev['derived']['cuts_per_min']} cortes/min</h2><main>{tiles}</main>""")
    print(f"[reverse] {len(shots)} planos → {out.relative_to(ROOT)} (evidence.json, cards.md, board.html)")


if __name__ == "__main__":
    main()
