// Escenas del formato DOCUMENTAL BIOGRÁFICO (referencia maestra v01 'my life') y de los otros formatos de Arthur Brooks.
// Cada componente cita el plano de referencia del que se extrajo (evidencia en styles/arthur-brooks/references/).
import React from "react";
import { AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Texture, color, popStyle, roles, safePad, useEnter, useExit, useStyle, BrandGrade } from "./kit";

type P = { props: any; dur: number; project: string; video: string; start: number };
const src = (project: string, p: string) => (p.startsWith("http") ? p : staticFile(`${project}/${p}`));
const isVid = (p?: string) => !!p && /\.(mp4|mov|webm|m4v)$/i.test(p);
const M: React.FC<{ project: string; path: string; style?: React.CSSProperties }> = ({ project, path, style }) => {
  const st = { width: "100%", height: "100%", objectFit: "cover" as const, ...style };
  return <BrandGrade>{isVid(path) ? <OffthreadVideo muted src={src(project, path)} style={st} /> : <Img src={src(project, path)} style={st} />}</BrandGrade>;
};
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const Out: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => <AbsoluteFill style={{ opacity: useExit(dur) }}>{children}</AbsoluteFill>;
const PAPER = "#F7F7F5";

/** Foto "impresa": borde blanco, sombra suave, rotación leve; cae con easing (v01 0:22, 0:52, 1:07). */
const PrintedPhoto: React.FC<{ project: string; path: string; w: number; rot: number; delay: number; x?: number; y?: number; border?: boolean }> = ({ project, path, w, rot, delay, x = 0, y = 0, border = true }) => {
  const frame = useCurrentFrame();
  const k = interpolate(frame - delay, [0, 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  return (
    <div style={{ position: "absolute", left: "50%", top: "50%", width: w, transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y + (1 - k) * 60}px)) rotate(${rot * (0.6 + 0.4 * k)}deg) scale(${1.08 - 0.08 * k})`, opacity: k, background: "#fff", padding: border ? w * 0.03 : 0, boxShadow: "0 18px 40px rgba(0,0,0,.28), 0 2px 6px rgba(0,0,0,.15)" }}>
      <div style={{ width: "100%", aspectRatio: "4/5", overflow: "hidden" }}><M project={project} path={path} /></div>
    </div>
  );
};

/** name_card — 'My name is / Arthur Brooks.' sobre fondo de estudio blanco (v01 0:01.5). */
export const NameCard: React.FC<P> = ({ props, dur, project }) => {
  const ctx = useStyle();
  const r = roles(ctx);
  const p = useEnter(0), q = useEnter(5);
  return (
    <Out dur={dur}><AbsoluteFill style={{ background: PAPER }}>
      {props.media ? <AbsoluteFill style={{ top: "28%" }}><M project={project} path={props.media} style={{ objectFit: "contain" }} /></AbsoluteFill> : null}
      <AbsoluteFill style={{ ...safePad(ctx.style, 30), alignItems: "center" }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start" }}>
          <div style={{ ...popStyle(p, ctx.style), fontFamily: `'${ctx.style.fonts.sans.family}'`, fontSize: 40, color: "#111" }}>{props.kicker ?? "Me llamo"}</div>
          <div style={{ ...popStyle(q, ctx.style), fontFamily: `'${ctx.style.fonts.special.family}'`, fontStyle: "italic", fontWeight: 700, fontSize: 104, letterSpacing: "-0.04em", lineHeight: 0.95, color: r.accent }}>{props.name}</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill></Out>
  );
};

/** paper_collage — papel blanco + 1–3 fotos + etiqueta pequeña con palabra serif azul (v01 0:03 'I write / speak / teach', 0:06 'I'm a professor'). */
export const PaperCollage: React.FC<P> = ({ props, dur, project }) => {
  const ctx = useStyle();
  const r = roles(ctx);
  const imgs: string[] = props.images ?? [];
  const labels: { small?: string; word: string }[] = props.labels ?? [];
  const lay = [[{ x: 0, y: 120, rot: -2 }], [{ x: -175, y: 90, rot: -4 }, { x: 175, y: 160, rot: 3 }], [{ x: -230, y: 70, rot: -5 }, { x: 0, y: 190, rot: 2 }, { x: 230, y: 100, rot: 4 }]][Math.min(2, Math.max(0, imgs.length - 1))];
  const w = imgs.length > 2 ? 400 : imgs.length > 1 ? 470 : 620;
  return (
    <Out dur={dur}><AbsoluteFill style={{ background: PAPER }}>
      {imgs.map((im, i) => <PrintedPhoto key={i} project={project} path={im} w={w} rot={lay[i].rot} x={lay[i].x} y={lay[i].y} delay={i * 6} />)}
      <AbsoluteFill style={{ ...safePad(ctx.style, 20), justifyContent: "flex-start", alignItems: "center", paddingTop: 1920 * 0.2 }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 6, alignItems: "center" }}>
          {labels.map((l, i) => {
            const k = useEnter(4 + i * 6);
            return (
              <div key={i} style={{ ...popStyle(k, ctx.style), display: "flex", alignItems: "baseline", gap: 8 }}>
                {l.small ? <span style={{ fontFamily: `'${ctx.style.fonts.sans.family}'`, fontSize: 46, color: "#222" }}>{l.small}</span> : null}
                <span style={{ fontFamily: `'${ctx.style.fonts.special.family}'`, fontStyle: "italic", fontWeight: 700, fontSize: 118, lineHeight: 1, letterSpacing: "-0.03em", color: i % 2 ? "#111" : r.accent }}>{l.word}</span>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill></Out>
  );
};

/** timeline — línea fina con ticks, etiquetas versalitas, marcador azul que avanza; fotos caen encima (v01 0:36, 0:51, 1:16, 2:07). */
export const Timeline: React.FC<P> = ({ props, dur, project }) => {
  const ctx = useStyle();
  const frame = useCurrentFrame();
  const r = roles(ctx);
  const ms: { label: string; age: string }[] = props.milestones ?? [];
  const active = props.active ?? ms.length - 1;
  const onDark = props.over_aroll === true;
  const ink = onDark ? "#fff" : "#111";
  const gap = 470;
  // el hito activo y el anterior quedan centrados dentro de la zona segura
  const target = active > 0 ? active * gap - gap / 2 : 0;
  const camX = interpolate(frame, [0, 22], [Math.max(0, target - gap), target], { extrapolateRight: "clamp", easing: ease });
  const k = interpolate(frame, [6, 26], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const body = (
    <div style={{ position: "absolute", left: 540 - camX, top: props.y ?? 1920 * 0.36, width: gap * (ms.length + 1) }}>
      <div style={{ position: "absolute", left: -2000, right: -2000, top: 0, height: 2, background: onDark ? "rgba(255,255,255,.7)" : "rgba(0,0,0,.55)" }} />
      {ms.map((m, i) => (
        <div key={i} style={{ position: "absolute", left: i * gap, top: -96, transform: "translateX(-50%)", textAlign: "center", width: 420 }}>
          <div style={{ fontFamily: `'${ctx.style.fonts.sans.family}'`, fontSize: 42, letterSpacing: "0.04em", textTransform: "uppercase", color: ink, opacity: i === active ? 1 : 0.55, fontWeight: i === active ? 700 : 500, lineHeight: 1.25 }}>{m.label}</div>
          <div style={{ width: 2, height: 28, background: ink, margin: "10px auto 0" }} />
          <div style={{ fontFamily: `'${ctx.style.fonts.sans.family}'`, fontSize: 54, color: ink, marginTop: 18, opacity: i === active ? 1 : 0.55 }}>{m.age}</div>
        </div>
      ))}
      <div style={{ position: "absolute", left: (active - 1) * gap + gap * (0.35 + 0.3 * k), top: -4, width: 70, height: 10, background: r.accent, borderRadius: 2 }} />
    </div>
  );
  return (
    <Out dur={dur}>
      {onDark ? null : <AbsoluteFill style={{ background: PAPER }} />}
      {body}
      {(props.images ?? []).map((im: string, i: number) => <PrintedPhoto key={i} project={project} path={im} w={470} rot={[-6, 5, -3][i % 3]} x={[-70, 90, 0][i % 3]} y={300 + i * 40} delay={10 + i * 8} />)}
    </Out>
  );
};

/** archival_photo — foto de archivo a sangre: B/N o color viejo, grano, scanlines CRT, aro de resaltado opcional (v01 0:24, 0:39). */
export const ArchivalPhoto: React.FC<P> = ({ props, dur, project }) => {
  const frame = useCurrentFrame();
  const ctx = useStyle();
  const z = interpolate(frame, [0, dur], [1.04, 1.12]);
  const ring = props.ring as { x: number; y: number; r: number } | undefined;
  const rk = interpolate(frame, [6, 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  return (
    <Out dur={dur}><AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ transform: `scale(${z})`, filter: props.bw ? "grayscale(1) contrast(1.15) brightness(0.95)" : "sepia(0.25) saturate(0.9) contrast(1.05)" }}><M project={project} path={props.media} /></AbsoluteFill>
      {props.scanlines !== false ? <AbsoluteFill style={{ backgroundImage: "repeating-linear-gradient(0deg, rgba(0,0,0,.22) 0 2px, transparent 2px 4px)", mixBlendMode: "multiply" }} /> : null}
      <AbsoluteFill style={{ boxShadow: "inset 0 0 220px 60px rgba(0,0,0,.55)" }} />
      {ring ? <div style={{ position: "absolute", left: ring.x * 1080 - ring.r, top: ring.y * 1920 - ring.r, width: ring.r * 2, height: ring.r * 2, borderRadius: 999, border: "6px solid rgba(190,240,255,.95)", boxShadow: "0 0 30px rgba(160,230,255,.8)", opacity: rk, transform: `scale(${1.25 - 0.25 * rk})` }} /> : null}
      <Texture />
    </AbsoluteFill></Out>
  );
};

/** video_card — b-roll dentro de tarjeta redondeada sobre negro, con caption pequeño (v01 0:45 'support a family', 1:34). */
export const VideoCard: React.FC<P> = ({ props, dur, project }) => {
  const ctx = useStyle();
  const p = useEnter(0, 1.2);
  return (
    <Out dur={dur}><AbsoluteFill style={{ background: "#050505", ...safePad(ctx.style, 0), justifyContent: "center", alignItems: "center" }}>
      <div style={{ width: props.size === "small" ? 560 : 760, aspectRatio: props.size === "small" ? "4/3" : "9/14", borderRadius: 34, overflow: "hidden", transform: `scale(${0.92 + 0.08 * p})`, opacity: p, boxShadow: "0 30px 80px rgba(0,0,0,.6)" }}>
        <M project={project} path={props.media} />
      </div>
    </AbsoluteFill></Out>
  );
};

/** split_layout — podcast pantalla dividida: close-up arriba (recorte) / plano abierto abajo (v05, v14, v15, v20). */
export const SplitLayout: React.FC<P> = ({ props, dur, video, start }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ratio = props.ratio ?? 0.66;
  const top = props.top_media ? staticFile(props.top_media) : staticFile(video);
  const bottom = props.bottom_media ? staticFile(props.bottom_media) : staticFile(video);
  const from = Math.round(start * fps);
  const fx = props.face_x ?? 0.5, fy = props.face_y ?? 0.35, zoom = props.zoom ?? 1.9;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: `${ratio * 100}%`, overflow: "hidden" }}>
        <OffthreadVideo src={top} startFrom={from} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${zoom})`, transformOrigin: `${fx * 100}% ${fy * 100}%` }} />
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: `${(1 - ratio) * 100}%`, overflow: "hidden", borderTop: "2px solid rgba(0,0,0,.9)" }}>
        <OffthreadVideo muted src={bottom} startFrom={from} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
    </AbsoluteFill>
  );
};

