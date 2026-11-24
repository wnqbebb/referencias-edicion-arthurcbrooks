#!/usr/bin/env python3
"""Análisis de SONIDO de una referencia: separa voz / resto (Demucs htdemucs, 2 stems) y en 'resto'
(música + SFX) detecta eventos transitorios = efectos de sonido. Clasifica cada evento por forma
(whoosh, click/pop, hit/boom, riser, swell/ambiente) y lo alinea con cortes de plano y palabras.
Guarda: references/vNN/audio/{vocals,no_vocals}.wav, sfx_events.json, sfx/*.wav (recortes de REFERENCIA,
no para usar en clientes: se mapean a equivalentes con licencia de assets/sfx_lib)."""
import os
import json, subprocess, sys
from pathlib import Path
import numpy as np, librosa, soundfile as sf
ROOT = Path(__file__).resolve().parent.parent
STYLE = os.environ.get("VES_STYLE", "arthur-brooks")   # estilo que se está entrenando
REFS = ROOT / "refs" / os.environ.get("VES_REFS", "arthur")  # carpeta con los videos de referencia vNN.mp4
REF = ROOT / "styles" / STYLE / "references"

def separate(v, out):
    if (out / "no_vocals.wav").exists(): return
    out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_mix.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-ac", "2", "-ar", "44100", str(tmp)], check=True)
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-d", "cpu", "-j", "4", "-o", str(out / "_d"), str(tmp)], check=True, capture_output=True)
    d = next((out / "_d").rglob("vocals.wav")).parent
    (d / "vocals.wav").rename(out / "vocals.wav"); (d / "no_vocals.wav").rename(out / "no_vocals.wav")
    subprocess.run(["rm", "-rf", str(out / "_d"), str(tmp)])

def classify(seg, sr):
    if len(seg) < sr * 0.05: return "click"
    S = np.abs(librosa.stft(seg, n_fft=1024, hop_length=256)) + 1e-9
    cent = librosa.feature.spectral_centroid(S=S, sr=sr)[0]; flat = librosa.feature.spectral_flatness(S=S)[0]
    rms = librosa.feature.rms(S=S, frame_length=1024)[0]; dur = len(seg) / sr
    peak = int(np.argmax(rms)) / max(1, len(rms))
    c, f = float(np.median(cent)), float(np.median(flat))
    if dur < 0.18: return "click" if c > 2500 else "pop"
    if c < 700 and peak < 0.3: return "hit/boom"
    if peak > 0.7 and dur > 0.8: return "riser"
    if f > 0.08 and 0.15 < dur < 1.5: return "whoosh"
    if dur > 1.5: return "swell/ambiente"
    return "pop" if c > 1500 else "hit/boom"

def analyze(d):
    v = REFS / f"{d.name}.mp4"; out = d / "audio"
    separate(v, out)
    y, sr = librosa.load(out / "no_vocals.wav", sr=22050, mono=True)
    # quitar la "cama" musical: comparar contra mediana móvil de energía
    hop = 256
    env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    base = np.convolve(rms, np.ones(80) / 80, mode="same")
    on = librosa.onset.onset_detect(onset_envelope=env, sr=sr, hop_length=hop, units="frames", backtrack=True, delta=0.25)
    ev = json.loads((d / "evidence.json").read_text()); words = ev["words"]
    cuts = [s["start"] for s in json.loads((d / "scenes.json").read_text())] if (d / "scenes.json").exists() else [s["start"] for s in ev["shots"]]
    sfxdir = out / "sfx"; sfxdir.mkdir(exist_ok=True)
    events = []
    for k, fr in enumerate(on):
        if rms[fr:fr + 8].max() < 1.5 * base[fr] + 0.004: continue   # no sobresale de la música → no es SFX
        t = fr * hop / sr
        end = fr
        while end < len(rms) - 1 and rms[end] > max(base[end] * 1.2, rms[fr:fr + 8].max() * 0.15) and (end - fr) * hop / sr < 3: end += 1
        seg = y[int(t * sr): int(end * hop)]
        kind = classify(seg, sr)
        near_cut = min(cuts, key=lambda c: abs(c - t)) if cuts else None
        w = min(words, key=lambda w: abs(w["start"] - t)) if words else None
        e = {"t": round(t, 3), "dur": round(len(seg) / sr, 2), "kind": kind, "gain_db": round(20 * np.log10(rms[fr:fr + 8].max() / (base[fr] + 1e-6)), 1),
             "to_cut": round(t - near_cut, 2) if near_cut is not None else None, "word": w["w"] if w else None, "to_word": round(t - w["start"], 2) if w else None}
        events.append(e)
        if len(seg) > sr * 0.04: sf.write(sfxdir / f"{len(events):03d}_{kind.replace('/', '-')}.wav", seg, sr)
    (d / "sfx_events.json").write_text(json.dumps(events, ensure_ascii=False, indent=1))
    from collections import Counter
    print(d.name, len(events), dict(Counter(e["kind"] for e in events)))

for d in sorted(REF.glob("v??")):
    if len(sys.argv) > 1 and d.name not in sys.argv[1:]: continue
    try: analyze(d)
    except Exception as ex: print(d.name, "ERROR", ex)
