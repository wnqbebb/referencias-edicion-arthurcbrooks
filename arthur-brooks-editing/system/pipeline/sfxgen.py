#!/usr/bin/env python3
"""Genera una librería base de SFX procedurales (sin licencias) con ffmpeg.
Reemplázalos por tu librería propia manteniendo los mismos nombres de archivo."""
import subprocess
import sys
from pathlib import Path

out = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/sfx")
out.mkdir(parents=True, exist_ok=True)
SR = 48000
LIB = {
    # nombre: filtro lavfi
    "pop": "sine=f=880:d=0.09,afade=t=out:st=0.02:d=0.07,volume=0.9",
    "click": "sine=f=2400:d=0.03,afade=t=out:st=0.005:d=0.025,volume=0.6",
    "tick": "sine=f=1800:d=0.04,afade=t=out:st=0.01:d=0.03,volume=0.5",
    "notify": "sine=f=1320:d=0.12,afade=t=out:st=0.05:d=0.07[a];sine=f=1760:d=0.18,adelay=110|110,afade=t=out:st=0.2:d=0.08[b];[a][b]amix=inputs=2:normalize=0",
    "whoosh": "anoisesrc=d=0.45:c=pink:a=0.6,bandpass=f=1200:w=900,afade=t=in:d=0.25,afade=t=out:st=0.25:d=0.2",
    "whoosh_soft": "anoisesrc=d=0.7:c=brown:a=0.5,lowpass=f=900,afade=t=in:d=0.4,afade=t=out:st=0.4:d=0.3",
    "riser": "anoisesrc=d=0.9:c=white:a=0.25,highpass=f=600,afade=t=in:d=0.85,afade=t=out:st=0.85:d=0.05",
    "hit": "sine=f=55:d=0.5,afade=t=out:st=0.05:d=0.45,volume=1.4",
    "draw": "anoisesrc=d=0.6:c=pink:a=0.15,bandpass=f=3000:w=1500,afade=t=in:d=0.1,afade=t=out:st=0.4:d=0.2",
}
for name, f in LIB.items():
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-filter_complex", f + ",aformat=sample_rates=48000:channel_layouts=stereo",
                    "-ar", str(SR), str(out / f"{name}.wav")], check=True)
print(f"[sfx] {len(LIB)} SFX en {out}")
