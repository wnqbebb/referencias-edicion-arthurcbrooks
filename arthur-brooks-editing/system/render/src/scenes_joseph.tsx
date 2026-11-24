// Escenas de los 10 principios (método Joseph, research/joseph + skills/arthur-brooks-style/JOSEPH_METODO.md).
// Todo se sincroniza a PALABRAS: los props traen tiempos absolutos (s) del transcript y se convierten a frames con `start`.
// Cámara: el mundo es más grande que la pantalla y la cámara sigue la punta de la línea / la bola (principios 4, 5 y 10).
import React from "react";
import { AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { BrandGrade, Texture, roles, useStyle } from "./kit";

type P = { props: any; dur: number; project: string; video: string; start: number };
const SERIF = "'Playfair Display'";
const SANS = "'Inter'";
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const inOut = Easing.bezier(0.65, 0, 0.35, 1);
const src = (project: string, p: string) => (p.startsWith("http") ? p : staticFile(`${project}/${p}`));
const isVid = (p?: string) => !!p && /\.(mp4|mov|webm|m4v)$/i.test(p);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** frame local de un tiempo absoluto (s) */
const useAt = (start: number) => {
  const { fps } = useVideoConfig();
  return (t: number | undefined, fallback = 0) => (t === undefined ? fallback : Math.round((t - start) * fps));
};

/** salida limpia: últimos 4 frames fundido */
const Out: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ opacity: f >= dur - 1 ? 0.0 : 1 }}>{children}</AbsoluteFill>;
};

/** fondo: negro / blanco / acento con papel (rugoso = más fuerte) */
const Paper: React.FC<{ bg: string; rough?: boolean }> = ({ bg, rough }) => {
  const ctx = useStyle(); const r = roles(ctx);
  const base = bg === "white" ? "#F6F4F1" : bg === "accent" ? r.accent : "#0A0A0C";
  const dark = bg !== "white";
  return (
    <AbsoluteFill style={{ background: base }}>
      {bg === "black" ? <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, rgba(255,255,255,.07), transparent 65%)" }} /> : null}
      <Texture kind="paper" opacity={rough ? (bg === "black" ? 0.8 : 1) : bg === "black" ? 0.45 : 0.85} dark={bg === "black"} />
      {rough ? <Texture kind="paper" opacity={bg === "black" ? 0.35 : 0.6} dark={bg === "black"} /> : null}
      <AbsoluteFill style={{ boxShadow: dark ? "inset 0 0 260px 40px rgba(0,0,0,.55)" : "inset 0 0 220px 20px rgba(0,0,0,.08)" }} />
    </AbsoluteFill>
  );
};

/** texto cinematográfico (principio 1): pequeño arriba + grande (serif itálica o sans 800) + pequeño abajo, se enciende */
export const Cine: React.FC<{ small?: string; big: string; after?: string; sans?: boolean; color: string; k: number; px?: number; align?: "center" | "left" | "right"; early?: boolean }> = ({ small, big, after, sans, color, k: kBig, px = 130, align = "center", early = true }) => {
  // el texto pequeño entra al empezar la escena (early) y la palabra grande se enciende en su palabra (gris → color)
  const fr = useCurrentFrame();
  const kS = early ? interpolate(fr, [2, 9], [0, 1], clamp) : kBig;
  const k = Math.max(kBig, 0);
  const dimmed = interpolate(k, [0, 1], [0.22, 1]);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: align === "center" ? "center" : align === "left" ? "flex-start" : "flex-end", opacity: kS > 0 || k > 0 ? 1 : 0 }}>
      {small ? <div style={{ fontFamily: SANS, fontWeight: 400, fontSize: Math.max(40, px * 0.34), color, opacity: Math.max(kS, Math.min(1, k * 2)), lineHeight: 1.05, marginBottom: -px * 0.05, whiteSpace: "nowrap" }}>{small}</div> : null}
      <div style={{ fontFamily: sans ? SANS : SERIF, fontStyle: sans ? "normal" : "italic", fontWeight: sans ? 800 : 700, fontSize: px, lineHeight: 0.95, letterSpacing: sans ? "-0.05em" : "-0.025em", color, opacity: early ? Math.max(kS * 0.22, dimmed * (k > 0 ? 1 : 0) || kS * 0.22) : dimmed, filter: `blur(${(1 - k) * 5}px)`, whiteSpace: "nowrap" }}>{big}</div>
      {after ? <div style={{ fontFamily: SANS, fontWeight: 400, fontSize: Math.max(40, px * 0.34), color, opacity: Math.max(kS * 0.0, Math.min(1, k * 2)), lineHeight: 1.05, marginTop: px * 0.04, whiteSpace: "nowrap" }}>{after}</div> : null}
    </div>
  );
};

