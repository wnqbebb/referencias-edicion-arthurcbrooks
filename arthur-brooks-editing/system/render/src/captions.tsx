// Modos de caption, derivados de las referencias de Arthur Brooks:
//  - "doc"      (v01 'my life'): centrado vertical (~50 %), palabra(s) clave GRANDES con 2 tratamientos que alternan
//                 (bold sans apretada  ↔  serif itálica bold), palabras de contexto pequeñas arriba-izq / abajo-der.
//  - "cinematic" (minimal): especial al centro, resto arriba/abajo (CinematicText).
//  - "bold_upper" (podcast clip): 1–3 palabras MAYÚSCULAS display condensada, blanco, centrado bajo la mitad.
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { CinematicText, color, popStyle, useEnter, useStyle } from "./kit";

const DocCaption: React.FC<{ ph: any }> = ({ ph }) => {
  const ctx = useStyle();
  const s = ctx.style;
  const c = s.captions;
  const words: string[] = ph.words.map((w: any) => w.w);
  const sp: number[] = ph.special ?? [];
  const first = sp.length ? Math.min(...sp) : -1;
  const last = sp.length ? Math.max(...sp) : -1;
  const before = first >= 0 ? words.slice(0, first).join(" ") : words.join(" ");
  const mid = first >= 0 ? words.slice(first, last + 1).join(" ") : "";
  const after = first >= 0 ? words.slice(last + 1).join(" ") : "";
  const serif = ph.treatment === "serif";
  const p = useEnter(0);
  const q = useEnter(2);
  const small: React.CSSProperties = { fontFamily: `'${s.fonts.sans.family}'`, fontWeight: 400, fontSize: Math.max(42, c.base_size * 0.62), color: c.color, letterSpacing: "-0.01em", lineHeight: 1.1, textShadow: "0 2px 12px rgba(0,0,0,.35)" };
  const big: React.CSSProperties = serif
    ? { fontFamily: `'${s.fonts.special.family}'`, fontStyle: "italic", fontWeight: 700, letterSpacing: "-0.035em", fontSize: c.base_size * c.special_scale }
    : { fontFamily: `'${s.fonts.sans_bold.family}'`, fontWeight: 800, letterSpacing: "-0.05em", fontSize: c.base_size * c.special_scale * 0.92 };
  if (!mid) {
    return <div style={{ ...popStyle(p, s), ...small, fontSize: c.base_size * 0.5, textAlign: "center" }}>{before}</div>;
  }
  return (
    <div style={{ display: "inline-flex", flexDirection: "column", alignItems: "stretch" }}>
      {before ? <div style={{ ...popStyle(p, s), ...small, alignSelf: "flex-start", marginBottom: -c.base_size * 0.12, paddingLeft: c.base_size * 0.1 }}>{before}</div> : null}
      <div style={{ ...popStyle(q, s), ...big, color: color(ctx, c.special_color, "#fff"), lineHeight: 0.95, textAlign: "center", textShadow: "0 4px 24px rgba(0,0,0,.35)" }}>{mid}</div>
      {after ? <div style={{ ...popStyle(q, s), ...small, alignSelf: "flex-end", marginTop: -c.base_size * 0.06, paddingRight: c.base_size * 0.1 }}>{after}</div> : null}
    </div>
  );
};

const BoldUpper: React.FC<{ ph: any }> = ({ ph }) => {
  const { style } = useStyle();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const c = style.captions;
  const t0 = ph.start;
  // palabra por palabra: cada palabra aparece en su tiempo exacto (pop corto)
  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "0 0.25em", maxWidth: 760 }}>
      {ph.words.map((w: any, i: number) => {
        const at = (w.start - t0) * fps;
        const k = interpolate(frame, [at, at + 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const hl = (ph.special ?? []).includes(i);
        return (
          <span key={i} style={{ opacity: k, transform: `scale(${0.85 + 0.15 * k})`, display: "inline-block", marginRight: "0.28em", fontFamily: `'${style.fonts.display?.family ?? "Bebas Neue"}'`, fontSize: c.base_size, lineHeight: 1, textTransform: "uppercase", letterSpacing: "0.01em", color: hl ? c.highlight_color ?? "#fff" : c.color, WebkitTextStroke: c.stroke ? `${c.stroke}px rgba(0,0,0,.85)` : undefined, textShadow: "0 3px 10px rgba(0,0,0,.6)" }}>{w.w}</span>
        );
      })}
    </div>
  );
};


