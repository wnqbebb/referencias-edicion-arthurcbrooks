#!/usr/bin/env python3
"""VES — Viral Edit System. CLI única y determinista.

Cualquier modelo (Claude, ChatGPT, Gemini) ejecuta EXACTAMENTE los mismos comandos.
El gusto/estilo vive en styles/*/style.json + componentes Remotion, no en el modelo.

  ves.py new        <nombre> --video RAW.mp4 --style premium-clean
  ves.py transcribe <nombre> [--model small] [--lang es]
  ves.py rawcut     <nombre> [--gap 0.35] [--pad 0.03] [--vertical]
  ves.py palette    <nombre> [--preset rosa | --accent #E8559A]
  ves.py storyboard <nombre>                 -> hoja storyboard con zona segura (SIEMPRE antes del render)
  ves.py fork       <nombre> <nuevo> --style X  -> mismo video en otro estilo
  ves.py captions   <nombre>
  ves.py plandoc    <nombre>                 -> plan.html (planificación humana)
  ves.py validate   <nombre>                 -> puerta de calidad (obligatoria)
  ves.py preview    <nombre> --at 1.0,4.5      -> PNGs para revisar escenas
  ves.py render     <nombre> [--draft]
  ves.py sound      <nombre> [--music track.mp3]
  ves.py all        <nombre>                 -> transcribe→rawcut→palette→captions→plandoc
"""
from __future__ import annotations

import argparse
import colorsys
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLES = ROOT / "styles"
PROJECTS = ROOT / "projects"
SCENES = json.loads((ROOT / "schemas" / "scenes.json").read_text())
RENDER = ROOT / "render"

STOPWORDS = set("""a al algo ante antes como con contra cual cuando de del desde donde durante e el ella ellas ellos en entre era es esa ese eso esta este esto fue ha hay la las le les lo los más mas me mi mis muy ni no nos o os para pero por porque que qué se si sí sin sobre su sus te tu tus un una uno unos y ya yo the a an and or but of to in on at for is are was were be been it its this that these those you your we our they their he she his her i me my with as by from so just than then there what which who will would can could do does did not no yes if into up out about have has had""".split())


# ───────────────────────── utilidades ─────────────────────────
def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


def proj(name: str) -> Path:
    p = PROJECTS / name
    if not p.exists():
        sys.exit(f"[ves] proyecto '{name}' no existe. Usa: ves.py new {name} --video ... --style ...")
    return p


def jload(p: Path):
    return json.loads(p.read_text())


def jsave(p: Path, data) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"[ves] escrito {p.relative_to(ROOT)}")


def load_style(style_id: str) -> dict:
    f = STYLES / style_id / "style.json"
    if not f.exists():
        sys.exit(f"[ves] estilo '{style_id}' no existe. Disponibles: {[d.name for d in STYLES.iterdir() if d.is_dir()]}")
    return jload(f)


def probe(video: Path) -> dict:
    out = sh(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(video)]).stdout
    d = json.loads(out)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    num, den = (v["r_frame_rate"].split("/") if v else ("30", "1"))
    return {
        "duration": float(d["format"]["duration"]),
        "width": int(v["width"]) if v else 0,
        "height": int(v["height"]) if v else 0,
        "fps": float(num) / float(den or 1),
        "has_audio": a is not None,
    }


# ───────────────────────── new ─────────────────────────
def cmd_new(a):
    load_style(a.style)
    p = PROJECTS / a.name
    (p / "media").mkdir(parents=True, exist_ok=True)
    (p / "refs").mkdir(exist_ok=True)
    src = Path(a.video).resolve()
    dst = p / "media" / ("raw" + src.suffix.lower())
    shutil.copy2(src, dst)
    meta = {"name": a.name, "style": a.style, "raw": str(dst.relative_to(p)), "probe": probe(dst)}
    jsave(p / "project.json", meta)


# ───────────────────────── transcribe ─────────────────────────
def cmd_transcribe(a):
    p = proj(a.name)
    meta = jload(p / "project.json")
    from faster_whisper import WhisperModel  # import tardío

    import numpy as np

    # decodificamos con ffmpeg (evita incompatibilidades de PyAV) → mono 16 kHz float32
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p / meta["raw"]), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    audio = np.frombuffer(pcm, dtype=np.float32)
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segs, info = model.transcribe(audio, word_timestamps=True, language=a.lang, vad_filter=False)
    words = []
    for s in segs:
        for w in s.words or []:
            words.append({"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3), "p": round(w.probability, 3)})
    jsave(p / "transcript.json", {"language": info.language, "words": words})


# ───────────────────────── rawcut ─────────────────────────
def _norm(w: str) -> str:
    return re.sub(r"[^\wáéíóúñü]", "", w.lower())


def _phrases(words, gap):
    out, cur = [], []
    for w in words:
        if cur and w["start"] - cur[-1]["end"] > gap:
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out


def _drop_bad_takes(phrases):
    """Si una frase empieza igual (3 palabras) que la siguiente, era una toma mala: se queda la última."""
    keep = []
    for i, ph in enumerate(phrases):
        nxt = phrases[i + 1] if i + 1 < len(phrases) else None
        head = [_norm(x["w"]) for x in ph[:3]]
        if nxt and len(ph) >= 3 and head == [_norm(x["w"]) for x in nxt[:3]]:
            print(f"[ves] toma repetida eliminada: '{' '.join(x['w'] for x in ph)}'")
            continue
        keep.append(ph)
    return keep


def cmd_rawcut(a):
    p = proj(a.name)
    meta = jload(p / "project.json")
    tr = jload(p / "transcript.json")
    words = [w for w in tr["words"] if w["w"]]
    if not words:
        sys.exit("[ves] transcript vacío")
    phrases = _drop_bad_takes(_phrases(words, a.gap))
    dur = meta["probe"]["duration"]
    segs = []
    for ph in phrases:
        s, e = max(0.0, ph[0]["start"] - a.pad), min(dur, ph[-1]["end"] + a.pad)
        if segs and s <= segs[-1][1]:
            segs[-1][1] = max(segs[-1][1], e)
        else:
            segs.append([s, e])
    # remapear palabras a la nueva línea de tiempo
    new_words = []
    t_cursor = 0.0
    seg_map = []
    for s, e in segs:
        seg_map.append((s, e, t_cursor))
        t_cursor += e - s
    kept = {id(w) for ph in phrases for w in ph}
    for w in words:
        if id(w) not in kept:
            continue
        for s, e, base in seg_map:
            if s - 1e-3 <= w["start"] <= e + 1e-3:
                new_words.append({**w, "start": round(base + w["start"] - s, 3), "end": round(base + min(w["end"], e) - s, 3)})
                break
    # render con ffmpeg (trim+concat, exacto al frame)
    raw = p / meta["raw"]
    has_a = meta["probe"]["has_audio"]
    parts, labels = [], []
    for i, (s, e) in enumerate(segs):
        parts.append(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS[v{i}]")
        if has_a:
            parts.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0,e-s-0.01):.3f}:d=0.01[a{i}]")
            labels.append(f"[v{i}][a{i}]")
        else:
            labels.append(f"[v{i}]")
    vf_tail = ""
    if a.vertical:
        W, H = 1080, 1920
        vf_tail = f";[vc]crop='min(iw,ih*9/16)':ih,scale={W}:{H}[vout]"
    concat = f"{''.join(labels)}concat=n={len(segs)}:v=1:a={1 if has_a else 0}[vc]{'[ac]' if has_a else ''}"
    fc = ";".join(parts) + ";" + concat + vf_tail
    out = p / "media" / "raw_cut.mp4"
    vmap = "[vout]" if a.vertical else "[vc]"
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-filter_complex", fc, "-map", vmap]
    if has_a:
        cmd += ["-map", "[ac]", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", str(out)]
    sh(cmd)
    removed = dur - t_cursor
    print(f"[ves] raw cut: {dur:.1f}s → {t_cursor:.1f}s (−{removed:.1f}s, {len(segs)} segmentos)")
    jsave(p / "transcript_cut.json", {"language": tr.get("language"), "words": new_words, "segments": segs})
    meta["cut"] = "media/raw_cut.mp4"
    meta["cut_probe"] = probe(out)
    jsave(p / "project.json", meta)


# ───────────────────────── palette ─────────────────────────
def _hex(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(c * 255)))) for c in rgb)


