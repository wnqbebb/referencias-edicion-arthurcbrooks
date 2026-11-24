#!/usr/bin/env python3
"""Toma los scenes.json de cada video y construye:
  1. skills/arthur-brooks-style/library/<categoria>/<id>.jpg  — hoja de 5 keyframes de la escena (la "animación")
     + <id>.md con su desglose (diseño / efectos / animación / por qué)
  2. styles/arthur-brooks/references/ALL_SCENES.json  — todas las escenas juntas
  3. board_assets/ — fotogramas para el tablero (best_t) de las escenas de inspiración
"""
import os
import json, subprocess
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parent.parent
STYLE = os.environ.get("VES_STYLE", "arthur-brooks")   # estilo que se está entrenando
REFS = ROOT / "refs" / os.environ.get("VES_REFS", "arthur")  # carpeta con los videos de referencia vNN.mp4
REF = ROOT / "styles" / STYLE / "references"
LIB = ROOT / "skills" / f"{STYLE}-style" / "library"
CAT_NAMES = {
    "captions_text": "01 Texto en pantalla (captions)", "broll_text": "02 B-roll + texto + overlay",
    "imagery_characters": "03 Imágenes - personajes + texto", "line_text": "04 Línea + texto",
    "line_illustration": "05 Línea + ilustraciones", "text_centric": "06 Escenas solo texto",
    "center_illustration": "07 Ilustración central + texto", "side_illustration": "08 Ilustración lateral + texto",
    "object_element": "09 Objetos - elementos + texto", "graph_stats": "10 Gráficas y estadística",
    "ui_screen": "11 UI - pantallas", "timeline": "12 Línea de tiempo", "split_layout": "13 Pantalla dividida",
    "title_cta": "14 Título - cierre - CTA", "aroll_plain": "15 A-roll sin texto",
}


DUR = {}
def frame(video, t, out, w):
    if video not in DUR:
        DUR[video] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)], capture_output=True, text=True).stdout)
    t = min(max(0, t), DUR[video] - 0.15)
    for back in (0, 0.5, 1.0, 2.0):
        Path(out).unlink(missing_ok=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(0, t - back):.2f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={w}:-2", "-q:v", "4", str(out)], check=True)
        if Path(out).exists() and Path(out).stat().st_size > 0:
            return


def main():
    allsc = []
    for d in sorted(REF.glob("v??")):
        f = d / "scenes.json"
        if not f.exists():
            print("falta", f); continue
        for s in json.loads(f.read_text()):
            s["video"] = d.name; allsc.append(s)
    (REF / "ALL_SCENES.json").write_text(json.dumps(allsc, ensure_ascii=False, indent=1))
    print(len(allsc), "escenas", Counter(s["category"] for s in allsc))
    board = ROOT / "board_assets"; board.mkdir(exist_ok=True)
    for s in allsc:
        cat = s.get("category", "aroll_plain"); v = REFS / f"{s['video']}.mp4"
        dst = LIB / CAT_NAMES.get(cat, cat); dst.mkdir(parents=True, exist_ok=True)
        st, en = float(s["start"]), float(s["end"])
        # hoja de keyframes (5 momentos de la escena) = cómo se anima
        tmp = []
        for k, fr in enumerate((0.05, 0.25, 0.5, 0.75, 0.95)):
            p = dst / f"_{k}.jpg"; frame(v, st + (en - st) * fr, p, 216); tmp.append(p)
        subprocess.run(["ffmpeg", "-y", "-v", "error", *sum([["-i", str(p)] for p in tmp], []), "-filter_complex", "hstack=inputs=5", str(dst / f"{s['id']}.jpg")], check=True)
        for p in tmp: p.unlink()
        (dst / f"{s['id']}.md").write_text(
            f"# {s['id']} · {CAT_NAMES.get(cat, cat)} · {st:.1f}–{en:.1f}s (calidad {s.get('quality')})\n\n![]({s['id']}.jpg)\n\n"
            f"- **Guion:** {s.get('script','')}\n- **Qué se ve:** {s.get('what','')}\n- **Diseño:** {s.get('design','')}\n"
            f"- **Efectos:** {s.get('effects','')}\n- **Animación:** {s.get('animation','')}\n- **Por qué aquí:** {s.get('why','')}\n")
        if (s.get("quality") or 0) >= 4 and cat != "aroll_plain":
            frame(v, float(s.get("best_t", (st + en) / 2)), board / f"{s['id']}.jpg", 240)
    print("biblioteca:", sum(1 for _ in LIB.rglob("*.jpg")), "hojas · tablero:", len(list(board.glob("*.jpg"))), "fotogramas")


if __name__ == "__main__":
    main()