// ── modo "arthur" (método Joseph, principio 1) ─────────────────────────────────────────────
// ≤5 palabras · la palabra clave GRANDE y negrita al centro (bold sans ↔ bold serif itálica) · el resto PEQUEÑO en sans
// light en los huecos arriba/abajo · el texto pequeño mide el 75 % del ancho del grande · palabras aparecen en su tiempo
// (gris → blanco en 3 frames) · variante: palabra serif sobre caja de acento ("enhance").
let _cv: CanvasRenderingContext2D | null = null;
const measure = (text: string, font: string) => {
  if (typeof document === "undefined") return text.length * 30;
  if (!_cv) _cv = document.createElement("canvas").getContext("2d");
  _cv!.font = font;
  return _cv!.measureText(text).width;
};
const ArthurCaption: React.FC<{ ph: any; fromSec?: number }> = ({ ph, fromSec }) => {
  const ctx = useStyle();
  const s = ctx.style;
  const c = s.captions;
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ws: any[] = ph.words;
  const sp: number[] = (ph.special ?? []).length ? ph.special : [ws.reduce((b: number, w: any, i: number) => (w.w.length > ws[b].w.length ? i : b), 0)];
  const a = Math.min(...sp), b = Math.max(...sp);
  const serif = ph.treatment === "serif";
  const MAXW = 1080 * 0.7;
  const bigFam = serif ? `'${s.fonts.special.family}'` : `'${s.fonts.sans_bold?.family ?? s.fonts.sans.family}'`;
  const bigFont = (px: number) => `${serif ? "italic 700" : "800"} ${px}px ${bigFam}`;
  const bigText = ws.slice(a, b + 1).map((w: any) => w.w).join(" ");
  let bigPx = c.base_size * (c.special_scale ?? 1.8) * (serif ? 1.08 : 1);
  const bw0 = measure(bigText, bigFont(bigPx)) * (serif ? 0.97 : 0.95);
  if (bw0 > MAXW) bigPx *= MAXW / bw0;
  bigPx = Math.max(bigPx, 100);
  const bigW = Math.min(MAXW, measure(bigText, bigFont(bigPx)) * (serif ? 0.97 : 0.95));
  const smallFam = `'${s.fonts.sans.family}'`;
  const fitSmall = (t: string) => {
    if (!t) return 0;
    const w100 = measure(t, `400 100px ${smallFam}`);
    return Math.max(40, Math.min(bigPx * 0.42, (0.75 * bigW * 100) / w100));
  };
  const before = ws.slice(0, a), after = ws.slice(b + 1);
  const bPx = fitSmall(before.map((w: any) => w.w).join(" "));
  const aPx = fitSmall(after.map((w: any) => w.w).join(" "));
  // sincronía fina: cada palabra termina de encenderse 2 frames ANTES de pronunciarse (≈66 ms de adelanto)
  const t0 = fromSec ?? ph.start;
  const on = (w: any) => { const wf = (w.start - t0) * fps; return interpolate(frame, [wf - 5, wf - 2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }); };
  const word = (w: any, i: number) => {
    const k = on(w);
    return <span key={i} style={{ opacity: 0.25 + 0.75 * k, color: k < 1 ? `rgba(255,255,255,${0.45 + 0.55 * k})` : c.color, marginRight: "0.24em" }}>{w.w}</span>;
  };
  const kBig = on(ws[a]);
  const smallSt = (px: number): React.CSSProperties => ({ fontFamily: smallFam, fontWeight: 400, fontSize: px, lineHeight: 1.05, letterSpacing: "-0.01em", color: c.color, textShadow: "0 2px 14px rgba(0,0,0,.45)", whiteSpace: "nowrap", textAlign: "center" });
  const box = ph.box === true && serif;
  // palabra clave resaltada en el color de marca del video; si el acento es muy oscuro para leerse sobre el A-roll,
  // se aclara hacia blanco lo justo para que tenga contraste
  const acc = ctx.palette?.vibrant_bright ?? "#1B54F8";
  const hx = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const [ar, ag, ab] = hx(acc);
  const lum = (0.2126 * ar + 0.7152 * ag + 0.0722 * ab) / 255;
  const mixW = lum < 0.32 ? Math.min(0.45, (0.32 - lum) * 2.2 + 0.18) : 0;
  const keyColor = `rgb(${[ar, ag, ab].map((v) => Math.round(v + (255 - v) * mixW)).join(",")})`;
  const bigSt: React.CSSProperties = {
    fontFamily: bigFam, fontStyle: serif ? "italic" : "normal", fontWeight: serif ? 700 : 800, fontSize: bigPx, lineHeight: 0.92,
    letterSpacing: serif ? "-0.03em" : "-0.055em", color: box ? "#fff" : keyColor, whiteSpace: "nowrap",
    opacity: kBig, filter: `blur(${(1 - kBig) * 6}px) brightness(${0.55 + 0.45 * kBig})`, transform: `translateY(${(1 - kBig) * 10}px)`,
    textShadow: box ? "none" : "0 3px 10px rgba(0,0,0,.55), 0 0 30px rgba(0,0,0,.35)",
    ...(box ? { background: ctx.palette?.vibrant_bright ?? "#1B54F8", padding: `0 ${bigPx * 0.12}px ${bigPx * 0.06}px`, borderRadius: 4 } : {}),
  };
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      {before.length ? <div style={{ ...smallSt(bPx), marginBottom: -bigPx * 0.06 }}>{before.map(word)}</div> : null}
      <div style={bigSt}>{bigText}</div>
      {after.length ? <div style={{ ...smallSt(aPx), marginTop: bigPx * 0.02 }}>{after.map(word)}</div> : null}
    </div>
  );
};

export const Caption: React.FC<{ ph: any; fromSec?: number }> = ({ ph, fromSec }) => {
  const { style } = useStyle();
  const c = style.captions;
  const z = style.safe_zone ?? { left: 0.08, right: 0.12 };
  const side = Math.max(z.left, z.right) * 100;
  // y calculado por ves.py (debajo del mentón, nunca sobre la boca); si no hay, el centro del estilo
  const cy = ph.y ? (ph.y / (style.format?.height ?? 1920)) * 100 : (c.center_y ?? 0.6) * 100;
  const mode = c.mode ?? "cinematic";
  const text = ph.words.map((w: any) => w.w).join(" ");
  const special = (ph.special ?? []).map((i: number) => ph.words[i]?.w).filter(Boolean);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", top: `${cy - 12}%`, height: "24%", padding: `0 ${side}%` }}>
      {mode === "arthur" ? <ArthurCaption ph={ph} fromSec={fromSec} /> : mode === "doc" ? <DocCaption ph={ph} /> : mode === "bold_upper" ? <BoldUpper ph={ph} /> : <CinematicText text={text} special={special} />}
    </AbsoluteFill>
  );
};