def build_palette(hue: float, sat: float) -> dict:
    s = max(0.55, min(0.95, sat))
    return {
        "vibrant_bright": _hex(colorsys.hls_to_rgb(hue, 0.58, s)),
        "vibrant_dark": _hex(colorsys.hls_to_rgb(hue, 0.28, s)),
        "dull_white": _hex(colorsys.hls_to_rgb(hue, 0.95, 0.12)),
        "dull_black": _hex(colorsys.hls_to_rgb(hue, 0.07, 0.10)),
    }


def cmd_palette(a):
    """Regla del creador: mirar el A-roll, encontrar el color que destaca, sacar 2 vibrantes (claro/oscuro) y 2 apagados (blanco/negro)."""
    import numpy as np
    from PIL import Image

    p = proj(a.name)
    meta = jload(p / "project.json")
    style = load_style(meta["style"])
    if getattr(a, "preset", None) or getattr(a, "accent", None):  # color por público/marca (ej. rosa para una mujer)
        hexc = a.accent or jload(STYLES / "palette_presets.json")[a.preset]
        r, g, b_ = [int(hexc[i : i + 2], 16) / 255 for i in (1, 3, 5)]
        hh, ll, ss = colorsys.rgb_to_hls(r, g, b_)
        pal = build_palette(hh, ss)
        jsave(p / "palette.json", {"source": f"override:{a.preset or a.accent}", "colors": pal, "options": [pal]})
        return
    if style["palette"]["mode"] == "fixed":
        pal = style["palette"]["fixed"]
        jsave(p / "palette.json", {"source": "style.fixed", "colors": pal, "options": [pal]})
        return
    vid = p / meta.get("cut", meta["raw"])
    tmp = p / "media" / "_pal"
    tmp.mkdir(exist_ok=True)
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(vid), "-vf", "fps=1/2,scale=160:-1", str(tmp / "f%03d.png")])
    px = np.concatenate([np.asarray(Image.open(f).convert("RGB")).reshape(-1, 3) for f in sorted(tmp.glob("*.png"))]) / 255.0
    shutil.rmtree(tmp)
    hls = np.array([colorsys.rgb_to_hls(*c) for c in px[:: max(1, len(px) // 60000)]])
    m = (hls[:, 2] > 0.35) & (hls[:, 1] > 0.18) & (hls[:, 1] < 0.85)  # píxeles con color real
    options = []
    if m.sum() > 50:
        h = hls[m]
        hist, edges = np.histogram(h[:, 0], bins=24, range=(0, 1), weights=h[:, 2])
        for b in np.argsort(hist)[::-1][:3]:
            sel = (h[:, 0] >= edges[b]) & (h[:, 0] < edges[b + 1])
            options.append(build_palette(float(np.median(h[sel, 0])), float(np.median(h[sel, 2]))))
    if not options:
        r, g, b_ = [int(style["palette"]["fallback_accent"][i : i + 2], 16) / 255 for i in (1, 3, 5)]
        hh, ll, ss = colorsys.rgb_to_hls(r, g, b_)
        options = [build_palette(hh, ss)]
    jsave(p / "palette.json", {"source": "footage", "colors": options[0], "options": options,
                               "note": "Elige opción: edita 'colors' o pon palette en edit_plan.json"})


# ───────────────────────── captions ─────────────────────────
SPLIT_BEFORE = set("de del que y o para con en a al porque pero sin por como cuando si donde and or but to with for because that when if of in".split())


def chunk_captions(words, max_words: int, gap: float = 0.35):
    """Frases como las corta Arthur: por sentido (puntuación y pausas), máx. max_words, cortes antes de
    palabras funcionales y nunca una palabra huérfana."""
    clauses, cur = [], []
    for w in words:
        if cur and (w["start"] - cur[-1]["end"] > gap or re.search(r"[.!?,;:]$", cur[-1]["w"]) or re.match(r"[¿¡]", w["w"])):
            clauses.append(cur); cur = []
        cur.append(w)
    if cur:
        clauses.append(cur)
    phrases = []
    for cl in clauses:
        n = len(cl)
        if n <= max_words:
            phrases.append(cl); continue
        k = -(-n // max_words)
        cuts, last = [], 0
        for part in range(1, k):
            ideal = round(n * part / k)
            best = min(range(max(last + 2, ideal - 2), min(n - 1, ideal + 2) + 1),
                       key=lambda c: abs(c - ideal) - (1.5 if _norm(cl[c]["w"]) in SPLIT_BEFORE else 0) + (3 if re.search(r"\d", cl[c - 1]["w"]) else 0), default=ideal)
            cuts.append(best); last = best
        prev = 0
        for c in cuts + [n]:
            phrases.append(cl[prev:c]); prev = c
    # huérfanas: una palabra sola se une a su frase (hacia atrás si sigue la misma oración, si no hacia adelante)
    out, carry = [], []
    for ph in phrases:
        ph = carry + ph; carry = []
        if len(ph) == 1 and out and not re.search(r"[.!?]$", out[-1][-1]["w"]) and not re.match(r"[¿¡]", ph[0]["w"]) and len(out[-1]) < max_words + 1:
            out[-1] = out[-1] + ph
        elif len(ph) == 1 and (re.match(r"[¿¡]", ph[0]["w"]) or not out or re.search(r"[.!?]$", out[-1][-1]["w"])):
            carry = ph
        else:
            out.append(ph)
    if carry:
        if out: out[-1] = out[-1] + carry
        else: out.append(carry)
    return out


def pick_special(phrase, forced: set[str]) -> list[int]:
    idx = [i for i, w in enumerate(phrase) if _norm(w["w"]) in forced]
    if idx:
        return idx[:2]
    cands = [(len(_norm(w["w"])) + (10 if re.search(r"\d", w["w"]) else 0), i) for i, w in enumerate(phrase) if _norm(w["w"]) not in STOPWORDS]
    if not cands:
        return []
    i = max(cands)[1]
    w = phrase[i]["w"]
    if w[:1].isupper() and i > 0 and phrase[i - 1]["w"][:1].isupper() and _norm(phrase[i - 1]["w"]) not in STOPWORDS:
        return [i - 1, i]
    if w[:1].isupper() and i + 1 < len(phrase) and phrase[i + 1]["w"][:1].isupper():
        return [i, i + 1]
    return [i]


def merge_symbols(words):
    """Une tokens que son solo símbolos (%, $, €) a la palabra anterior: '90' '%' → '90%'."""
    out = []
    for w in words:
        if out and re.fullmatch(r"[%$€.,!?]+", w["w"]):
            out[-1] = {**out[-1], "w": out[-1]["w"] + w["w"], "end": w["end"]}
        else:
            out.append(dict(w))
    return out


def cmd_captions(a):
    p = proj(a.name)
    meta = jload(p / "project.json")
    style = load_style(meta["style"])
    tr = jload(p / ("transcript_cut.json" if (p / "transcript_cut.json").exists() else "transcript.json"))
    forced = set()
    plan_f = p / "edit_plan.json"
    if plan_f.exists():
        forced = {_norm(x) for x in jload(plan_f).get("captions", {}).get("special_words", [])}
    out, sentence, hist = [], 0, []
    mode = style["captions"].get("mode", "cinematic")
    for ph in chunk_captions(merge_symbols(tr["words"]), style["captions"]["max_words"]):
        sp = pick_special(ph, forced)
        treatment = None
        if mode in ("doc", "arthur") and sp:
            # v01: el bloque grande es CONTIGUO (1–3 palabras): 'zero dollars', 'my dream', 'career down'
            i = sp[0]
            span = [i]
            if i + 1 < len(ph) and _norm(ph[i + 1]["w"]) not in STOPWORDS and len(_norm(ph[i + 1]["w"])) >= 5 and not re.search(r"[.,!?]$", ph[i]["w"]):
                span.append(i + 1)
            elif i > 0 and _norm(ph[i - 1]["w"]) in {"my", "mi", "un", "una", "tu", "tus"}:
                span.insert(0, i - 1)
            sp = span
            # tratamiento: frase de ≥2 palabras → serif itálica; 1 palabra → bold sans; nunca 3 iguales seguidas
            treatment = "serif" if len(sp) >= 2 else "sans"
            if len(hist) >= 2 and hist[-1] == hist[-2] == treatment:
                treatment = "sans" if treatment == "serif" else "serif"
            hist.append(treatment)
        box = mode == "arthur" and treatment == "serif" and hist.count("serif") % 4 == 0  # caja de acento 1 de cada 4 serif
        out.append({"start": ph[0]["start"], "end": ph[-1]["end"], "sentence": sentence, "treatment": treatment, "box": box,
                    "words": [{"w": w["w"], "start": w["start"], "end": w["end"]} for w in ph], "special": sp})
        if re.search(r"[.!?]$", ph[-1]["w"]):
            sentence += 1
    for i in range(len(out) - 1):  # el caption dura hasta que empieza el siguiente (máx +0.4s)
        out[i]["end"] = round(min(out[i + 1]["start"], out[i]["end"] + 0.4), 3)
    place_captions(p, style, out)
    jsave(p / "captions.json", {"phrases": out})


def facetrack(p: Path, video: Path, fps: float = 4.0) -> list:
    """Cara por tiempo (Haar frontal+perfil) → [{t, x, y, w, h}] en px del video de salida (1080x1920)."""
    import cv2
    import numpy as np
    cache = p / "facetrack.json"
    if cache.exists():
        return jload(cache)
    cas = [cv2.CascadeClassifier(cv2.data.haarcascades + n) for n in ("haarcascade_frontalface_default.xml", "haarcascade_profileface.xml")]
    W, H = 360, 640
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", f"fps={fps},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    F = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
    track, k = [], 1080 / W
    for i, g in enumerate(F):
        boxes = []
        for c in cas:
            boxes += [tuple(b) for b in c.detectMultiScale(g, 1.1, 5, minSize=(40, 40))]
        if boxes:
            x, y, w, h = max(boxes, key=lambda b: b[2] * b[3])
            track.append({"t": round(i / fps, 2), "x": int(x * k), "y": int(y * k), "w": int(w * k), "h": int(h * k)})
    jsave(cache, track)
    return track


def place_captions(p: Path, style: dict, phrases: list) -> None:
    """Regla: centrado horizontal, cerca de la mitad, PERO nunca sobre la boca/mentón.
    El bloque del caption (alto estimado) se coloca bajo el mentón + margen; si no cabe dentro
    de la zona segura inferior, se sube sobre la cabeza. Guarda y_center (px) por frase."""
    meta = jload(p / "project.json")
    video = p / meta.get("cut", meta["raw"])
    track = facetrack(p, video)
    H = style["format"]["height"]
    c = style["captions"]
    base = c["base_size"]
    block = base * (c.get("special_scale", 1.6) + 1.4)  # alto aprox: palabra grande + línea pequeña arriba y abajo
    safe_bottom = H * (1 - style.get("safe_zone", {}).get("bottom", 0.22))
    safe_top = H * style.get("safe_zone", {}).get("top", 0.12)
    want = H * c.get("center_y", 0.6)
    for ph in phrases:
        fs = [f for f in track if ph["start"] - 0.25 <= f["t"] <= ph["end"] + 0.25]
        if not fs:
            ph["y"] = round(want); continue
        chin = max(f["y"] + f["h"] * 1.18 for f in fs)  # la caja Haar llega a la boca; +18% ≈ mentón
        head = min(f["y"] - f["h"] * 0.25 for f in fs)
        y = max(want, chin + 30 + block / 2)
        if y + block / 2 > safe_bottom:  # no cabe debajo → arriba de la cabeza
            y = min(want, head - 30 - block / 2)
            if y - block / 2 < safe_top:
                y = safe_bottom - block / 2  # último recurso: lo más abajo posible dentro de la zona segura
        ph["y"] = round(y)


# ───────────────────────── plandoc ─────────────────────────
RECO_RULES = [
    (r"\b(\d+|uno|dos|tres|cuatro|cinco|one|two|three|four|five)\b.*\b(pasos|steps|claves|keys|formas|ways|reglas|rules|tipos|types)\b", ["listicle", "list_card", "line_text"]),
    (r"\d+ ?%|\bpor ciento\b|percent|\b\d{2,}\b", ["counter_ring", "bar_graph", "line_graph"]),
    (r"\b(vs|versus|antes|después|before|after|pero|but|en cambio|instead)\b", ["before_after", "two_object", "bar_graph"]),
    (r"\b(sube|subir|crece|grow|up|más y más|aumenta|baja|cae|drop)\b", ["line_graph", "bar_graph"]),
    (r"\b(stripe|youtube|instagram|tiktok|google|apple|nvidia|chatgpt|claude|gemini|app|pago|payment|dinero|money|\$)\b", ["notification", "counter_ring"]),
    (r"\?", ["fullscreen_text", "two_object", "quote"]),
    (r"\b(dijo|said|cita|quote)\b|\"", ["quote", "fullscreen_text"]),
    (r"\b(mi padre|mi papá|my dad|historia|story|me enamoré|fell in love|persona|person)\b", ["broll_text", "painting", "object_callout"]),
    (r"\b(vida|life|alma|soul|propósito|calling|sentido|meaning)\b", ["painting", "center_illustration", "quote"]),
]


def recommend(text: str, allowed: list[str], position: int) -> list[str]:
    t = text.lower()
    recs = []
    if position == 0:
        recs += ["notification", "listicle", "two_object", "fullscreen_text"]
    for pat, scenes in RECO_RULES:
        if re.search(pat, t):
            recs += scenes
    recs += ["aroll", "fullscreen_text", "broll_text"]
    seen, out = set(), []
    for r in recs:
        if r in allowed and r not in seen:
            seen.add(r)
            out.append(r)
    return out[:4]


def cmd_plandoc(a):
    p = proj(a.name)
    meta = jload(p / "project.json")
    style = load_style(meta["style"])
    tr = jload(p / ("transcript_cut.json" if (p / "transcript_cut.json").exists() else "transcript.json"))
    lines = chunk_captions(tr["words"], 12, gap=0.45)  # líneas de guion (más largas que captions)
    rows = []
    for i, ln in enumerate(lines):
        text = " ".join(w["w"] for w in ln)
        rows.append({"i": i, "start": ln[0]["start"], "end": ln[-1]["end"], "text": text,
                     "reco": recommend(text, style["scenes_allowed"], i)})
    tpl = (ROOT / "pipeline" / "plandoc_template.html").read_text()
    video_rel = os.path.relpath(p / meta.get("cut", meta["raw"]), p)
    html = (tpl.replace("__ROWS__", json.dumps(rows, ensure_ascii=False))
               .replace("__SCENES__", json.dumps({k: v["use_when"] for k, v in SCENES.items() if k in style["scenes_allowed"]}, ensure_ascii=False))
               .replace("__STYLE__", style["name"]).replace("__VIDEO__", video_rel).replace("__PROJECT__", a.name))
    (p / "plan.html").write_text(html)
    print(f"[ves] escrito projects/{a.name}/plan.html — ábrelo, planifica, pulsa 'Copiar plan' y pégalo al modelo.")


# ───────────────────────── validate (puerta de calidad) ─────────────────────────
def validate_plan(plan: dict, style: dict, duration: float | None) -> tuple[list[str], list[str], dict]:
    errs, warns = [], []
    allowed = set(style["scenes_allowed"])
    scenes = sorted(plan.get("scenes", []), key=lambda s: s["start"])
    ids = set()
    pace = style["pacing"]
    for s in scenes:
        sid = s.get("id", "?")
        if sid in ids:
            errs.append(f"{sid}: id duplicado")
        ids.add(sid)
        t = s.get("type")
        if t not in SCENES:
            errs.append(f"{sid}: tipo '{t}' no existe en schemas/scenes.json")
            continue
        if t not in allowed:
            errs.append(f"{sid}: tipo '{t}' no permitido en estilo {style['id']} (permitidos: {sorted(allowed)})")
        if s["end"] - s["start"] < pace["min_scene_s"]:
            errs.append(f"{sid}: dura {s['end']-s['start']:.2f}s < mínimo {pace['min_scene_s']}s")
        if duration and s["end"] > duration + 0.05:
            errs.append(f"{sid}: termina en {s['end']}s, después del video ({duration:.2f}s)")
        lim, pr = SCENES[t]["limits"], s.get("props", {})
        for key in ("text", "body"):
            if key in pr and "max_words" in lim and len(str(pr[key]).split()) > lim["max_words"]:
                errs.append(f"{sid}: '{key}' tiene {len(str(pr[key]).split())} palabras > {lim['max_words']} (menos texto = más premium)")
        if "special" in pr:
            sp = pr["special"]
            if len(sp) > lim.get("special_max", 2):
                errs.append(f"{sid}: demasiadas palabras especiales ({len(sp)})")
            for w in sp:
                if _norm(w) not in [_norm(x) for x in str(pr.get("text") or pr.get("label") or "").split()]:
                    errs.append(f"{sid}: palabra especial '{w}' no está en text")
        if "items" in pr and "max_items" in lim and len(pr["items"]) > lim["max_items"]:
            errs.append(f"{sid}: {len(pr['items'])} items > {lim['max_items']}")
        paths = []
        for k in ("media", "image"):
            v = pr.get(k)
            paths += v if isinstance(v, list) else ([v] if v else [])
        paths += [it.get("media") for it in pr.get("items", []) if isinstance(it, dict) and it.get("media")]
        for m in paths:
            if not str(m).startswith(("http", "frame:")) and not (PROJECTS / plan.get("_project", "") / m).exists():
                warns.append(f"{sid}: asset '{m}' no encontrado (asset list pendiente)")
    # solapes entre escenas fullscreen
    fs = [s for s in scenes if SCENES.get(s.get("type"), {}).get("layer") == "fullscreen"]
    for x, y in zip(fs, fs[1:]):
        if y["start"] < x["end"] - 1e-3:
            errs.append(f"{x['id']}/{y['id']}: escenas fullscreen se solapan")
    # racha de A-roll sin estímulo visual
    is_vis = lambda s: s.get("type") != "aroll" or s.get("props", {}).get("zoom") or s.get("props", {}).get("desaturate")  # un punch-in también es evento visual
    visual = sorted([(s["start"], s["end"]) for s in scenes if is_vis(s)])
    streak, t = 0.0, 0.0
    worst = (0.0, 0.0)
    for s, e in visual + [((duration or t), (duration or t))]:
        if s - t > worst[0]:
            worst = (s - t, t)
        t = max(t, e)
    if worst[0] > pace["max_aroll_streak_s"] + 0.01:
        errs.append(f"racha de A-roll sin visual de {worst[0]:.1f}s desde {worst[1]:.1f}s > {pace['max_aroll_streak_s']}s (añade un pop/overlay)")
    # hook
    hook = [s for s in scenes if s["start"] < pace["hook_window_s"] and (s.get("type") != "aroll" or s.get("props", {}).get("zoom"))]
    if not hook:
        errs.append(f"hook: no hay visual en los primeros {pace['hook_window_s']}s (fórmula speaker + texto + visual)")
    # cuota de animación
    stats = {}
    if duration:
        covered = sum(s["end"] - s["start"] for s in scenes if SCENES.get(s.get("type"), {}).get("layer") == "fullscreen")
        share = covered / duration
        stats = {"duration": round(duration, 2), "fullscreen_share": round(share, 2), "scenes": len(scenes)}
        tgt = pace["target_animation_share"]
        if abs(share - tgt) > 0.25:
            warns.append(f"cuota fullscreen {share:.0%} lejos del objetivo del estilo {tgt:.0%}")
    return errs, warns, stats


def cmd_validate(a):
    p = proj(a.name)
    meta = jload(p / "project.json")
    plan = jload(p / "edit_plan.json")
    plan["_project"] = a.name
    style = load_style(plan.get("style", meta["style"]))
    dur = meta.get("cut_probe", meta["probe"])["duration"]
    errs, warns, stats = validate_plan(plan, style, dur)
    for w in warns:
        print("  ⚠", w)
    for e in errs:
        print("  ✗", e)
    print(f"[ves] stats {stats}")
    if errs:
        sys.exit(f"[ves] PLAN RECHAZADO: {len(errs)} errores. Corrige edit_plan.json y vuelve a validar.")
    print("[ves] PLAN OK ✓ — listo para render")


# ───────────────────────── render ─────────────────────────
def resolve_media(plan: dict, p: Path, pub: Path) -> None:
    """Asset pendiente → usa su "fallback" si existe; si no, genera un placeholder visible (id + descripción)
    para que la vista previa muestre DÓNDE irá cada asset que falta entregar."""
    from PIL import Image, ImageDraw, ImageFont
    man = {a["id"]: a for a in plan.get("assets", [])}
    fb = plan.get("fallbacks", {})
    def fix(m):
        if not isinstance(m, str) or m.startswith("http") or (p / m).exists():
            return m
        aid = Path(m).stem.split("_")[0]
        if fb.get(aid) and (p / fb[aid]).exists():
            return fb[aid]
        ph = pub / "media" / "_ph" / f"{aid}.png"; ph.parent.mkdir(parents=True, exist_ok=True)
        im = Image.new("RGB", (1080, 1350), "#2a2a2e"); d = ImageDraw.Draw(im)
        f = ImageFont.truetype(str(RENDER / "public/fonts/Anton.ttf"), 90); g = ImageFont.truetype(str(RENDER / "public/fonts/Anton.ttf"), 44)
        d.rectangle([20, 20, 1060, 1330], outline="#888", width=6)
        d.text((80, 520), f"ASSET {aid}", font=f, fill="#fff")
        d.text((80, 650), (man.get(aid, {}).get("subject") or m)[:40], font=g, fill="#bbb")
        im.save(ph)
        return f"media/_ph/{aid}.png"
    for s in plan.get("scenes", []):
        pr = s.get("props", {})
        for k in ("media", "image"):
            if isinstance(pr.get(k), list): pr[k] = [fix(x) for x in pr[k]]
            elif pr.get(k): pr[k] = fix(pr[k])
        for k in ("images",):
            if isinstance(pr.get(k), list): pr[k] = [fix(x) for x in pr[k]]
        for it in pr.get("items", []):
            if isinstance(it, dict) and it.get("media"): it["media"] = fix(it["media"])


# ── fluidez entre escenas (revisión del cliente: "las transiciones se veían forzadas") ─────────────────────────────
VISUAL_LEAD = {"j_broll", "j_painting", "j_illus", "painting", "broll_text", "arthur_broll", "paper_collage", "archival_photo", "video_card", "name_card", "arthur_icons", "arthur_orbit", "arthur_stripes"}
DECOR_TRANS = {"whip", "glitch_blocks", "light_leak", "flash_tint", "flash_white", "zoom_blur", "invert_sandwich", "wipe", "iris", "ink_wipe"}


def fluidity(plan, words, style):
    """Ajusta el plan ANTES del render (no toca edit_plan.json):
    1) inicio de cada escena = inicio de la palabra más cercana (±0.35 s); las imágenes entran 0.12 s antes (Arthur: 0.1–0.3 s),
       el texto 1 frame antes; 2) el final cae en el inicio de la palabra que abre la frase siguiente (corte en palabra
       funcional, nunca a mitad de palabra); 3) huecos de A-roll < 0.6 s entre dos escenas se cierran (sin destellos de cara);
       4) transiciones decorativas solo las permitidas por el estilo y separadas ≥ min_gap_s; el resto, corte seco."""
    starts = [w["start"] for w in words]
    def snap(t, lim=0.35):
        best = min(starts, key=lambda x: abs(x - t)) if starts else t
        return best if abs(best - t) <= lim else t
    tr = style.get("transitions", {})
    allowed = set(tr.get("allowed", ["crossfade"]))
    gap = tr.get("min_gap_s", 8.0)
    sc = sorted(plan.get("scenes", []), key=lambda s: s["start"])
    for s in sc:
        if s["type"] == "aroll":
            s["start"] = round(snap(s["start"]), 3); s["end"] = round(snap(s["end"]), 3); continue
        lead = 0.12 if s["type"] in VISUAL_LEAD else 0.034
        s["start"] = round(max(0, snap(s["start"]) - lead), 3)
        s["end"] = round(max(s["start"] + 0.5, snap(s["end"]) - 0.034), 3)
    full = [s for s in sc if s["type"] != "aroll"]
    for a_, b_ in zip(full, full[1:]):
        if 0 < b_["start"] - a_["end"] < 0.6:
            a_["end"] = b_["start"]; a_.pop("out", None); b_.pop("in", None)
        if a_["end"] > b_["start"]:
            a_["end"] = b_["start"]
    last = -99.0
    for s in sc:
        for k in ("in", "out"):
            t = s["start"] if k == "in" else s["end"]
            v = s.get(k)
            if not v or v not in DECOR_TRANS:
                continue
            if v not in allowed or t - last < gap:
                s.pop(k)
            else:
                last = t
    cuts = []
    for c in plan.get("cuts", []):
        if c.get("type") in allowed and c["t"] - last >= gap:
            cuts.append(c); last = c["t"]
    plan["cuts"] = cuts
    plan["scenes"] = sc
    return plan


def cmd_render(a):
    p = proj(a.name)
    meta = jload(p / "project.json")
    plan = jload(p / "edit_plan.json")
    style = load_style(plan.get("style", meta["style"]))
    plan["_project"] = a.name
    errs, _, _ = validate_plan(plan, style, meta.get("cut_probe", meta["probe"])["duration"])
    if errs and not a.force:
        sys.exit("[ves] el plan no pasa validate; no se renderiza (usa --force solo para depurar)")
    pal = plan.get("palette") or (jload(p / "palette.json")["colors"] if (p / "palette.json").exists() else build_palette(0.6, 0.8))
    caps = jload(p / "captions.json") if (p / "captions.json").exists() else {"phrases": []}
    # assets del proyecto → render/public/<proyecto>
    # solo el proyecto actual en public/ (el bundle copia public entero) y sin originales pesados
    for d in (RENDER / "public").iterdir():
        if d.is_dir() and d.name not in ("fonts", "textures"):
            shutil.rmtree(d)
    pub = RENDER / "public" / a.name
    shutil.copytree(p, pub, ignore=shutil.ignore_patterns("out", "*.html", "_*", "stock", "cand", "raw.*"))
    video = meta.get("cut", meta["raw"])
    dur = meta.get("cut_probe", meta["probe"])["duration"]
    resolve_media(plan, p, pub)
    tw = jload(p / ("transcript_cut.json" if (p / "transcript_cut.json").exists() else "transcript.json"))["words"]
    plan = fluidity(plan, tw, style)
    # texturas propias del proyecto (assets entregados) reemplazan a las genéricas del estilo
    if plan.get("textures"):
        style = dict(style, texture=dict(style.get("texture", {}), files={k: f"{a.name}/{v}" for k, v in plan["textures"].items()}))
    props = {"project": a.name, "video": f"{a.name}/{video}", "duration": dur, "style": style,
             "palette": pal, "plan": plan, "captions": caps["phrases"]}
    (p / "out").mkdir(exist_ok=True)
    pf = p / "out" / "props.json"
    pf.write_text(json.dumps(props, ensure_ascii=False))
    if getattr(a, "at", None):  # previews: fotogramas sueltos para revisión rápida
        ts = ",".join(f"{float(x):.2f}" for x in a.at.split(","))
        subprocess.run(["node", "render.mjs", str(pf), str(p / "out" / "still_{t}.png"), f"--still={ts}"], cwd=RENDER, check=True)
        return
    ok = (p / "APPROVED").exists() and (p / "APPROVED").read_text().strip() == _approval_hash(p)
    if not ok and not a.force and not getattr(a, "draft", False):  # el borrador (½ res.) es para revisar, el final exige aprobación
        sys.exit("[ves] ⛔ SIN APROBACIÓN: muestra al humano storyboard + caption_sheet + paleta y espera su OK (ves.py approve). No se renderiza.")
    out = p / "out" / ("draft.mp4" if a.draft else "edit.mp4")
    cmd = ["node", "render.mjs", str(pf), str(out)] + (["--draft"] if a.draft else [])
    print("[ves] renderizando…", " ".join(cmd))
    subprocess.run(cmd, cwd=RENDER, check=True)
    print(f"[ves] ✓ {out.relative_to(ROOT)}")


# ───────────────────────── sound ─────────────────────────
def cmd_sound(a):
    p = proj(a.name)
    meta = jload(p / "project.json")
    plan = jload(p / "edit_plan.json")
    style = load_style(plan.get("style", meta["style"]))
    caps = jload(p / "captions.json")["phrases"] if (p / "captions.json").exists() else []
    sfx_dir = ROOT / "assets" / "sfx"
    if not any(sfx_dir.glob("*.wav")):
        subprocess.run([sys.executable, str(ROOT / "pipeline" / "sfxgen.py"), str(sfx_dir)], check=True)
    a.music = a.music or plan.get("music", {}).get("file")  # la pista elegida con pick-music
    if a.music and not Path(a.music).exists():
        print(f"[ves] ⚠ no encuentro la música {a.music} (descárgala con: node pipeline/gen/fetch_music.mjs). Mezclo sin música.")
        a.music = None
    cues = []
    for s in plan["scenes"]:
        name = style["sfx"].get(s["type"])
        if name:
            cues.append({"t": round(max(0, s["start"] - (0.12 if name.startswith("whoosh") else 0)), 3), "sfx": name, "scene": s["id"], "gain": 0.55})
    if style["sfx"].get("caption_special"):
        for ph in caps:
            t = ph["words"][ph["special"][0]]["start"] if ph["special"] else None
            # clic solo en palabras clave espaciadas (≥2.5 s de cualquier otro sonido): ritmo, no ruido
            if t is not None and all(abs(c["t"] - t) >= 2.5 for c in cues):
                cues.append({"t": t, "sfx": style["sfx"]["caption_special"], "scene": None, "gain": 0.22})
    cues.sort(key=lambda c: c["t"])
    # densidad máxima medida en las referencias (Arthur: ~1 SFX cada 10–20 s; la música hace el trabajo)
    gap = style["sfx"].get("min_gap_s")
    if gap:
        kept = []
        for c in sorted(cues, key=lambda c: (c["scene"] is None, c["t"])):  # prioridad: cambios de escena
            if all(abs(c["t"] - k["t"]) >= gap for k in kept):
                kept.append(c)
        cues = sorted(kept, key=lambda c: c["t"])
    jsave(p / "cue_sheet.json", {"cues": cues, "music": a.music, "mood": style["music"]["mood"]})
    src = p / "out" / ("draft.mp4" if getattr(a, "draft", False) else "edit.mp4")
    if not src.exists():
        sys.exit("[ves] cue sheet listo; renderiza primero (ves.py render) para mezclar")
    inputs = ["-i", str(src)]
    filt, labels = [], []
    for i, c in enumerate(cues):
        inputs += ["-i", str(sfx_dir / f"{c['sfx']}.wav")]
        ms = int(c["t"] * 1000)
        filt.append(f"[{i+1}:a]adelay={ms}|{ms},volume={c['gain']}[s{i}]")
        labels.append(f"[s{i}]")
    n = len(cues)
    music_in = ""
    if a.music:
        inputs += ["-stream_loop", "-1", "-i", a.music]
        mi = n + 1
        filt.append(f"[{mi}:a]volume={plan.get('music', {}).get('volume', 0.18)}[mraw]")
        filt.append("[mraw][0:a]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[m]")
        music_in = "[m]"
    mix_n = 1 + n + (1 if a.music else 0)
    filt.append(f"[0:a]{''.join(labels)}{music_in}amix=inputs={mix_n}:normalize=0:duration=first,alimiter=limit=0.9,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    out = p / "out" / ("BORRADOR.mp4" if getattr(a, "draft", False) else "master.mp4")
    sh(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", str(out)])
    print(f"[ves] ✓ master con {n} SFX: {out.relative_to(ROOT)}")
    # versión liviana para subir a redes (~3× menos peso, misma calidad visible en el celular)
    web = out.with_name(out.stem + "_web.mp4")
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-profile:v", "high",
        "-pix_fmt", "yuv420p", "-maxrate", "8M", "-bufsize", "16M", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(web)])
    print(f"[ves] ✓ comprimido para redes: {web.relative_to(ROOT)} ({web.stat().st_size / 1048576:.1f} MB)")


def cmd_storyboard(a):
    """Hoja storyboard: 1 fotograma por escena (+ captions de A-roll), guía de zona segura,
    y explicación de qué se ve y cómo está hecho (ASSETS / EFFECTS / ANIMATION / POR QUÉ)."""
    from PIL import Image, ImageDraw
    p = proj(a.name)
    meta = jload(p / "project.json")
    plan = jload(p / "edit_plan.json")
    style = load_style(plan.get("style", meta["style"]))
    tr = jload(p / ("transcript_cut.json" if (p / "transcript_cut.json").exists() else "transcript.json"))["words"]
    scenes = sorted(plan["scenes"], key=lambda s: s["start"])
    times = [round(s["start"] + min(0.9 * (s["end"] - s["start"]), max(0.6, 0.55 * (s["end"] - s["start"]))), 2) for s in scenes]
    cmd_render(argparse.Namespace(name=a.name, at=",".join(str(t) for t in times), force=a.force, draft=False))
    sz = style.get("safe_zone", {})
    rows = []
    for s, t in zip(scenes, times):
        f = p / "out" / f"still_{t:06.2f}.png"
        im = Image.open(f).convert("RGB")
        W, H = im.size
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        x0, y0, x1, y1 = W * sz.get("left", 0), H * sz.get("top", 0), W * (1 - sz.get("right", 0)), H * (1 - sz.get("bottom", 0))
        d.rectangle([0, 0, W, y0], fill=(255, 0, 80, 70)); d.rectangle([0, y1, W, H], fill=(255, 0, 80, 70))
        d.rectangle([0, y0, x0, y1], fill=(255, 0, 80, 70)); d.rectangle([x1, y0, W, y1], fill=(255, 0, 80, 70))
        d.rectangle([x0, y0, x1, y1], outline=(0, 255, 160, 255), width=4)
        for k in (1, 2):  # tercios
            d.line([0, H * k / 3, W, H * k / 3], fill=(255, 255, 255, 90), width=2); d.line([W * k / 3, 0, W * k / 3, H], fill=(255, 255, 255, 90), width=2)
        sb = p / "out" / "storyboard"; sb.mkdir(exist_ok=True)
        out = sb / f"{s['id']}.jpg"
        Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB").resize((W // 2, H // 2)).save(out, quality=85)
        said = " ".join(w["w"] for w in tr if s["start"] <= w["start"] < s["end"])
        sc = SCENES.get(s["type"], {})
        rows.append(f"""<article><img src="storyboard/{s['id']}.jpg"><div><h3>{s['id']} · {s['type']} <small>{s['start']:.2f}s → {s['end']:.2f}s ({s['end']-s['start']:.1f}s)</small></h3>
<p class=q>“{said}”</p><dl><dt>Qué se ve</dt><dd><code>{json.dumps(s.get('props', {}), ensure_ascii=False)}</code></dd>
<dt>Capa</dt><dd>{sc.get('layer')}</dd><dt>Animación</dt><dd>entrada {style['motion']['enter_ms']} ms, curva cubic-bezier{tuple(style['motion']['easing'])}, salida {style['motion']['exit_ms']} ms · SFX: {style['sfx'].get(s['type'])}</dd>
<dt>Por qué aquí</dt><dd>{sc.get('use_when','')}</dd></dl></div></article>""")
    html = f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Storyboard {a.name}</title>
<style>body{{margin:0;padding:20px;background:#0f0f12;color:#e8e8ee;font:15px/1.45 Inter,system-ui}}article{{display:grid;grid-template-columns:270px 1fr;gap:20px;background:#18181d;border-radius:12px;padding:14px;margin:0 0 14px}}
img{{width:270px;border-radius:8px}}h3{{margin:0 0 6px}}small{{color:#9a9aa6;font-weight:400}}.q{{font-style:italic;color:#cfcfe0}}dt{{color:#7fe3b8;font-size:12px;text-transform:uppercase;margin-top:8px}}dd{{margin:2px 0 0}}code{{font-size:12px;word-break:break-word}}
@media(max-width:640px){{article{{grid-template-columns:1fr}}img{{width:100%}}}}</style>
<h1>Storyboard — {a.name} <small>estilo {style['name']} · verde = zona segura · rojo = tapado por la UI de la app</small></h1>{''.join(rows)}"""
    (p / "out" / "storyboard.html").write_text(html)
    print(f"[ves] ✓ storyboard: projects/{a.name}/out/storyboard.html ({len(rows)} escenas)")


def cmd_fork(a):
    """Mismo video en otro estilo: copia corte/transcripción/captions, cambia estilo (3 estilos desde el mismo material)."""
    src = proj(a.name)
    dst = PROJECTS / a.new
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("out", "edit_plan.json", "plan.html", "palette.json"))
    meta = jload(dst / "project.json"); meta["name"] = a.new; meta["style"] = a.style; load_style(a.style)
    jsave(dst / "project.json", meta)
    for f in (cmd_palette, cmd_captions, cmd_plandoc):
        f(argparse.Namespace(name=a.new, preset=None, accent=None))


def cmd_captionsheet(a):
    """Hoja de diseño de captions para aprobar: ~12 frases sobre el A-roll, con zona segura,
    línea roja en la boca y verde en el mentón (el caption nunca debe cruzar la roja)."""
    from PIL import Image, ImageDraw
    p = proj(a.name)
    meta = jload(p / "project.json")
    plan = jload(p / "edit_plan.json")
    style = load_style(plan.get("style", meta["style"]))
    phr = jload(p / "captions.json")["phrases"]
    full = [s for s in plan["scenes"] if SCENES.get(s["type"], {}).get("layer") == "fullscreen"]
    vis = [ph for ph in phr if not any(ph["start"] < s["end"] and ph["end"] > s["start"] for s in full)]
    pick = vis[:: max(1, len(vis) // 12)][:12]
    times = [round((ph["start"] + ph["end"]) / 2 + 0.25, 2) for ph in pick]
    cmd_render(argparse.Namespace(name=a.name, at=",".join(map(str, times)), force=True, draft=False))
    track = facetrack(p, p / meta.get("cut", meta["raw"]))
    tiles = []
    for t, ph in zip(times, pick):
        im = Image.open(p / "out" / f"still_{t:06.2f}.png").convert("RGB")
        d = ImageDraw.Draw(im)
        f = min(track, key=lambda x: abs(x["t"] - t)) if track else None
        if f:
            mouth, chin = f["y"] + f["h"] * 0.82, f["y"] + f["h"] * 1.18
            d.line([0, mouth, 1080, mouth], fill=(255, 40, 60), width=5)
            d.line([0, chin, 1080, chin], fill=(0, 230, 140), width=3)
        sz = style.get("safe_zone", {})
        d.rectangle([1080 * sz.get("left", 0), 1920 * sz.get("top", 0), 1080 * (1 - sz.get("right", 0)), 1920 * (1 - sz.get("bottom", 0))], outline=(0, 230, 140), width=4)
        tiles.append(im.resize((360, 640)))
    cols = 6; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 364, rows * 644), "white")
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * 364, (i // cols) * 644))
    out = p / "out" / "caption_sheet.jpg"; sheet.save(out, quality=88)
    print(f"[ves] ✓ hoja de captions: {out.relative_to(ROOT)} — roja = boca (no tocar), verde = mentón / zona segura")


def _approval_hash(p: Path) -> str:
    import hashlib
    h = hashlib.sha1()
    for f in ("edit_plan.json", "captions.json", "palette.json"):
        if (p / f).exists():
            h.update((p / f).read_bytes())
    return h.hexdigest()[:12]


def cmd_approve(a):
    """Solo el HUMANO aprueba (después de ver storyboard + hoja de captions + paleta)."""
    p = proj(a.name)
    (p / "APPROVED").write_text(_approval_hash(p))
    print(f"[ves] aprobado {a.name} ({_approval_hash(p)}). Cualquier cambio posterior al plan/captions/paleta anula la aprobación.")


def cmd_all(a):
    for f, extra in ((cmd_transcribe, {"model": a.model, "lang": a.lang}), (cmd_rawcut, {"gap": 0.35, "pad": 0.03, "vertical": a.vertical}),
                     (cmd_palette, {"preset": None, "accent": None}), (cmd_captions, {}), (cmd_plandoc, {})):
        f(argparse.Namespace(name=a.name, **extra))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("new"); s.add_argument("name"); s.add_argument("--video", required=True); s.add_argument("--style", required=True); s.set_defaults(f=cmd_new)
    s = sub.add_parser("transcribe"); s.add_argument("name"); s.add_argument("--model", default="small"); s.add_argument("--lang", default=None); s.set_defaults(f=cmd_transcribe)
    s = sub.add_parser("rawcut"); s.add_argument("name"); s.add_argument("--gap", type=float, default=0.35); s.add_argument("--pad", type=float, default=0.03); s.add_argument("--vertical", action="store_true"); s.set_defaults(f=cmd_rawcut)
    s = sub.add_parser("palette"); s.add_argument("name"); s.add_argument("--preset", default=None); s.add_argument("--accent", default=None); s.set_defaults(f=cmd_palette)
    s = sub.add_parser("storyboard"); s.add_argument("name"); s.add_argument("--force", action="store_true"); s.set_defaults(f=cmd_storyboard)
    s = sub.add_parser("captionsheet"); s.add_argument("name"); s.set_defaults(f=cmd_captionsheet)
    s = sub.add_parser("approve"); s.add_argument("name"); s.set_defaults(f=cmd_approve)
    s = sub.add_parser("fork"); s.add_argument("name"); s.add_argument("new"); s.add_argument("--style", required=True); s.set_defaults(f=cmd_fork)
    for n, f in (("captions", cmd_captions), ("plandoc", cmd_plandoc), ("validate", cmd_validate)):
        s = sub.add_parser(n); s.add_argument("name"); s.set_defaults(f=f)
    s = sub.add_parser("render"); s.add_argument("name"); s.add_argument("--draft", action="store_true"); s.add_argument("--force", action="store_true"); s.set_defaults(f=cmd_render)
    s = sub.add_parser("preview"); s.add_argument("name"); s.add_argument("--at", required=True, help="segundos separados por coma"); s.add_argument("--force", action="store_true"); s.add_argument("--draft", action="store_true"); s.set_defaults(f=cmd_render)
    s = sub.add_parser("sound"); s.add_argument("name"); s.add_argument("--music", default=None); s.add_argument("--draft", action="store_true"); s.set_defaults(f=cmd_sound)
    s = sub.add_parser("all"); s.add_argument("name"); s.add_argument("--model", default="small"); s.add_argument("--lang", default=None); s.add_argument("--vertical", action="store_true"); s.set_defaults(f=cmd_all)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