// ── j_graph (principio 10): fondo oscuro con textura, cuadrícula fina que brilla, bola azul que dibuja la línea,
//    la cámara la sigue; cada punto se alcanza en su palabra (props.points[i].t). Al final zoom-out para ver todo.
export const JGraph: React.FC<P> = ({ props, dur, start }) => {
  const f = useCurrentFrame(); const at = useAt(start); const ctx = useStyle(); const r = roles(ctx);
  const pts: { x: number; y: number; t?: number; label?: string }[] = props.points ?? [{ x: 0, y: 0 }, { x: 1, y: 1 }];
  const W = 1500, H = 1500, X0 = 150, Y0 = 1350; // mundo
  const P = pts.map((p) => [X0 + p.x * (W - 2 * X0 + 100), Y0 - p.y * (Y0 - 200)]);
  const times = pts.map((p, i) => at(p.t, Math.round(8 + (i / Math.max(1, pts.length - 1)) * dur * 0.7)));
  // progreso continuo sobre los segmentos
  let seg = 0, u = 0;
  for (let i = 0; i < pts.length - 1; i++) {
    if (f >= times[i]) { seg = i; u = interpolate(f, [times[i], Math.max(times[i] + 1, times[i + 1])], [0, 1], { ...clamp, easing: inOut }); }
  }
  const head = [P[seg][0] + (P[seg + 1 < P.length ? seg + 1 : seg][0] - P[seg][0]) * u, P[seg][1] + (P[seg + 1 < P.length ? seg + 1 : seg][1] - P[seg][1]) * u];
  const drawn = [...P.slice(0, seg + 1), head];
  const d = drawn.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" ");
  const end = times[times.length - 1];
  const out = interpolate(f, [end + 6, end + 26], [0, 1], { ...clamp, easing: ease });
  const zoom = interpolate(out, [0, 1], [1.35, 0.72]);
  const cx = interpolate(out, [0, 1], [head[0], W / 2]); const cy = interpolate(out, [0, 1], [head[1], H / 2 + 60]);
  const grid = [];
  for (let i = 0; i <= 8; i++) grid.push(<line key={"h" + i} x1={X0} x2={W - 50} y1={Y0 - i * 145} y2={Y0 - i * 145} stroke="rgba(255,255,255,.13)" strokeWidth={2} />);
  const kT = interpolate(f, [at(props.text_t, 4), at(props.text_t, 4) + 8], [0, 1], clamp);
  return (
    <Out dur={dur}>
      <Paper bg="black" />
      <AbsoluteFill style={{ transform: `translate(${540 - cx * zoom}px, ${1060 - cy * zoom}px) scale(${zoom})`, transformOrigin: "0 0" }}>
        <svg width={W} height={H} style={{ overflow: "visible", filter: "drop-shadow(0 0 6px rgba(255,255,255,.25))" }}>
          {grid}
          <line x1={X0} x2={X0} y1={120} y2={Y0} stroke="rgba(255,255,255,.85)" strokeWidth={3} />
          <line x1={X0} x2={W - 50} y1={Y0} y2={Y0} stroke="rgba(255,255,255,.85)" strokeWidth={3} />
          <text x={X0 - 34} y={300} fill="rgba(255,255,255,.75)" fontFamily="Inter" fontWeight={700} fontSize={30} letterSpacing="0.2em" transform={`rotate(-90 ${X0 - 34} 300)`}>{props.y_label ?? ""}</text>
          <text x={W / 2} y={Y0 + 70} fill="rgba(255,255,255,.75)" fontFamily="Inter" fontWeight={700} fontSize={30} letterSpacing="0.2em" textAnchor="middle">{props.x_label ?? ""}</text>
          <path d={d} fill="none" stroke="rgba(255,255,255,.95)" strokeWidth={7} strokeLinejoin="round" strokeLinecap="round" />
          {pts.map((p, i) => p.label && f >= times[i] ? <text key={i} x={P[i][0] + 34} y={P[i][1] - 30} fill="#fff" fontFamily="Inter" fontWeight={600} fontSize={44} opacity={interpolate(f, [times[i], times[i] + 6], [0, 1], clamp)}>{p.label}</text> : null)}
          <circle cx={head[0]} cy={head[1]} r={30} fill={r.accent} style={{ filter: `drop-shadow(0 0 24px ${r.accent}) drop-shadow(0 0 8px ${r.accent})` }} />
        </svg>
      </AbsoluteFill>
      <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 330 }}>
        <Cine small={props.small} big={props.big ?? ""} after={props.after} sans={props.sans !== false} color="#fff" k={kT} px={props.px ?? 150} />
      </AbsoluteFill>
    </Out>
  );
};

