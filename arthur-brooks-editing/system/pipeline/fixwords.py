#!/usr/bin/env python3
"""Corrige palabras mal transcritas en transcript_cut.json conservando los tiempos.
uso: fixwords.py <proyecto> "frase mal=>frase bien" ...   (se compara normalizado; el nº de palabras puede cambiar)"""
import json, re, sys
from pathlib import Path
p = Path(__file__).resolve().parent.parent / "projects" / sys.argv[1] / "transcript_cut.json"
d = json.loads(p.read_text()); W = d["words"]
n = lambda s: re.sub(r"[^\wáéíóúñü%]", "", s.lower())
for rule in sys.argv[2:]:
    bad, good = [x.strip() for x in rule.split("=>")]
    bt, gt = bad.split(), good.split()
    i, hits = 0, 0
    while i <= len(W) - len(bt):
        if [n(w["w"]) for w in W[i:i + len(bt)]] == [n(x) for x in bt]:
            s, e = W[i]["start"], W[i + len(bt) - 1]["end"]
            step = (e - s) / len(gt)
            new = [{"w": g, "start": round(s + k * step, 3), "end": round(s + (k + 1) * step, 3)} for k, g in enumerate(gt)]
            W[i:i + len(bt)] = new; i += len(gt); hits += 1
        else:
            i += 1
    print(f"{rule!r}: {hits}")
p.write_text(json.dumps(d, ensure_ascii=False, indent=1))
