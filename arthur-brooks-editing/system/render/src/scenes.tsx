// Catálogo de escenas (ver schemas/scenes.json). Cada componente recibe props del plan + duración.
import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { Backdrop, CinematicText, Glass, inkOn, popStyle, roles, safePad, stagger, useEnter, useExit, useStyle, BrandGrade } from "./kit";

type P = { props: any; dur: number; project: string; video: string; start: number };
const src = (project: string, p?: string) => (!p ? undefined : p.startsWith("http") ? p : staticFile(`${project}/${p}`));
const isVideo = (p?: string) => !!p && /\.(mp4|mov|webm|m4v)$/i.test(p);

const Media: React.FC<{ project: string; path?: string; style?: React.CSSProperties }> = ({ project, path, style }) => {
  if (!path) return null;
  const s = { width: "100%", height: "100%", objectFit: "cover" as const, ...style };
  return <BrandGrade>{isVideo(path) ? <OffthreadVideo muted src={src(project, path)!} style={s} /> : <Img src={src(project, path)!} style={s} />}</BrandGrade>;
};

const Exit: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const o = useExit(dur);
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

// ── fullscreen_text ──────────────────────────────────────────
export const FullscreenText: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const r = roles(ctx);
  const ink = inkOn(r.primary) ? r.secondary : "#ffffff";
  return (
    <Exit dur={dur}><Backdrop>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", ...safePad(ctx.style, 20) }}>
        <CinematicText maxWidth={760} text={props.text} special={props.special} size={ctx.style.captions.base_size * 1.15} ink={ink} specialInk={r.accent} />
      </AbsoluteFill>
    </Backdrop></Exit>
  );
};

// ── quote ────────────────────────────────────────────────────
export const Quote: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const r = roles(ctx);
  const ink = inkOn(r.primary) ? r.secondary : "#ffffff";
  const p = useEnter(0, 1.6);
  const mark = (ch: string, pos: React.CSSProperties) => (
    <div style={{ position: "absolute", ...pos, fontFamily: `'${ctx.style.fonts.special.family}'`, fontSize: 260, color: r.accent, opacity: p * 0.9, lineHeight: 1 }}>{ch}</div>
  );
  return (
    <Exit dur={dur}><Backdrop>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", ...safePad(ctx.style, 30) }}>
        <div style={{ position: "relative", padding: "120px 20px", maxWidth: 740 }}>
          {mark("“", { top: -20, left: 0 })}
          <CinematicText text={props.text} special={props.special} size={ctx.style.captions.base_size * 1.05} ink={ink} specialInk={r.accent} delay={4} />
          {mark("”", { bottom: -120, right: 0 })}
        </div>
        {props.author ? <div style={{ ...popStyle(useEnter(14), ctx.style), marginTop: 40, fontFamily: `'${ctx.style.fonts.sans.family}'`, fontSize: 34, letterSpacing: "0.12em", textTransform: "uppercase", color: ink, opacity: 0.6 }}>— {props.author}</div> : null}
      </AbsoluteFill>
    </Backdrop></Exit>
  );
};