// ── j_line (principios 4 y 5): línea gruesa de acento que se dibuja, el TEXTO la interrumpe y la línea sigue hacia el
//    siguiente texto; la cámara sigue la punta. shape: "zigzag" (progresión por fases) | "down" | "arc". Punto blanco opcional.
export const JLine: React.FC<P> = ({ props, dur, start, project }) => {
  const f = useCurrentFrame(); const at = useAt(start); const ctx = useStyle(); const r = roles(ctx);
  const bg = props.bg ?? "white";
  const ink = bg === "white" ? "#111" : "#fff";
  const stops: { t?: number; small?: string; big: string; after?: string; sans?: boolean; img?: string }[] = props.stops ?? [];
  const n = stops.length;
  const shape = props.shape ?? "zigzag";
  const GAP = 820; // distancia vertical entre paradas en el mundo
  const pos = stops.map((_, i) => {
    const x = shape === "zigzag" ? (i % 2 ? 640 : 440) : shape === "arc" ? 540 + Math.sin(i * 1.3) * 160 : 540;
    return [x, 700 + i * GAP];
  });
  const times = stops.map((s, i) => at(s.t, Math.round(6 + (i / Math.max(1, n)) * dur * 0.8)));
  const TXT = 150; // medio alto del bloque de texto (hueco donde la línea se interrumpe)
  // segmentos: entrada desde arriba → parada0, parada i → parada i+1 (de borde inferior a borde superior del texto)
  const segs: { a: number[]; b: number[]; t0: number; t1: number }[] = [];
  segs.push({ a: [pos[0][0] - 260, pos[0][1] - 700], b: [pos[0][0], pos[0][1] - TXT], t0: times[0] - 14, t1: times[0] });
  for (let i = 0; i < n - 1; i++) segs.push({ a: [pos[i][0], pos[i][1] + TXT], b: [pos[i + 1][0], pos[i + 1][1] - TXT], t0: times[i] + 4, t1: times[i + 1] });
  if (props.tail !== false && n) segs.push({ a: [pos[n - 1][0], pos[n - 1][1] + TXT], b: [pos[n - 1][0] + 240, pos[n - 1][1] + 700], t0: times[n - 1] + 4, t1: times[n - 1] + 26 });
  const curve = (a: number[], b: number[]) => {
    const my = (a[1] + b[1]) / 2;
    return `M${a[0]},${a[1]} C${a[0]},${my} ${b[0]},${my} ${b[0]},${b[1]}`;
  };
  let tip = segs[0].a;
  const paths = segs.map((s, i) => {
    const u = interpolate(f, [s.t0, Math.max(s.t0 + 1, s.t1)], [0, 1], { ...clamp, easing: inOut });
    if (u > 0) { const mt = u; const x = (1 - mt) ** 3 * s.a[0] + 3 * (1 - mt) ** 2 * mt * s.a[0] + 3 * (1 - mt) * mt * mt * s.b[0] + mt ** 3 * s.b[0]; const my = (s.a[1] + s.b[1]) / 2; const y = (1 - mt) ** 3 * s.a[1] + 3 * (1 - mt) ** 2 * mt * my + 3 * (1 - mt) * mt * mt * my + mt ** 3 * s.b[1]; tip = [x, y]; }
    return <path key={i} d={curve(s.a, s.b)} pathLength={1} fill="none" stroke={r.accent} strokeWidth={34} strokeLinecap="round" strokeDasharray="1 1" strokeDashoffset={1 - u} opacity={u > 0.01 ? 1 : 0} />;
  });
  // cámara: sigue la punta (suavizada hacia la parada activa)
  const camY = tip[1];
  const camX = interpolate(tip[0], [300, 780], [470, 610]);
  const z = props.zoom ?? 1;
  return (
    <Out dur={dur}>
      <Paper bg={bg} />
      <AbsoluteFill style={{ transform: `translate(${540 - camX * z}px, ${960 - camY * z}px) scale(${z})`, transformOrigin: "0 0" }}>
        <svg width={1080} height={700 + n * GAP + 800} style={{ position: "absolute", overflow: "visible" }}>{paths}</svg>
        {stops.map((s, i) => {
          const k = interpolate(f, [times[i] - 2, times[i] + 6], [0, 1], clamp);
          return (
            <div key={i} style={{ position: "absolute", left: 40, top: pos[i][1] - TXT, width: 1000, height: TXT * 2, display: "flex", justifyContent: "center", alignItems: "center" }}>
              {s.img ? <Img src={src(project, s.img)} style={{ position: "absolute", top: TXT * 2 + 40, left: pos[i][0] > 540 ? 60 : 560, width: 360, height: 420, objectFit: "cover", borderRadius: 8, opacity: k, filter: "grayscale(.2) contrast(1.05)", boxShadow: "0 18px 40px rgba(0,0,0,.3)" }} /> : null}
              <Cine small={s.small} big={s.big} after={s.after} sans={s.sans} color={ink} k={k} px={props.px ?? 128} early={false} />
            </div>
          );
        })}
        {props.dot ? <div style={{ position: "absolute", left: tip[0] - 20, top: tip[1] - 20, width: 40, height: 40, borderRadius: 99, background: "#fff", boxShadow: `0 0 0 6px ${r.accent}55, 0 0 30px rgba(255,255,255,.9)` }} /> : null}
      </AbsoluteFill>
    </Out>
  );
};

