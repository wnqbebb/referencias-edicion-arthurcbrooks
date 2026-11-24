#!/usr/bin/env python3
"""Prepara material de estudio por video: hoja índice de planos (fotograma medio + id + tiempo),
hojas de línea de tiempo cada 1.5 s, shots.txt (plano → guion) y subtítulos .srt palabra a palabra agrupados."""
import os
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
STYLE = os.environ.get("VES_STYLE", "arthur-brooks")   # estilo que se está entrenando
REFS = ROOT / "refs" / os.environ.get("VES_REFS", "arthur")  # carpeta con los videos de referencia vNN.mp4
def srt_t(t):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s - int(s)) * 1000):03d}"
for d in sorted((ROOT / "styles" / STYLE / "references").glob("v??")):
    ev = json.loads((d / "evidence.json").read_text()); v = REFS / f"{d.name}.mp4"
    st = d / "study"; st.mkdir(exist_ok=True)
    # 1) índice de planos
    lines = []
    for s in ev["shots"]:
        mid = (s["start"] + s["end"]) / 2
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{mid:.2f}", "-i", str(v), "-frames:v", "1", "-vf",
                        f"scale=200:-2,drawtext=text='{s['id']:03d} {s['start']:.1f}s':x=4:y=4:fontsize=15:fontcolor=yellow:box=1:boxcolor=black@0.7",
                        str(st / f"_m{s['id']:03d}.jpg")], check=True)
        lines.append(f"{s['id']:03d} {s['start']:7.2f}-{s['end']:7.2f} ({s['length']:.1f}s) | {s['observed']['script'] or '—'}")
    n = len(ev["shots"])
    for k in range(0, n, 24):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-start_number", str(k), "-i", str(st / "_m%03d.jpg"), "-frames:v", "1",
                        "-vf", f"tile=8x3:padding=3", str(st / f"shots_{k // 24 + 1:02d}.jpg")], check=True)
    for f in st.glob("_m*.jpg"): f.unlink()
    (st / "shots.txt").write_text("\n".join(lines))
    # 2) línea de tiempo cada 1.5 s
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-vf",
                    "fps=2/3,scale=200:-2,drawtext=text='%{pts\\:hms}':x=4:y=4:fontsize=14:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=8x3:padding=3",
                    str(st / "timeline_%02d.jpg")], check=True)
    # 3) subtítulos
    W = ev["words"]; out = []; i = 0; n_ = 1
    while i < len(W):
        grp = W[i:i + 5]; i += 5
        out.append(f"{n_}\n{srt_t(grp[0]['start'])} --> {srt_t(grp[-1]['end'])}\n{' '.join(w['w'] for w in grp)}\n"); n_ += 1
    (d / f"{d.name}.srt").write_text("\n".join(out))
    (d / "transcript.txt").write_text(" ".join(w["w"] for w in W))
    print(d.name, n, "planos", len(list(st.glob("timeline_*.jpg"))), "hojas")