// ── listicle (rombos con número) ─────────────────────────────
export const Listicle: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const { fps } = useVideoConfig();
  const r = roles(ctx);
  const items: string[] = props.items ?? [];
  return (
    <Exit dur={dur}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", top: 250 }}>
        {props.title ? <div style={{ ...popStyle(useEnter(0), ctx.style), fontFamily: `'${ctx.style.fonts.special.family}'`, fontStyle: ctx.style.fonts.special.style, fontSize: 84, color: "#fff", marginBottom: 50, textShadow: "0 6px 30px rgba(0,0,0,.45)" }}>{props.title}</div> : null}
        <div style={{ display: "flex", gap: 34, maxWidth: 760, justifyContent: "center" }}>
          {items.map((it, i) => {
            const p = useEnter(4 + stagger(i, fps, ctx.style) * 2);
            const on = props.active === -1 || props.active === undefined || props.active === i;
            return (
              <div key={i} style={{ ...popStyle(p, ctx.style, "pop_blur_fade"), display: "flex", flexDirection: "column", alignItems: "center", gap: 26, opacity: p * (on ? 1 : 0.35) }}>
                <div style={{ width: 150, height: 150, transform: "rotate(45deg)", borderRadius: 26, background: `linear-gradient(135deg, ${r.accent}, ${r.accentDark})`, border: "3px solid rgba(255,255,255,.65)", display: "flex", alignItems: "center", justifyContent: "center", boxShadow: `0 20px 60px ${r.accent}66` }}>
                  <div style={{ transform: "rotate(-45deg)", fontFamily: `'${ctx.style.fonts.sans_bold.family}'`, fontWeight: 800, fontSize: 70, color: "#fff" }}>{i + 1}</div>
                </div>
                <div style={{ fontFamily: `'${ctx.style.fonts.sans.family}'`, fontWeight: 600, fontSize: 36, color: "#fff", maxWidth: 260, textAlign: "center", textShadow: "0 4px 20px rgba(0,0,0,.6)" }}>{it}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </Exit>
  );
};

// ── notification (UI pop) ────────────────────────────────────
export const Notification: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const p = useEnter(0);
  const r = roles(ctx);
  return (
    <Exit dur={dur}>
      <AbsoluteFill style={{ alignItems: "center", ...safePad(ctx.style, 10) }}>
        <div style={{ transform: `translateY(${(1 - p) * -160}px)`, opacity: p, filter: `blur(${(1 - p) * 10}px)` }}>
          <Glass style={{ width: 740, padding: "30px 32px", display: "flex", gap: 30, alignItems: "center", background: "rgba(250,250,252,0.82)" }}>
            <div style={{ width: 110, height: 110, borderRadius: 28, background: r.accent, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 60, flexShrink: 0 }}>{props.icon ?? "🔔"}</div>
            <div style={{ fontFamily: `'${ctx.style.fonts.sans.family}'`, color: "#111", flex: 1 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 30, opacity: 0.55, fontWeight: 500 }}><span>{props.app}</span><span>ahora</span></div>
              <div style={{ fontSize: 42, fontWeight: 800, marginTop: 4 }}>{props.title}</div>
              <div style={{ fontSize: 36, fontWeight: 400, marginTop: 2 }}>{props.body}</div>
            </div>
          </Glass>
        </div>
      </AbsoluteFill>
    </Exit>
  );
};

// ── counter_ring ─────────────────────────────────────────────
export const CounterRing: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const r = roles(ctx);
  const p = useEnter(0);
  const k = interpolate(frame, [4, Math.min(dur - 6, 4 + fps * 1.4)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.2, 0.8, 0.2, 1) });
  const val = props.from + (props.to - props.from) * k;
  const max = props.max ?? Math.max(props.to, 100);
  const R = 200, C = 2 * Math.PI * R;
  return (
    <Exit dur={dur}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", top: 300 }}>
        <div style={{ ...popStyle(p, ctx.style, "pop_blur_fade"), position: "relative", width: 520, height: 520 }}>
          <Glass style={{ position: "absolute", inset: 0, borderRadius: 999 }}><span /></Glass>
          <svg width={520} height={520} style={{ position: "absolute", inset: 0, transform: "rotate(-90deg)" }}>
            <circle cx={260} cy={260} r={R} fill="none" stroke="rgba(255,255,255,.18)" strokeWidth={26} />
            <circle cx={260} cy={260} r={R} fill="none" stroke={r.accent} strokeWidth={26} strokeLinecap="round" strokeDasharray={C} strokeDashoffset={C * (1 - Math.min(1, val / max))} />
          </svg>
          <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", fontFamily: `'${ctx.style.fonts.sans_bold.family}'`, color: "#fff" }}>
            <div style={{ fontSize: 150, fontWeight: 800, letterSpacing: "-0.04em" }}>{Math.round(val)}{props.suffix ?? ""}</div>
            {props.label ? <div style={{ fontSize: 38, fontWeight: 500, opacity: 0.8, marginTop: -6 }}>{props.label}</div> : null}
          </AbsoluteFill>
        </div>
      </AbsoluteFill>
    </Exit>
  );
};