// ── j_quote (principio 6): fondo blanco o de acento con papel MUY rugoso, comillas alrededor del centro, texto en medio ──
export const JQuote: React.FC<P> = ({ props, dur, start }) => {
  const f = useCurrentFrame(); const at = useAt(start); const ctx = useStyle(); const r = roles(ctx);
  const bg = props.bg ?? "white";
  const ink = bg === "white" ? r.accent : "#fff";
  const kq = interpolate(f, [0, 8], [0, 1], { ...clamp, easing: ease });
  const k = interpolate(f, [at(props.t, 6), at(props.t, 6) + 8], [0, 1], clamp);
  const q = { fontFamily: SERIF, fontStyle: "italic" as const, fontWeight: 700, fontSize: 230, color: ink, lineHeight: 1, opacity: kq };
  return (
    <Out dur={dur}>
      <Paper bg={bg} rough />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div style={{ position: "relative", padding: "40px 90px", transform: `scale(${0.96 + 0.04 * kq})` }}>
          <div style={{ ...q, position: "absolute", left: 0, top: -30, transform: `translateX(${(1 - kq) * -40}px)` }}>“</div>
          <div style={{ ...q, position: "absolute", right: 0, bottom: -90, transform: `translateX(${(1 - kq) * 40}px)` }}>”</div>
          <Cine small={props.small} big={props.big} after={props.after} sans={props.sans} color={ink} k={k} px={props.px ?? 120} />
        </div>
      </AbsoluteFill>
    </Out>
  );
};

