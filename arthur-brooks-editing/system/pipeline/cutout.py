"""Recorta personas/objetos sin fondo (rembg) → media/assets/<ID>_cut.png, para ilustraciones Arthur (principios 7–9).
Uso: python3 pipeline/cutout.py <proyecto> A02 A04 ...   (personas: modelo humano; resto: modelo general)"""
import sys
from pathlib import Path
from PIL import Image
from rembg import remove, new_session
ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "projects" / sys.argv[1] / "media" / "assets"
human, gen = new_session("u2net_human_seg"), new_session("isnet-general-use")
for aid in sys.argv[2:]:
    kind, aid = (aid.split(":") + [""])[:2] if ":" in aid else ("h", aid)
    im = Image.open(p / f"{aid}.png").convert("RGB")
    out = remove(im, session=human if kind == "h" else gen, post_process_mask=True)
    bb = out.getbbox(); out = out.crop(bb)
    out.save(p / f"{aid}_cut.png"); print("✓", aid, out.size)