// ── before_after (balance horizontal + flecha) ───────────────
export const BeforeAfter: React.FC<P> = ({ props, dur, project }) => {
  const ctx = useStyle();
  const r = roles(ctx);
  const ink = inkOn(r.primary) ? r.secondary : "#fff";
  const card = (side: any, i: number) => {
    const p = useEnter(i * 6);
    return (
      <div style={{ ...popStyle(p, ctx.style, "pop_blur_fade"), display: "flex", flexDirection: "column", alignItems: "center", gap: 28 }}>
        <div style={{ width: 330, height: 460, borderRadius: ctx.style.shapes.radius, overflow: "hidden", background: i ? r.accent : r.secondary, border: `4px solid ${i ? r.accent : "rgba(0,0,0,.15)"}`, filter: i ? "none" : "saturate(0.2)" }}>
          <Media project={project} path={side.image} />
        </div>
        <div style={{ fontFamily: `'${i ? ctx.style.fonts.special.family : ctx.style.fonts.sans.family}'`, fontStyle: i ? ctx.style.fonts.special.style : "normal", fontWeight: i ? 600 : 500, fontSize: i ? 64 : 48, color: i ? r.accent : ink }}>{side.label}</div>
      </div>
    );
  };
  const pa = useEnter(10);
  return (
    <Exit dur={dur}><Backdrop>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "row", gap: 40 }}>
        {card(props.left, 0)}
        <svg width={120} height={60} style={{ opacity: pa, marginBottom: 90 }}><path d={`M5 30 H${5 + 100 * pa}`} stroke={ink} strokeWidth={6} strokeLinecap="round" /><path d="M85 12 L110 30 L85 48" fill="none" stroke={ink} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" opacity={pa > 0.9 ? 1 : 0} /></svg>
        {card(props.right, 1)}
      </AbsoluteFill>
    </Backdrop></Exit>
  );
};

// ── two_object (speaker abajo + texto arriba, balance vertical) ──
export const TwoObject: React.FC<P> = ({ props, dur, project, video, start }) => {
  const ctx = useStyle();
  const r = roles(ctx);
  const p = useEnter(0, 1.3);
  const ink = inkOn(r.primary) ? r.secondary : "#fff";
  return (
    <Exit dur={dur}><Backdrop>
      <AbsoluteFill style={{ height: "50%", justifyContent: "center", alignItems: "center", padding: 80 }}>
        <CinematicText text={props.text} special={props.special} ink={ink} specialInk={r.accent} size={ctx.style.captions.base_size * 1.1} />
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 70, right: 70, bottom: 110, height: "44%", borderRadius: ctx.style.shapes.radius, overflow: "hidden", transform: `translateY(${(1 - p) * 140}px)`, opacity: p, boxShadow: "0 40px 90px rgba(0,0,0,.35)" }}>
        {props.image ? <Media project={project} path={props.image} /> : <OffthreadVideo muted src={staticFile(video)} startFrom={Math.round(start * 30)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />}
      </div>
    </Backdrop></Exit>
  );
};

// ── list_card ────────────────────────────────────────────────
export const ListCard: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const { fps } = useVideoConfig();
  const r = roles(ctx);
  const p = useEnter(0);
  return (
    <Exit dur={dur}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", top: 260 }}>
        <div style={popStyle(p, ctx.style, "pop_blur_fade")}>
          <Glass style={{ width: 740, padding: "40px 46px" }}>
            <div style={{ fontFamily: `'${ctx.style.fonts.special.family}'`, fontStyle: ctx.style.fonts.special.style, fontSize: 64, color: "#fff", marginBottom: 20 }}>{props.title}</div>
            {(props.items ?? []).map((it: string, i: number) => {
              const q = useEnter(8 + stagger(i, fps, ctx.style) * 3);
              return (
                <div key={i} style={{ ...popStyle(q, ctx.style, "pop_blur_fade"), display: "flex", alignItems: "center", gap: 22, padding: "16px 0", borderTop: i ? "1px solid rgba(255,255,255,.14)" : "none", fontFamily: `'${ctx.style.fonts.sans.family}'`, fontSize: 42, color: "#fff" }}>
                  <span style={{ width: 18, height: 18, borderRadius: 99, background: r.accent, flexShrink: 0 }} />{it}
                </div>
              );
            })}
          </Glass>
        </div>
      </AbsoluteFill>
    </Exit>
  );
};