/** filtro de "pintado rugoso": desplaza los bordes con turbulencia */
const RoughDefs: React.FC<{ id: string; scale?: number }> = ({ id, scale = 14 }) => (
  <svg width={0} height={0} style={{ position: "absolute" }}>
    <filter id={id}><feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves={3} seed={4} /><feDisplacementMap in="SourceGraphic" scale={scale} /></filter>
  </svg>
);

// ── j_illus (principios 7, 8 y 9): figura recortada (PNG sin fondo) convertida a ilustración Arthur: monocroma en el
//    acento, textura pintada/rugosa, bordes desplazados, sangra desde abajo hacia el centro. mode: center | side | object
export const JIllus: React.FC<P> = ({ props, dur, start, project }) => {
  const f = useCurrentFrame(); const at = useAt(start); const ctx = useStyle(); const r = roles(ctx);
  const bg = props.bg ?? "white";
  const ink = bg === "white" ? "#111" : "#fff";
  const mode = props.mode ?? "center";
  const k = interpolate(f, [0, 16], [0, 1], { ...clamp, easing: ease });
  const kT = interpolate(f, [at(props.t, 8), at(props.t, 8) + 8], [0, 1], clamp);
  const zoom = interpolate(f, [0, dur], [1.0, 1.06]);
  const fig = props.media ? (
    <div style={{ position: "relative", width: mode === "side" ? 640 : 860, height: mode === "side" ? 1200 : 1250, transform: `scale(${zoom}) translateY(${(1 - k) * 60}px)`, opacity: k, filter: "url(#rough)" }}>
      {props.fill ? <div style={{ position: "absolute", inset: 0, background: props.fill, WebkitMaskImage: `url(${src(project, props.media)})`, WebkitMaskSize: "contain", WebkitMaskRepeat: "no-repeat", WebkitMaskPosition: "bottom", maskImage: `url(${src(project, props.media)})`, maskSize: "contain", maskRepeat: "no-repeat", maskPosition: "bottom" }} /> : null}
      <Img src={src(project, props.media)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "contain", objectPosition: "bottom", mixBlendMode: props.fill ? "multiply" : "normal", opacity: props.fill ? 0.18 : 1, filter: props.keep_color ? "contrast(1.1)" : "grayscale(1) contrast(1.6) brightness(1.05)" }} />
      {props.keep_color || props.fill ? null : (
        <div style={{ position: "absolute", inset: 0, background: bg === "white" ? r.accent : "#fff", mixBlendMode: bg === "white" ? "screen" : "multiply",
          WebkitMaskImage: `url(${src(project, props.media)})`, WebkitMaskSize: "contain", WebkitMaskRepeat: "no-repeat", WebkitMaskPosition: "bottom", maskImage: `url(${src(project, props.media)})`, maskSize: "contain", maskRepeat: "no-repeat", maskPosition: "bottom" }} />
      )}
      <div style={{ position: "absolute", inset: 0, backgroundImage: `url(${staticFile("textures/cloth.png")})`, backgroundSize: "cover", mixBlendMode: "multiply", opacity: props.fill ? 0.28 : 0.55,
        WebkitMaskImage: `url(${src(project, props.media)})`, WebkitMaskSize: "contain", WebkitMaskRepeat: "no-repeat", WebkitMaskPosition: "bottom", maskImage: `url(${src(project, props.media)})`, maskSize: "contain", maskRepeat: "no-repeat", maskPosition: "bottom" }} />
    </div>
  ) : null;
  return (
    <Out dur={dur}>
      <Paper bg={bg} />
      <RoughDefs id="rough" />
      {mode === "side" ? (
        <>
          <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "flex-start", paddingLeft: 0 }}>{fig}</AbsoluteFill>
          <AbsoluteFill style={{ justifyContent: "center", alignItems: "flex-end", paddingRight: 150 }}>
            <Cine small={props.small} big={props.big ?? ""} after={props.after} sans={props.sans} color={bg === "white" ? r.accent : "#fff"} k={kT} px={props.px ?? 120} align="right" />
          </AbsoluteFill>
        </>
      ) : (
        <>
          <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center" }}>{fig}</AbsoluteFill>
          <AbsoluteFill style={{ background: `linear-gradient(transparent 82%, ${bg === "white" ? "#F6F4F1" : "#0A0A0C"})` }} />
          <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 330 }}>
            <Cine small={props.small} big={props.big ?? ""} after={props.after} sans={props.sans} color={bg === "white" ? r.accent : "#fff"} k={kT} px={props.px ?? 130} />
          </AbsoluteFill>
        </>
      )}
      <Texture kind="paper" opacity={0.35} dark={bg !== "white"} />
      {ink ? null : null}
    </Out>
  );
};

