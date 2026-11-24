// Kit de diseño compartido: tokens → movimiento, color, texto cinematográfico, fondos y texturas.
// Toda decisión estética sale de style.json; los componentes nunca inventan valores.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { continueRender, delayRender, staticFile } from "remotion";

// Fuentes locales (OFL) → render 100% offline y determinista en cualquier máquina/modelo.
const FONTS: [string, string, string][] = [
  ["Inter", "fonts/Inter.woff2", "normal"],
  ["Inter", "fonts/Inter-ext.woff2", "normal"],
  ["Playfair Display", "fonts/Playfair.woff2", "normal"],
  ["Playfair Display", "fonts/Playfair-Italic.woff2", "italic"],
  ["Bebas Neue", "fonts/BebasNeue.ttf", "normal"],
  ["Anton", "fonts/Anton.ttf", "normal"],
  ["Caveat", "fonts/Caveat.ttf", "normal"],
  ["Instrument Serif", "fonts/InstrumentSerif.woff2", "normal"],
  ["Instrument Serif", "fonts/InstrumentSerif-Italic.woff2", "italic"],
];
if (typeof document !== "undefined") {
  const h = delayRender("fonts");
  Promise.all(FONTS.map(([fam, file, st]) => new FontFace(fam, `url(${staticFile(file)})`, { style: st, weight: "100 900" }).load().then((f) => (document as any).fonts.add(f))))
    .then(() => continueRender(h)).catch((e) => { console.error(e); continueRender(h); });
}

export type Ctx = { style: any; palette: Record<string, string> };
export const StyleCtx = React.createContext<Ctx>(null as any);
export const useStyle = () => React.useContext(StyleCtx);

export const color = (ctx: Ctx, ref: string | undefined, fallback = "#ffffff") => {
  if (!ref) return fallback;
  if (ref.startsWith("#")) return ref;
  const role = ctx.style.palette.roles?.[ref];
  return ctx.palette[role ?? ref] ?? fallback;
};
export const roles = (ctx: Ctx) => ({
  primary: color(ctx, "primary"),
  secondary: color(ctx, "secondary"),
  accent: color(ctx, "accent"),
  accentDark: ctx.palette.vibrant_dark,
});
// texto legible sobre un fondo dado
export const inkOn = (bg: string) => {
  const n = parseInt(bg.slice(1), 16);
  const l = (0.299 * ((n >> 16) & 255) + 0.587 * ((n >> 8) & 255) + 0.114 * (n & 255)) / 255;
  return l > 0.55;
};

/** progreso 0→1 de entrada usando la curva y duración del estilo */
export const useEnter = (delayFrames = 0, scaleMs = 1) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { style } = useStyle();
  const m = style.motion;
  const dur = Math.max(1, Math.round(((m.enter_ms * scaleMs) / 1000) * fps));
  return interpolate(frame - delayFrames, [0, dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(m.easing[0], m.easing[1], m.easing[2], m.easing[3]),
  });
};
/** salida 1→0 en los últimos exit_ms del clip */
export const useExit = (durationFrames: number) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { style } = useStyle();
  const d = Math.max(1, Math.round((style.motion.exit_ms / 1000) * fps));
  return interpolate(frame, [durationFrames - d, durationFrames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
};

/** animación de entrada canónica del estilo: pop + blur + fade */
export const popStyle = (p: number, style: any, kind?: string): React.CSSProperties => {
  const m = style.motion;
  const anim = kind ?? style.captions.animation;
  const scale = anim === "blur_fade" ? 1 : m.pop_from_scale + (1 - m.pop_from_scale) * p;
  return {
    opacity: p,
    filter: `blur(${(1 - p) * m.blur_from_px}px)`,
    transform: `translateY(${(1 - p) * 18}px) scale(${scale})`,
  };
};

export const stagger = (i: number, fps: number, style: any) => Math.round(((style.motion.stagger_ms * i) / 1000) * fps);

const norm = (w: string) => w.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");

/**
 * Texto cinematográfico (regla del estilo): palabra(s) especial(es) grandes en la fuente especial
 * en el centro; el resto, pequeño en sans, rellena los huecos arriba y abajo.
 */
export const CinematicText: React.FC<{
  text: string; special?: string[]; size?: number; ink?: string; specialInk?: string; align?: "center" | "left"; delay?: number; maxWidth?: number;
}> = ({ text, special = [], size, ink, specialInk, align = "center", delay = 0, maxWidth = 900 }) => {
  const ctx = useStyle();
  const { fps } = useVideoConfig();
  const s = ctx.style;
  const base = size ?? s.captions.base_size;
  const words = text.split(/\s+/).filter(Boolean);
  const spSet = new Set(special.map(norm));
  let first = words.findIndex((w) => spSet.has(norm(w)));
  let last = first;
  while (last + 1 < words.length && spSet.has(norm(words[last + 1]))) last++;
  const before = first >= 0 ? words.slice(0, first) : words;
  const mid = first >= 0 ? words.slice(first, last + 1) : [];
  const after = first >= 0 ? words.slice(last + 1) : [];
  const sansF = `'${s.fonts.sans.family}'`;
  const spF = `'${s.fonts.special.family}'`;
  const lines: { text: string; special: boolean }[] = [];
  if (before.length) lines.push({ text: before.join(" "), special: false });
  if (mid.length) lines.push({ text: mid.join(" "), special: true });
  if (after.length) lines.push({ text: after.join(" "), special: false });
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: align === "center" ? "center" : "flex-start", maxWidth, gap: base * 0.05 }}>
      {lines.map((ln, i) => {
        const p = useEnter(delay + stagger(i, fps, s));
        return (
          <div key={i} style={{
            ...popStyle(p, s),
            fontFamily: ln.special ? spF : sansF,
            fontWeight: ln.special ? s.fonts.special.weight : s.fonts.sans.weight,
            fontStyle: ln.special ? s.fonts.special.style : "normal",
            fontSize: ln.special ? base * s.captions.special_scale : base,
            lineHeight: ln.special ? 1.0 : 1.15,
            letterSpacing: ln.special ? "-0.01em" : "-0.02em",
            color: ln.special ? specialInk ?? color(ctx, s.captions.special_color) : ink ?? s.captions.color,
            textAlign: align, textWrap: "balance" as any,
          }}>{ln.text}</div>
        );
      })}
    </div>
  );
};