// ── bar_graph ────────────────────────────────────────────────
export const BarGraph: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const r = roles(ctx);
  const dark = !inkOn(r.primary);
  const ink = dark ? "#fff" : r.secondary;
  const bars: any[] = props.bars ?? [];
  return (
    <Exit dur={dur}><Backdrop grid>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 50, ...safePad(ctx.style, 20) }}>
        {props.title ? <CinematicText text={props.title} ink={ink} size={52} /> : null}
        <div style={{ display: "flex", alignItems: "flex-end", gap: 60, height: 760 }}>
          {bars.map((b, i) => {
            const k = interpolate(frame, [6 + i * 8, 6 + i * 8 + fps * 1.1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.2, 0.9, 0.1, 1) });
            const hi = i === bars.reduce((m, x, j) => (x.value > bars[m].value ? j : m), 0);
            return (
              <div key={i} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 22 }}>
                <div style={{ fontFamily: `'${ctx.style.fonts.sans_bold.family}'`, fontWeight: 800, fontSize: 56, color: hi ? r.accent : ink, opacity: k }}>{Math.round(b.value * k)}</div>
                <div style={{ width: 200, height: 560 * (b.value / 100) * k, borderRadius: `${ctx.style.shapes.radius}px ${ctx.style.shapes.radius}px 6px 6px`, background: hi ? `linear-gradient(${r.accent}, ${r.accentDark})` : dark ? "rgba(255,255,255,.22)" : "rgba(0,0,0,.14)", boxShadow: hi ? `0 0 60px ${r.accent}55` : "none" }} />
                <div style={{ fontFamily: `'${ctx.style.fonts.sans.family}'`, fontSize: 40, color: ink, fontWeight: 500 }}>{b.label}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </Backdrop></Exit>
  );
};

// ── line_graph (bola de acento que sigue la línea, cámara la sigue) ──
export const LineGraph: React.FC<P> = ({ props, dur, start }) => {
  const ctx = useStyle();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const r = roles(ctx);
  const pts: number[] = props.points ?? [10, 30, 50, 70, 90];
  const W = 2200, H = 1100, n = pts.length;
  const xy = pts.map((v, i) => [80 + (i / Math.max(1, n - 1)) * (W - 160), H - 80 - (v / 100) * (H - 160)]);
  let path = `M${xy[0][0]} ${xy[0][1]}`;
  for (let i = 1; i < n; i++) path += props.steps ? ` H${xy[i][0]} V${xy[i][1]}` : ` L${xy[i][0]} ${xy[i][1]}`;
  // progreso: sincronizado a palabras si hay sync_words, si no lineal
  let k: number;
  if (props.sync_words?.length) {
    const t = start + frame / fps;
    const idx = props.sync_words.filter((s: number) => s <= t).length;
    k = Math.min(1, idx / Math.max(1, n - 1));
  } else k = interpolate(frame, [6, dur - 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const segI = Math.min(n - 2, Math.floor(k * (n - 1)));
  const f = k * (n - 1) - segI;
  const a = xy[segI], b = xy[Math.min(n - 1, segI + 1)];
  const ball = props.steps ? (f < 0.5 ? [a[0] + (b[0] - a[0]) * f * 2, a[1]] : [b[0], a[1] + (b[1] - a[1]) * (f - 0.5) * 2]) : [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f];
  const camX = 540 - ball[0], camY = 960 - ball[1] - 100;
  const dark = !inkOn(r.primary);
  return (
    <Exit dur={dur}><Backdrop bg={dark ? r.primary : r.secondary} grid>
      <div style={{ position: "absolute", left: 0, top: 0, transform: `translate(${camX}px, ${camY}px)` }}>
        <svg width={W} height={H} style={{ overflow: "visible" }}>
          {Array.from({ length: 12 }).map((_, i) => <line key={i} x1={0} x2={W} y1={(i * H) / 11} y2={(i * H) / 11} stroke="rgba(255,255,255,.12)" strokeWidth={2} />)}
          <path d={path} fill="none" stroke="rgba(255,255,255,.18)" strokeWidth={8} />
          <path d={path} fill="none" stroke={r.accent} strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - k} style={{ filter: `drop-shadow(0 0 14px ${r.accent})` }} />
          <circle cx={ball[0]} cy={ball[1]} r={30} fill={r.accent} style={{ filter: `drop-shadow(0 0 26px ${r.accent})` }} />
        </svg>
      </div>
      {props.label ? <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 260 }}><CinematicText text={props.label} special={props.special} ink="#fff" specialInk={r.accent} size={54} /></AbsoluteFill> : null}
    </Backdrop></Exit>
  );
};