/** kinetic_type — tipografía manuscrita palabra por palabra sobre papel crema o negro (v04). */
export const KineticType: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dark = props.dark === true;
  const lines: { text: string; size?: number; at?: number }[] = props.lines ?? [];
  return (
    <Out dur={dur}><AbsoluteFill style={{ background: dark ? "#2E2C2B" : "#F3EEE3", ...safePad(ctx.style, 30), justifyContent: "center", alignItems: "center" }}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", transform: "rotate(-4deg)" }}>
        {lines.map((l, i) => {
          const at = (l.at ?? i * 0.5) * fps;
          const k = interpolate(frame, [at, at + 4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return <div key={i} style={{ opacity: k, transform: `translateY(${(1 - k) * 10}px)`, fontFamily: "'Caveat'", fontWeight: (l.size ?? 1) > 1.4 ? 700 : 500, fontSize: 70 * (l.size ?? 1), lineHeight: 0.95, color: dark ? "#F3EEE3" : "#2B2A28" }}>{l.text}</div>;
        })}
      </div>
      <Texture />
    </AbsoluteFill></Out>
  );
};

/** blue_quote — fondo azul con gradiente radial, comilla grande y texto (v01 1:24). */
export const BlueQuote: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const r = roles(ctx);
  const p = useEnter(0, 1.4);
  return (
    <Out dur={dur}><AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 45%, ${r.accent} 0%, ${r.accentDark} 45%, #050814 100%)`, ...safePad(ctx.style, 40), justifyContent: "center", alignItems: "center" }}>
      <div style={{ ...popStyle(p, ctx.style), display: "flex", gap: 18, alignItems: "flex-start", maxWidth: 760 }}>
        <span style={{ fontFamily: `'${ctx.style.fonts.special.family}'`, fontSize: 140, lineHeight: 0.8, color: "#fff" }}>“</span>
        {String(props.text).split(/\s+/).length <= 4
          ? <span style={{ fontFamily: `'${ctx.style.fonts.special.family}'`, fontStyle: "italic", fontWeight: 700, fontSize: 110, letterSpacing: "-0.03em", color: "#fff", lineHeight: 1, paddingTop: 30 }}>{props.text}</span>
          : <span style={{ fontFamily: `'${ctx.style.fonts.sans.family}'`, fontSize: 46, color: "#fff", lineHeight: 1.2, paddingTop: 20 }}>{props.text}</span>}
      </div>
    </AbsoluteFill></Out>
  );
};

export const DOC_REGISTRY: Record<string, React.FC<any>> = {
  name_card: NameCard, paper_collage: PaperCollage, timeline: Timeline, archival_photo: ArchivalPhoto,
  video_card: VideoCard, split_layout: SplitLayout, kinetic_type: KineticType, blue_quote: BlueQuote,
};