// ── j_half (principio 8, variante): media luna con textura de tela a la izquierda y texto limpio rotando alrededor ──
export const JHalf: React.FC<P> = ({ props, dur, start }) => {
  const f = useCurrentFrame(); const at = useAt(start); const ctx = useStyle(); const r = roles(ctx);
  const bg = props.bg ?? "white";
  const k = interpolate(f, [0, 14], [0, 1], { ...clamp, easing: ease });
  const words: string[] = props.ring ?? [];
  const rot = interpolate(f, [0, dur], [-20, 25]);
  const kT = interpolate(f, [at(props.t, 8), at(props.t, 8) + 8], [0, 1], clamp);
  return (
    <Out dur={dur}>
      <Paper bg={bg} />
      <RoughDefs id="roughH" scale={10} />
      <div style={{ position: "absolute", left: -700 + (1 - k) * -200, top: 960 - 500, width: 1000, height: 1000, borderRadius: 999, background: r.accent, filter: "url(#roughH)", overflow: "hidden" }}>
        <AbsoluteFill style={{ backgroundImage: `url(${staticFile("textures/cloth.png")})`, backgroundSize: "cover", mixBlendMode: "multiply", opacity: 0.7 }} />
      </div>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <defs><path id="ringP" d="M -200,380 A 580,580 0 0,1 -200,1540" /></defs>
        <g transform={`rotate(${rot} -200 960)`} opacity={k}>
          {words.map((w, i) => <text key={i} fontFamily="Inter" fontWeight={500} fontSize={40} fill={bg === "white" ? "#222" : "#fff"} letterSpacing="0.06em"><textPath href="#ringP" startOffset={`${8 + i * (80 / Math.max(1, words.length))}%`}>{w}</textPath></text>)}
        </g>
      </svg>
      <div style={{ position: "absolute", right: 110, top: 900, display: "flex", justifyContent: "flex-end" }}>
        <Cine small={props.small} big={props.big ?? ""} after={props.after} sans={props.sans} color={bg === "white" ? r.accent : "#fff"} k={kT} px={props.px ?? 110} align="right" />
      </div>
    </Out>
  );
};