// ── broll_text / painting (media + viñeta + textura + texto) ──
export const BrollText: React.FC<P & { painting?: boolean }> = ({ props, dur, project, painting }) => {
  const ctx = useStyle();
  const frame = useCurrentFrame();
  const r = roles(ctx);
  const slide = painting ? interpolate(frame, [0, 24], [220, 0], { extrapolateRight: "clamp", easing: Easing.bezier(0.16, 1, 0.3, 1) }) : 0;
  const zoom = interpolate(frame, [0, dur], [1.04, 1.12]);
  return (
    <Exit dur={dur}>
      <AbsoluteFill style={{ backgroundColor: "#000" }}>
        <AbsoluteFill style={{ transform: `translateX(${slide}px) scale(${zoom})`, filter: painting ? "contrast(1.05) saturate(0.85)" : "saturate(0.9)" }}>
          <Media project={project} path={props.media} />
        </AbsoluteFill>
        <AbsoluteFill style={{ boxShadow: "inset 0 0 260px 120px rgba(0,0,0,.85)", backdropFilter: "blur(0px)" }} />
        <AbsoluteFill style={{ background: "linear-gradient(transparent 28%, rgba(0,0,0,.6) 55%, rgba(0,0,0,.88))" }} />
        <TextureOverlay />
        <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", ...safePad(ctx.style, 40) }}>
          <CinematicText text={props.text ?? ""} special={props.special} ink="#fff" specialInk={r.accent === "#ffffff" ? "#fff" : "#fff"} delay={6} />
        </AbsoluteFill>
      </AbsoluteFill>
    </Exit>
  );
};
const TextureOverlay: React.FC = () => {
  const { style } = useStyle();
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='500' height='500'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='3'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='0.55'/></svg>`;
  return <AbsoluteFill style={{ opacity: Math.max(0.12, style.texture?.opacity ?? 0), mixBlendMode: "overlay", backgroundImage: `url("data:image/svg+xml;utf8,${svg}")` }} />;
};

// ── line_text (línea que se dibuja y es interrumpida por conceptos) ──
export const LineText: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const frame = useCurrentFrame();
  const r = roles(ctx);
  const ink = inkOn(r.primary) ? r.secondary : "#fff";
  const words: string[] = props.words ?? [];
  const n = words.length;
  const step = 1400;
  const k = interpolate(frame, [4, dur - 8], [0, n - 0.4], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const camY = 960 - (200 + k * step * 0.5);
  return (
    <Exit dur={dur}><Backdrop>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, transform: `translateY(${camY}px)` }}>
        {words.map((w, i) => {
          const y = 200 + i * step * 0.5;
          const lineK = Math.max(0, Math.min(1, k - i + 0.6));
          const textOn = Math.max(0, Math.min(1, (k - i + 0.2) * 3));
          return (
            <div key={i} style={{ position: "absolute", left: 0, right: 0, top: y, display: "flex", flexDirection: "column", alignItems: "center" }}>
              <div style={{ width: 6, height: 520 * lineK, background: r.accent, borderRadius: 3, marginTop: -560 }} />
              <div style={{ opacity: textOn, filter: `blur(${(1 - textOn) * 14}px)`, fontFamily: `'${ctx.style.fonts.special.family}'`, fontStyle: ctx.style.fonts.special.style, fontSize: 120, color: i === n - 1 ? r.accent : ink, padding: "30px 0" }}>{w}</div>
            </div>
          );
        })}
      </div>
    </Backdrop></Exit>
  );
};

// ── center_illustration ──────────────────────────────────────
export const CenterIllustration: React.FC<P> = ({ props, dur, project }) => {
  const ctx = useStyle();
  const frame = useCurrentFrame();
  const r = roles(ctx);
  const ink = inkOn(r.primary) ? r.secondary : "#fff";
  const p = useEnter(0, 1.5);
  const rot = frame * 0.4;
  const spiral = () => {
    let d = "M 0 0";
    for (let t = 0; t < 6 * Math.PI * Math.min(1, frame / 40); t += 0.1) d += ` L ${Math.cos(t) * t * 16} ${Math.sin(t) * t * 16}`;
    return <svg width={700} height={700} viewBox="-350 -350 700 700" style={{ transform: `rotate(${rot}deg)` }}><path d={d} fill="none" stroke={r.accent} strokeWidth={8} strokeLinecap="round" /></svg>;
  };
  return (
    <Exit dur={dur}><Backdrop>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div style={{ opacity: p, transform: `scale(${0.9 + 0.1 * p})`, width: 760, height: 760, display: "flex", alignItems: "center", justifyContent: "center", borderRadius: props.shape === "circle" ? 999 : 0, overflow: "hidden" }}>
          {props.media ? <Media project={project} path={props.media} style={{ objectFit: "contain", filter: "grayscale(1) contrast(1.2)", mixBlendMode: "multiply" }} /> : props.shape === "spiral" ? spiral() : <div style={{ width: 600, height: 600, borderRadius: 999, border: `6px solid ${r.accent}` }} />}
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", ...safePad(ctx.style, 20) }}>
        <CinematicText text={props.text ?? ""} special={props.special} ink={ink} specialInk={r.accent} delay={8} />
      </AbsoluteFill>
    </Backdrop></Exit>
  );
};

// ── object_callout ───────────────────────────────────────────
export const ObjectCallout: React.FC<P> = ({ props, dur, project }) => {
  const ctx = useStyle();
  const r = roles(ctx);
  const ink = inkOn(r.primary) ? r.secondary : "#fff";
  const p = useEnter(0, 1.2);
  const q = useEnter(10);
  return (
    <Exit dur={dur}><Backdrop>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 50 }}>
        <div style={{ ...popStyle(p, ctx.style, "pop_blur_fade"), width: 640, height: 780, overflow: "hidden", borderRadius: ctx.style.shapes.radius, border: `5px solid ${r.accent}`, boxShadow: `0 30px 80px rgba(0,0,0,.3)` }}>
          <Media project={project} path={props.media} />
        </div>
        <div style={{ ...popStyle(q, ctx.style), display: "flex", flexDirection: "column", alignItems: "center" }}>
          <div style={{ fontFamily: `'${ctx.style.fonts.special.family}'`, fontStyle: ctx.style.fonts.special.style, fontSize: 84, color: r.accent }}>{props.label}</div>
          {props.text ? <div style={{ fontFamily: `'${ctx.style.fonts.sans.family}'`, fontSize: 42, color: ink, marginTop: 8 }}>{props.text}</div> : null}
        </div>
      </AbsoluteFill>
    </Backdrop></Exit>
  );
};

// ── lower_third ──────────────────────────────────────────────
export const LowerThird: React.FC<P> = ({ props, dur }) => {
  const ctx = useStyle();
  const r = roles(ctx);
  const p = useEnter(0);
  return (
    <Exit dur={dur}>
      <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "flex-start", paddingTop: 1150, paddingLeft: 90 }}>
        <div style={{ display: "flex", alignItems: "stretch", gap: 20, opacity: p, transform: `translateX(${(1 - p) * -60}px)` }}>
          <div style={{ width: 8, background: r.accent, borderRadius: 4 }} />
          <div style={{ fontFamily: `'${ctx.style.fonts.sans.family}'`, color: "#fff", textShadow: "0 4px 20px rgba(0,0,0,.6)" }}>
            <div style={{ fontSize: 52, fontWeight: 800 }}>{props.name}</div>
            <div style={{ fontSize: 34, fontWeight: 400, opacity: 0.85 }}>{props.role}</div>
          </div>
        </div>
      </AbsoluteFill>
    </Exit>
  );
};

export const REGISTRY: Record<string, React.FC<any>> = {
  fullscreen_text: FullscreenText, quote: Quote, listicle: Listicle, notification: Notification,
  counter_ring: CounterRing, before_after: BeforeAfter, two_object: TwoObject, list_card: ListCard,
  bar_graph: BarGraph, line_graph: LineGraph, broll_text: BrollText,
  painting: (p: any) => <BrollText {...p} painting />, line_text: LineText,
  center_illustration: CenterIllustration, object_callout: ObjectCallout, lower_third: LowerThird,
};
