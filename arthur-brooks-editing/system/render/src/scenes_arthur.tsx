// Lenguaje visual Arthur Brooks (extraído de 506 escenas, ver styles/arthur-brooks/references/ALL_SCENES.json):
//  · inversión de color: fondo acento + texto blanco  ↔  fondo blanco + texto acento (corte seco)
//  · write-on palabra por palabra; la palabra grande entra gris y se aclara (v08_s16, v10_s01)
//  · serif condensada grande (Instrument Serif) + sans pequeña (Inter) en los huecos
//  · ilustración: mancha blanca con siluetas/íconos de línea (v10_s01, v03_s04), anillos orbitales (v12_s09)
//  · franjas numeradas al enumerar (v06_s03), bloques que se dividen (v19_s14), flash amarillo (v08_s16)
import React from "react";
import { AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { BrandGrade, Texture, roles, safePad, useExit, useStyle } from "./kit";

type P = { props: any; dur: number; project: string; video: string; start: number };
const SERIF = "'Playfair Display'"; // principio 1: palabra clave en Playfair Display itálica, en negrita
const SANS = "'Inter'";
const src = (project: string, p: string) => (p.startsWith("http") ? p : staticFile(`${project}/${p}`));
const isVid = (p?: string) => !!p && /\.(mp4|mov|webm|m4v)$/i.test(p);
const ease = Easing.bezier(0.16, 1, 0.3, 1);

/** fondo de marca: acento con glow radial más claro al centro + textura + grano (o blanco papel) */
const Ground: React.FC<{ bg: string; children?: React.ReactNode }> = ({ bg, children }) => {
  const ctx = useStyle(); const r = roles(ctx);
  const base = bg === "white" ? r.primary : bg === "black" ? "#050505" : r.accent;
  const glow = bg === "white" ? "rgba(255,255,255,.0)" : bg === "black" ? `${r.accent}33` : "rgba(255,255,255,.07)";
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 45%, ${glow} 0%, transparent 60%), ${base}` }}>
      {bg !== "white" ? <AbsoluteFill style={{ boxShadow: "inset 0 0 280px 60px rgba(0,0,0,.35)" }} /> : null}
      {children}
      <Texture kind="paper" opacity={bg === "white" ? 0.9 : bg === "black" ? 0.55 : 0.8} dark={bg === "black"} />
    </AbsoluteFill>
  );
};
const ink = (bg: string, r: any) => (bg === "white" ? r.accent : "#FFFFFF");

/** líneas de texto Arthur: [{t, size:'s'|'l', align}] con write-on por palabra */
export const ArthurLines: React.FC<{ lines: any[]; bg: string; from?: number; dur?: number }> = ({ lines, bg, from = 3, dur = 60 }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const ctx = useStyle(); const r = roles(ctx);
  // el write-on termina al 40 % de la escena (el texto completo debe leerse la mayor parte del tiempo)
  const total = lines.reduce((n: number, ln: any) => n + String(ln.t).split(/\s+/).length, 0);
  const wps = Math.max(3.5, total / Math.max(0.35, (dur * 0.4 - from) / fps));
  let k = 0;
  const c = ink(bg, r);
  const dim = bg === "white" ? "rgba(0,0,0,.25)" : "rgba(255,255,255,.38)";
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: "100%", maxWidth: 860 }}>
      {lines.map((ln: any, i: number) => {
        const big = ln.size === "l";
        const words = String(ln.t).split(/\s+/);
        return (
          <div key={i} style={{ alignSelf: ln.align === "left" ? "flex-start" : ln.align === "right" ? "flex-end" : "center", textAlign: ln.align ?? "center",
            fontFamily: big ? (ln.sans ? SANS : SERIF) : SANS, fontStyle: big && !ln.sans && ln.italic !== false ? "italic" : "normal", fontWeight: big ? (ln.sans ? 800 : 700) : 400,
            fontSize: big ? (ln.px ?? 150) : (ln.px ?? 60), maxWidth: "100%", whiteSpace: "normal", textWrap: "balance" as any, lineHeight: big ? 1.0 : 1.15, letterSpacing: big ? (ln.sans ? "-0.045em" : "-0.02em") : "-0.01em", marginTop: big ? 4 : 10 }}>
            {words.map((w: string, j: number) => {
              const at = from + Math.round((k++ / wps) * fps);
              const vis = frame >= at ? 1 : 0;
              const lit = interpolate(frame, [at, at + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
              const hl = ln.accentWord && w.replace(/[^\p{L}\p{N}]/gu, "").toLowerCase() === ln.accentWord.toLowerCase();
              return <span key={j} style={{ opacity: vis, color: big ? (lit < 1 ? dim : hl ? "#F2C230" : c) : c, transition: "none" }}>{w + " "}</span>;
            })}
          </div>
        );
      })}
    </div>
  );
};

/** flash de transición (amarillo de la referencia) al inicio/fin */
const Flash: React.FC<{ dur: number; mode?: string }> = ({ dur, mode }) => {
  const frame = useCurrentFrame();
  if (!mode) return null;
  const a = (mode === "in" || mode === "both") && frame < 3 ? 1 : 0;
  const b = (mode === "out" || mode === "both") && frame > dur - 3 ? 1 : 0;
  return a || b ? <AbsoluteFill style={{ background: "#F2C230" }} /> : null;
};
const Out: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => <AbsoluteFill style={{ opacity: useExit(dur) }}>{children}</AbsoluteFill>;

// ── arthur_text: escena solo texto (fondo acento/blanco/negro), con comillas opcionales ──
export const ArthurText: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle(); const r = roles(ctx); const bg = props.bg ?? "accent";
  return (
    <Out dur={dur}><Ground bg={bg}>
      <AbsoluteFill style={{ ...safePad(ctx.style, 20), justifyContent: "center", alignItems: "center" }}>
        <div style={{ position: "relative", width: "100%", maxWidth: 860, display: "flex", justifyContent: "center" }}>
          {props.quote ? <div style={{ position: "absolute", left: -70, top: -40, fontFamily: SERIF, fontSize: 220, color: ink(bg, r), opacity: 0.95, lineHeight: 1 }}>“</div> : null}
          <ArthurLines lines={props.lines} bg={bg} dur={dur} />
        </div>
      </AbsoluteFill>
      <Flash dur={dur} mode={props.flash} />
    </Ground></Out>
  );
};

// ── íconos de línea (trazo 7px, sin texto) ──
const ICONS: Record<string, string> = {
  tshirt: "M70 40 L95 28 Q120 46 145 28 L170 40 L205 75 L182 100 L168 88 L168 205 L72 205 L72 88 L58 100 L35 75 Z",
  hanger: "M120 40 q18 0 18 16 q0 12 -18 18 L30 160 L210 160 L120 74",
  tag: "M40 120 L120 40 L200 40 L200 120 L120 200 Z M165 75 m-12 0 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0",
  phone: "M80 30 h80 q14 0 14 14 v152 q0 14 -14 14 h-80 q-14 0 -14 -14 v-152 q0 -14 14 -14 Z M108 188 h24",
  box: "M40 85 L120 50 L200 85 L200 175 L120 210 L40 175 Z M40 85 L120 120 L200 85 M120 120 L120 210",
  person: "M120 40 m-34 0 a34 34 0 1 0 68 0 a34 34 0 1 0 -68 0 M55 210 q0 -80 65 -80 q65 0 65 80",
  eye: "M25 120 Q120 30 215 120 Q120 210 25 120 Z M120 120 m-30 0 a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0",
  heart: "M120 200 L45 125 Q15 90 45 60 Q80 30 120 75 Q160 30 195 60 Q225 90 195 125 Z",
  bag: "M50 80 h140 l-12 125 h-116 Z M88 80 q0 -45 32 -45 q32 0 32 45",
  camera: "M35 75 h45 l15 -25 h50 l15 25 h45 v120 h-170 Z M120 135 m-38 0 a38 38 0 1 0 76 0 a38 38 0 1 0 -76 0",
  star: "M120 30 L145 95 L212 95 L158 135 L178 200 L120 160 L62 200 L82 135 L28 95 L95 95 Z",
  calendar: "M40 60 h160 v140 h-160 Z M40 100 h160 M80 40 v40 M160 40 v40",
  sun: "M120 120 m-40 0 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0 M120 30 v30 M120 180 v30 M30 120 h30 M180 120 h30",
  cart: "M30 50 h35 l25 110 h100 l20 -80 h-130 M100 195 m-12 0 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0 M175 195 m-12 0 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0",
};
export const Icon: React.FC<{ name: string; size: number; color: string; fill?: string; draw?: number }> = ({ name, size, color, fill = "none", draw = 1 }) => (
  <svg viewBox="0 0 240 240" width={size} height={size}>
    <defs><filter id="roughline"><feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="5" /><feDisplacementMap in="SourceGraphic" scale="5" /></filter></defs>
    <path d={ICONS[name] ?? ICONS.star} style={{ filter: "url(#roughline)" }} fill={fill} stroke={color} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
  </svg>
);

// ── arthur_icons: mancha blanca orgánica con íconos que aparecen en secuencia + texto arriba ──
export const ArthurIcons: React.FC<P> = ({ props, dur }) => {
  const frame = useCurrentFrame(); const ctx = useStyle(); const r = roles(ctx); const bg = props.bg ?? "accent";
  const icons: string[] = props.icons ?? ["tshirt"];
  const blobK = interpolate(frame, [2, 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const n = icons.length, size = n === 1 ? 400 : n === 2 ? 280 : 210;
  const iconColor = bg === "white" ? r.accent : r.accent;
  return (
    <Out dur={dur}><Ground bg={bg}>
      <AbsoluteFill style={{ ...safePad(ctx.style, 10), justifyContent: "flex-start", alignItems: "center", paddingTop: 1920 * 0.17 }}>
        <ArthurLines lines={props.lines ?? []} bg={bg} dur={dur} />
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 540 - 380, top: 960 - 120, width: 760, height: 600, transform: `translateY(${(1 - blobK) * 260}px) scale(${0.85 + 0.15 * blobK})`, opacity: blobK }}>
        <svg viewBox="0 0 760 600" width={760} height={600} style={{ position: "absolute" }}>
          <defs><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="4" seed="3" /><feDisplacementMap in="SourceGraphic" scale="26" /></filter></defs>
          <path filter="url(#rough)" d="M120 80 Q380 -20 640 70 Q770 180 700 360 Q640 560 380 580 Q120 590 60 420 Q-20 220 120 80 Z" fill={bg === "white" ? r.accent : "#FBF9F9"} opacity={bg === "white" ? 0.12 : 1} />
        </svg>
        <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", gap: 30 }}>
          {icons.map((ic, i) => {
            const at = 10 + i * 5; const k = interpolate(frame, [at, at + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
            const hl = props.highlight === i;
            return <div key={i} style={{ transform: `scale(${0.6 + 0.4 * k})`, opacity: k }}><Icon name={ic} size={size} color={iconColor} fill={hl ? iconColor : "none"} draw={k} /></div>;
          })}
        </div>
      </div>
      <Flash dur={dur} mode={props.flash} />
    </Ground></Out>
  );
};

// ── arthur_orbit: círculo blanco con ícono o foto + anillos orbitales discontinuos (v12_s09) ──
export const ArthurOrbit: React.FC<P> = ({ props, dur, project }) => {
  const frame = useCurrentFrame(); const ctx = useStyle(); const r = roles(ctx); const bg = props.bg ?? "accent";
  const k = interpolate(frame, [0, 12], [1.6, 1], { extrapolateRight: "clamp", easing: ease });
  const rot = frame * 0.6;
  return (
    <Out dur={dur}><Ground bg={bg}>
      <AbsoluteFill style={{ ...safePad(ctx.style, 10), justifyContent: "flex-start", alignItems: "center", paddingTop: 1920 * 0.16 }}>
        <ArthurLines lines={props.lines ?? []} bg={bg} dur={dur} />
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 540, top: 1140, transform: `translate(-50%,-50%) scale(${k})` }}>
        {[300, 400].map((R, i) => (
          <svg key={i} width={R * 2} height={R * 2} style={{ position: "absolute", left: -R, top: -R, transform: `rotate(${i ? -rot : rot}deg)` }}>
            <circle cx={R} cy={R} r={R - 4} fill="none" stroke={ink(bg, r)} strokeOpacity={0.55} strokeWidth={3} strokeDasharray="6 16" />
            <circle cx={R} cy={8} r={11} fill={ink(bg, r)} />
          </svg>
        ))}
        <div style={{ position: "absolute", left: -190, top: -190, width: 380, height: 380, borderRadius: 999, overflow: "hidden", background: "#FBF9F9", display: "flex", alignItems: "center", justifyContent: "center" }}>
          {props.media ? <BrandGrade><Img src={src(project, props.media)} style={{ width: "100%", height: "100%", objectFit: "cover" }} /></BrandGrade> : <Icon name={props.icon ?? "person"} size={240} color={r.accent} />}
        </div>
      </div>
      <Flash dur={dur} mode={props.flash} />
    </Ground></Out>
  );
};

// ── arthur_stripes: pantalla dividida en N franjas numeradas al enumerar (v06_s03) ──
export const ArthurStripes: React.FC<P> = ({ props, dur, project }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const ctx = useStyle(); const r = roles(ctx);
  const items: any[] = props.items ?? [];
  const n = items.length; const w = 1080 / n;
  const activeAt: number[] = props.active_at ?? [];   // segundos (relativos a la escena) en que cada ítem se activa
  const t = frame / fps;
  const active = activeAt.length ? activeAt.filter((x) => x <= t).length - 1 : -1;
  return (
    <Out dur={dur}><AbsoluteFill style={{ background: "#050505" }}>
      {items.map((it, i) => {
        const k = interpolate(frame, [i * 4, i * 4 + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
        const on = active < 0 || active === i;
        return (
          <div key={i} style={{ position: "absolute", left: i * w, top: 0, width: w - 4, height: 1920 * k, overflow: "hidden", opacity: on ? 1 : 0.28, transition: "none" }}>
            {it.media ? (isVid(it.media) ? <BrandGrade><OffthreadVideo muted src={src(project, it.media)} style={{ width: "100%", height: "100%", objectFit: "cover" }} /></BrandGrade>
              : <BrandGrade><Img src={src(project, it.media)} style={{ width: "100%", height: "100%", objectFit: "cover" }} /></BrandGrade>)
              : <div style={{ width: "100%", height: "100%", background: i % 2 ? r.accentDark : r.accent }} />}
            <AbsoluteFill style={{ background: "linear-gradient(transparent 35%, rgba(0,0,0,.55) 50%, transparent 65%)" }} />
            <div style={{ position: "absolute", top: 1920 * 0.44, width: "100%", textAlign: "center", fontFamily: SANS, fontWeight: 800, fontSize: 92, color: "#fff" }}>{i + 1}.</div>
            <div style={{ position: "absolute", top: 1920 * 0.52, width: "100%", textAlign: "center", fontFamily: SERIF, fontSize: n > 3 ? 58 : n > 2 ? 70 : 84, color: "#fff", padding: "0 10px", lineHeight: 1 }}>{it.label}</div>
          </div>
        );
      })}
    </AbsoluteFill></Out>
  );
};

// ── arthur_blocks: un bloque de acento que se divide en 2/4 con etiquetas (v19_s14) ──
export const ArthurBlocks: React.FC<P> = ({ props, dur }) => {
  const frame = useCurrentFrame(); const ctx = useStyle(); const r = roles(ctx); const bg = props.bg ?? "white";
  const labels: string[] = props.labels ?? ["A", "B"];
  const n = labels.length;
  const split = interpolate(frame, [12, 26], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const W = 620, H = 620, gap = 24 * split;
  const cols = n > 2 ? 2 : n, rows = n > 2 ? 2 : 1;
  return (
    <Out dur={dur}><Ground bg={bg}>
      <AbsoluteFill style={{ ...safePad(ctx.style, 10), justifyContent: "flex-start", alignItems: "center", paddingTop: 1920 * 0.16 }}>
        <ArthurLines lines={props.lines ?? []} bg={bg} dur={dur} />
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 540 - W / 2, top: 1100 - H / 2, width: W, height: H, display: "grid", gridTemplateColumns: `repeat(${cols},1fr)`, gridTemplateRows: `repeat(${rows},1fr)`, gap }}>
        {labels.map((l, i) => {
          const hl = props.highlight === i;
          return <div key={i} style={{ background: hl ? r.accent : i % 2 ? r.accentDark : r.accent, opacity: split < 1 && i > 0 ? split : 1, display: "flex", alignItems: "center", justifyContent: "center", borderRadius: 6, boxShadow: hl ? `0 0 60px ${r.accent}` : "none" }}>
            <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: n > 2 ? 52 : 64, color: "#fff", opacity: split, textAlign: "center", padding: 12 }}>{l}</div>
          </div>;
        })}
      </div>
      <Flash dur={dur} mode={props.flash} />
    </Ground></Out>
  );
};

// ── arthur_broll: b-roll oscuro de cine; el texto se queda fijo mientras cambian las tomas debajo ──
export const ArthurBroll: React.FC<P> = ({ props, dur, project }) => {
  const frame = useCurrentFrame(); const ctx = useStyle();
  const media: string[] = props.media ?? [];
  const per = Math.max(1, Math.floor(dur / Math.max(1, media.length)));
  const idx = Math.min(media.length - 1, Math.floor(frame / per));
  const local = frame - idx * per;
  const z = interpolate(local, [0, per], [1.04, 1.12]);
  const m = media[idx];
  return (
    <Out dur={dur}><AbsoluteFill style={{ background: "#000" }}>
      {m ? <AbsoluteFill style={{ transform: `scale(${z})` }}><BrandGrade>{isVid(m) ? <OffthreadVideo muted src={src(project, m)} style={{ width: "100%", height: "100%", objectFit: "cover" }} /> : <Img src={src(project, m)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />}</BrandGrade></AbsoluteFill> : null}
      <AbsoluteFill style={{ boxShadow: "inset 0 0 300px 120px rgba(0,0,0,.85)" }} />
      <AbsoluteFill style={{ background: "linear-gradient(rgba(0,0,0,.25), rgba(0,0,0,.55) 45%, rgba(0,0,0,.55) 60%, rgba(0,0,0,.2))" }} />
      <AbsoluteFill style={{ ...safePad(ctx.style, 20), justifyContent: "center", alignItems: "center" }}>
        <ArthurLines lines={props.lines ?? []} bg="black" dur={dur} />
      </AbsoluteFill>
      <Texture />
    </AbsoluteFill></Out>
  );
};

// ── arthur_number: cifra gigante que cae desde arriba sobre el A-roll/b-roll (v17 "1 / 8000 MILLONES", v11 "85% PASS") ──
export const ArthurNumber: React.FC<P> = ({ props, dur }) => {
  const frame = useCurrentFrame(); const ctx = useStyle(); const r = roles(ctx);
  const y = interpolate(frame, [0, 7], [-700, 0], { extrapolateRight: "clamp", easing: Easing.bezier(0.3, 1.4, 0.5, 1) });
  const k = interpolate(frame, [5, 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Out dur={dur}><AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 1920 * 0.44 }}>
      <div style={{ transform: `translateY(${y}px)`, fontFamily: SANS, fontWeight: 900, fontSize: props.px ?? 380, lineHeight: 0.85, color: "#fff", letterSpacing: "-0.06em", textShadow: "0 10px 40px rgba(0,0,0,.45)" }}>{props.value}</div>
      <div style={{ opacity: k, transform: `scale(${0.8 + 0.2 * k})`, fontFamily: SANS, fontWeight: 900, fontSize: 92, letterSpacing: "-0.02em", color: r.accent, WebkitTextStroke: "3px #fff", textTransform: "uppercase", marginTop: -10 }}>{props.label}</div>
    </AbsoluteFill></Out>
  );
};

export const ARTHUR_REGISTRY: Record<string, React.FC<any>> = {
  arthur_text: ArthurText, arthur_icons: ArthurIcons, arthur_orbit: ArthurOrbit,
  arthur_stripes: ArthurStripes, arthur_blocks: ArthurBlocks, arthur_broll: ArthurBroll, arthur_number: ArthurNumber,
};
