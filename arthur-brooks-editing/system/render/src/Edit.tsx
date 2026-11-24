// Composición principal: A-roll base (con punch-ins) + escenas (base/fullscreen/overlay) + captions por modo de estilo.
import React from "react";
import { AbsoluteFill, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { StyleCtx, useStyle } from "./kit";
import { REGISTRY as BASE_REG } from "./scenes";
import { DOC_REGISTRY } from "./scenes_doc";
import { ARTHUR_REGISTRY } from "./scenes_arthur";
import { JOSEPH_REGISTRY } from "./scenes_joseph";
import { Caption } from "./captions";
import { Transition, TRANSITION_FRAMES } from "./transitions";

/** entrada de escena: crossfade / slide (v01, v10) — envuelve la escena */
const Shell: React.FC<{ kind?: string; children: React.ReactNode }> = ({ kind, children }) => {
  const fr = useCurrentFrame();
  if (kind === "crossfade") return <AbsoluteFill style={{ opacity: interpolate(fr, [0, 8], [0, 1], { extrapolateRight: "clamp" }) }}>{children}</AbsoluteFill>;
  if (kind === "slide") return <AbsoluteFill style={{ transform: `translateX(${interpolate(fr, [0, 9], [100, 0], { extrapolateRight: "clamp", easing: (t) => 1 - Math.pow(1 - t, 3) })}%)` }}>{children}</AbsoluteFill>;
  if (kind === "slide_up") return <AbsoluteFill style={{ transform: `translateY(${interpolate(fr, [0, 9], [100, 0], { extrapolateRight: "clamp", easing: (t) => 1 - Math.pow(1 - t, 3) })}%)` }}>{children}</AbsoluteFill>;
  return <>{children}</>;
};

export type EditProps = { project: string; video: string; duration: number; style: any; palette: any; plan: any; captions: any[] };
const REGISTRY: Record<string, React.FC<any>> = { ...BASE_REG, ...DOC_REGISTRY, ...ARTHUR_REGISTRY, ...JOSEPH_REGISTRY };

const LAYER: Record<string, string> = {
  aroll: "none", split_layout: "base",
  fullscreen_text: "fullscreen", quote: "fullscreen", before_after: "fullscreen", two_object: "fullscreen", bar_graph: "fullscreen",
  line_graph: "fullscreen", broll_text: "fullscreen", painting: "fullscreen", line_text: "fullscreen", center_illustration: "fullscreen",
  object_callout: "fullscreen", name_card: "fullscreen", paper_collage: "fullscreen", archival_photo: "fullscreen", video_card: "fullscreen",
  kinetic_type: "fullscreen", blue_quote: "fullscreen", timeline: "fullscreen",
  arthur_text: "fullscreen", arthur_icons: "fullscreen", arthur_orbit: "fullscreen", arthur_stripes: "fullscreen", arthur_blocks: "fullscreen", arthur_broll: "fullscreen", arthur_number: "top", j_graph: "fullscreen", j_line: "fullscreen", j_quote: "fullscreen", j_illus: "fullscreen", j_half: "fullscreen", j_painting: "fullscreen", j_broll: "fullscreen",
  listicle: "overlay", notification: "overlay", counter_ring: "overlay", list_card: "overlay", lower_third: "overlay",
};
export const layerOf = (s: any) => (s.type === "timeline" && s.props?.over_aroll ? "overlay" : LAYER[s.type] ?? "fullscreen");
// escenas fullscreen que DEJAN ver captions (en la referencia, el b-roll/archivo lleva caption encima)
const CAPTION_OVER = new Set(["broll_text_caption", "archival_photo", "video_card"]);

const ARoll: React.FC<{ video: string; scenes: any[]; captions: any[] }> = ({ video, scenes, captions }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { style } = useStyle();
  const t = frame / fps;
  const a = scenes.find((s) => s.type === "aroll" && t >= s.start && t < s.end);
  let z = 1;
  if (a?.props?.zoom) z = a.props.zoom; // punch-in de Arthur: corte seco al encuadre cerrado, sin zoom lento
  else if (style.aroll?.auto_punch) {
    // punch-in por oración (corte seco, sin easing) — v01: plano medio ↔ primer plano
    const ph = captions.find((p) => t >= p.start && t < p.end) ?? [...captions].reverse().find((p) => p.start <= t);
    z = ph && ph.sentence % 2 === 1 ? style.aroll.punch_zoom ?? 1.3 : 1;
  }
  const oy = style.aroll?.punch_origin_y ?? 0.3;
  return (
    <AbsoluteFill>
      <OffthreadVideo src={staticFile(video)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${z})`, transformOrigin: `50% ${oy * 100}%`, filter: a?.props?.desaturate ? "saturate(0.15)" : style.aroll?.grade ?? "none" }} />
      {style.aroll?.vignette ? <AbsoluteFill style={{ boxShadow: `inset 0 0 300px 80px rgba(0,0,0,${style.aroll.vignette})` }} /> : null}
    </AbsoluteFill>
  );
};

const CaptionBackdrop: React.FC = () => {
  const { style } = useStyle();
  const b = style.captions.backdrop;
  if (!b || b.type === "none") return null;
  const cy = style.captions.center_y ?? 0.6;
  if (b.type === "blur_dark")
    return <AbsoluteFill style={{ top: `${(cy - 0.12) * 100}%`, bottom: `${(style.safe_zone?.bottom ?? 0.2) * 60}%`, backdropFilter: `blur(${b.blur}px)`, background: `rgba(0,0,0,${b.darkness})`, maskImage: "linear-gradient(transparent, black 30%)", WebkitMaskImage: "linear-gradient(transparent, black 30%)" }} />;
  return <AbsoluteFill style={{ top: `${(cy - 0.15) * 100}%`, background: `linear-gradient(transparent, rgba(0,0,0,${b.darkness}))` }} />;
};

export const Edit: React.FC<EditProps> = ({ video, style, palette, plan, captions, project }) => {
  const { fps } = useVideoConfig();
  const scenes: any[] = plan.scenes ?? [];
  const f = (s: number) => Math.round(s * fps);
  const fullscreen = scenes.filter((s) => layerOf(s) === "fullscreen");
  // overlays que ocupan la zona media-baja: el caption se oculta mientras están (no se pisan, la cara queda libre)
  const LOW = new Set(["counter_ring", "listicle", "list_card", "arthur_number"]);
  const lowOv = scenes.filter((s) => LOW.has(s.type) || (s.type === "timeline" && s.props?.over_aroll));
  const hiddenDuring = (ph: any) => lowOv.some((s) => ph.start < s.end - 0.05 && ph.end > s.start + 0.05) || fullscreen.some((s) => !CAPTION_OVER.has(s.type) && !s.props?.captions_on && ph.start < s.end - 0.05 && ph.end > s.start + 0.05);
  const capsOn = plan.captions?.enabled !== false;
  // sincronía: la frase aparece CAPTION_LEAD frames antes de la primera palabra (un pelín adelantada, nunca tarde) y se
  // queda hasta que empieza la siguiente; si la tapa una escena a pantalla completa, se muestra solo el tramo libre.
  const LEAD = 2;
  const blockers = [...lowOv, ...fullscreen.filter((s) => !CAPTION_OVER.has(s.type) && !s.props?.captions_on)].map((s) => [f(s.start), f(s.end)]);
  const visibleSpans = (ph: any): [number, number][] => {
    let spans: [number, number][] = [[Math.max(0, f(ph.start) - LEAD), f(ph.end) - LEAD]];
    for (const [b0, b1] of blockers) spans = spans.flatMap(([x0, x1]) => (b1 <= x0 || b0 >= x1 ? [[x0, x1]] : ([[x0, b0], [b1, x1]] as [number, number][]).filter(([p, q]) => q - p >= 6)));
    return spans.filter(([x0, x1]) => x1 - x0 >= 6);
  };
  const seq = (s: any) => {
    const C = REGISTRY[s.type];
    if (!C) return null;
    return <Sequence key={s.id} from={f(s.start)} durationInFrames={Math.max(1, f(s.end) - f(s.start))}><Shell kind={s.enter}><C props={s.props ?? {}} dur={f(s.end) - f(s.start)} project={project} video={video} start={s.start} /></Shell></Sequence>;
  };
  // transiciones sobre el corte: s.in (entrada) y s.out (salida a A-roll) — y "cuts" sueltos en el A-roll (plan.cuts)
  const trans: { t: number; type: string; k: string }[] = [];
  scenes.forEach((s) => { if (s.in) trans.push({ t: s.start, type: s.in, k: s.id + "i" }); if (s.out) trans.push({ t: s.end, type: s.out, k: s.id + "o" }); });
  (plan.cuts ?? []).forEach((c: any, i: number) => trans.push({ t: c.t, type: c.type, k: "c" + i }));
  return (
    <StyleCtx.Provider value={{ style, palette }}>
      <AbsoluteFill style={{ backgroundColor: "#000" }}>
        <ARoll video={video} scenes={scenes} captions={captions} />
        {scenes.filter((s) => layerOf(s) === "base").map(seq)}
        {capsOn ? <CaptionBackdrop /> : null}
        {scenes.filter((s) => layerOf(s) === "overlay").map(seq)}
        {fullscreen.map(seq)}
        {capsOn ? captions.flatMap((ph, i) => visibleSpans(ph).map(([a0, a1], j) => (
          <Sequence key={`c${i}_${j}`} from={a0} durationInFrames={Math.max(1, a1 - a0)}><Caption ph={ph} fromSec={a0 / fps} /></Sequence>
        ))) : null}
        {scenes.filter((s) => layerOf(s) === "top").map(seq)}
        {trans.filter((x) => TRANSITION_FRAMES[x.type]).map((x) => (
          <Sequence key={x.k} from={Math.max(0, f(x.t) - 1)} durationInFrames={TRANSITION_FRAMES[x.type]}><Transition type={x.type} /></Sequence>
        ))}
      </AbsoluteFill>
    </StyleCtx.Provider>
  );
};