// ── j_painting (principio 3): slide de cámara que revela la pintura, textura de pintura que se mueve CON ella a media
//    fuerza + papel rugoso, texto alrededor del sujeto (props.text_pos: top|bottom)
export const JPainting: React.FC<P> = ({ props, dur, start, project }) => {
  const f = useCurrentFrame(); const at = useAt(start);
  const slide = interpolate(f, [0, 22], [260, 0], { ...clamp, easing: ease });
  const zoom = interpolate(f, [0, dur], [1.06, 1.14]);
  const kT = interpolate(f, [at(props.t, 8), at(props.t, 8) + 8], [0, 1], clamp);
  return (
    <Out dur={dur}>
      <AbsoluteFill style={{ background: "#000" }}>
        <AbsoluteFill style={{ transform: `translateX(${slide}px) scale(${zoom})` }}>
          <Img src={src(project, props.media)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "contrast(1.04) saturate(0.88) sepia(0.08)" }} />
          <AbsoluteFill style={{ backgroundImage: `url(${staticFile("textures/paint.png")})`, backgroundSize: "cover", mixBlendMode: "overlay", opacity: 0.28 }} />
          <AbsoluteFill style={{ backgroundImage: `url(${staticFile("textures/paper.png")})`, backgroundSize: "cover", mixBlendMode: "multiply", opacity: 0.32 }} />
        </AbsoluteFill>
        <AbsoluteFill style={{ boxShadow: "inset 0 0 280px 90px rgba(0,0,0,.8)" }} />
        <AbsoluteFill style={{ justifyContent: props.text_pos === "bottom" ? "flex-end" : "flex-start", alignItems: "center", padding: props.text_pos === "bottom" ? "0 0 560px" : "360px 0 0" }}>
          <Cine small={props.small} big={props.big ?? ""} after={props.after} sans={props.sans} color="#fff" k={kT} px={props.px ?? 130} />
        </AbsoluteFill>
      </AbsoluteFill>
    </Out>
  );
};

// ── j_broll (principio 2): b-roll literal con papel claro, bordes oscurecidos Y desenfocados (foco al centro), texto fijo
//    encima que describe la escena; varias tomas bajo el mismo texto
export const JBroll: React.FC<P> = ({ props, dur, start, project }) => {
  const f = useCurrentFrame(); const at = useAt(start);
  const media: string[] = Array.isArray(props.media) ? props.media : [props.media];
  const cuts = (props.cuts as number[] | undefined)?.map((t) => at(t)) ?? media.map((_, i) => Math.round((i * dur) / media.length));
  let idx = 0;
  cuts.forEach((c, i) => { if (f >= c) idx = i; });
  const local = f - cuts[idx];
  const z = interpolate(local, [0, dur], [1.05, 1.13]);
  const m = media[idx];
  const kT = interpolate(f, [at(props.t, 4), at(props.t, 4) + 8], [0, 1], clamp);
  const layer = (blur: boolean) => (
    <AbsoluteFill style={{ transform: `scale(${z})`, filter: blur ? "blur(14px)" : undefined }}>
      <BrandGrade>{isVid(m) ? <OffthreadVideo muted src={src(project, m)} style={{ width: "100%", height: "100%", objectFit: "cover" }} /> : <Img src={src(project, m)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />}</BrandGrade>
    </AbsoluteFill>
  );
  return (
    <Out dur={dur}>
      <AbsoluteFill style={{ background: "#000" }}>
        {layer(true)}
        <AbsoluteFill style={{ WebkitMaskImage: "radial-gradient(ellipse 62% 48% at 50% 48%, #000 55%, transparent 100%)", maskImage: "radial-gradient(ellipse 62% 48% at 50% 48%, #000 55%, transparent 100%)" }}>{layer(false)}</AbsoluteFill>
        <AbsoluteFill style={{ boxShadow: "inset 0 0 300px 110px rgba(0,0,0,.82)" }} />
        <AbsoluteFill style={{ background: "rgba(0,0,0,.18)" }} />
        <Texture kind="paper" opacity={0.4} dark />
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <Cine small={props.small} big={props.big ?? ""} after={props.after} sans={props.sans} color="#fff" k={kT} px={props.px ?? 140} />
        </AbsoluteFill>
      </AbsoluteFill>
    </Out>
  );
};

export const JOSEPH_REGISTRY: Record<string, React.FC<any>> = {
  j_graph: JGraph, j_line: JLine, j_quote: JQuote, j_illus: JIllus, j_half: JHalf, j_painting: JPainting, j_broll: JBroll,
};