/** Fondos: color primario + grid opcional + textura (paper / halftone / cloth) */
export const Backdrop: React.FC<{ bg?: string; children?: React.ReactNode; grid?: boolean }> = ({ bg, children, grid }) => {
  const ctx = useStyle();
  const s = ctx.style;
  const c = bg ?? roles(ctx).primary;
  const g = grid ?? s.background.grid;
  const ink = inkOn(c) ? "0,0,0" : "255,255,255";
  return (
    <AbsoluteFill style={{ backgroundColor: c }}>
      {g ? (
        <AbsoluteFill style={{
          backgroundImage: `linear-gradient(rgba(${ink},${s.background.grid_opacity || 0.06}) 2px, transparent 2px), linear-gradient(90deg, rgba(${ink},${s.background.grid_opacity || 0.06}) 2px, transparent 2px)`,
          backgroundSize: "90px 90px", backgroundPosition: "center",
          maskImage: "radial-gradient(ellipse at center, black 30%, transparent 80%)",
        }} />
      ) : null}
      {children}
      <Texture />
    </AbsoluteFill>
  );
};

export const Texture: React.FC<{ kind?: string; opacity?: number; dark?: boolean }> = ({ kind, opacity, dark }) => {
  // Texturas REALES (render/public/textures/*.png): papel rugoso, pintura, tela, halftone (principios 2, 3, 6, 7 de Arthur)
  const { style } = useStyle();
  const t = style.texture ?? {};
  const k = kind ?? t.kind;
  const o = opacity ?? Math.max(t.opacity ?? 0, k && k !== "none" ? 0.35 : 0);
  if (!k || k === "none" || !o) return null;
  return <AbsoluteFill style={{ opacity: o, mixBlendMode: dark ? "overlay" : "multiply", backgroundImage: `url(${staticFile(t.files?.[k] ?? `textures/${k}.png`)})`, backgroundSize: "cover", pointerEvents: "none" }} />;
};

/** Caja con blur para UI (notificaciones, listas) */
export const Glass: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => {
  const ctx = useStyle();
  return (
    <div style={{
      background: "rgba(20,20,24,0.55)", backdropFilter: "blur(24px)", WebkitBackdropFilter: "blur(24px)",
      border: "1.5px solid rgba(255,255,255,0.18)", borderRadius: ctx.style.shapes.radius, boxShadow: "0 30px 80px rgba(0,0,0,.35)",
      ...style,
    }}>{children}</div>
  );
};

/** Padding de zona segura (Reels/TikTok/Shorts). Contenido centrado: margen lateral simétrico = el mayor. */
export const safePad = (style: any, extra = 0): React.CSSProperties => {
  const z = style.safe_zone ?? { top: 0.12, bottom: 0.22, left: 0.08, right: 0.12 };
  const side = Math.max(z.left, z.right) * 1080 + extra;
  return { paddingTop: z.top * 1920 + extra, paddingBottom: z.bottom * 1920 + extra, paddingLeft: side, paddingRight: side, boxSizing: "border-box" };
};

/** Grado de marca para b-roll/imágenes (equivale a aplicar la misma LUT a todo el material externo). */
export const BrandGrade: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const ctx = useStyle();
  const g = ctx.style.broll_grade ?? {};
  const tint = color(ctx, g.tint ?? "accent_dark", ctx.palette.vibrant_dark);
  const noise = `<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>`;
  return (
    <div style={{ position: "relative", width: "100%", height: "100%", overflow: "hidden" }}>
      <AbsoluteFill style={{ filter: `contrast(${g.contrast ?? 1}) saturate(${g.saturate ?? 1}) brightness(${g.brightness ?? 1})` }}>{children}</AbsoluteFill>
      <AbsoluteFill style={{ background: tint, mixBlendMode: "soft-light", opacity: g.tint_opacity ?? 0.12 }} />
      <AbsoluteFill style={{ backgroundImage: `url("data:image/svg+xml;utf8,${noise}")`, opacity: g.grain ?? 0.06, mixBlendMode: "overlay" }} />
    </div>
  );
};
