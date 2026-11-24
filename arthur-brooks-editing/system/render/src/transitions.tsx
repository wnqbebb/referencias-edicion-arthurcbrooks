// Transiciones medidas en los 20 videos de Arthur (references/vNN/edit_logic.json). Cada una dura pocos frames
// y se dibuja ENCIMA del corte (empieza 1–3 frames antes de la escena nueva). Firma por formato:
//  documental: crossfade, slide, match-cut, light_leak dorado (solo cambio de capítulo) · animación VO: slide, wipe, flash_white, iris
//  talking head + minimal: punch (en A-roll), glitch_blocks, wipe, invert_sandwich · podcast clip: whip, flash_tint, zoom_blur
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { roles, useStyle } from "./kit";

export const TRANSITION_FRAMES: Record<string, number> = {
  cut: 0, flash_white: 3, flash_tint: 4, light_leak: 10, whip: 6, zoom_blur: 4, glitch_blocks: 5, invert_sandwich: 3, wipe: 9, iris: 9, ink_wipe: 6,
};

export const Transition: React.FC<{ type: string }> = ({ type }) => {
  const f = useCurrentFrame();
  const ctx = useStyle(); const r = roles(ctx);
  const n = TRANSITION_FRAMES[type] ?? 0;
  switch (type) {
    case "flash_white": // v10/v19: 1–2 frames de blanco puro
      return <AbsoluteFill style={{ background: "#fff", opacity: f < 2 ? 1 : interpolate(f, [2, n], [1, 0]) }} />;
    case "flash_tint": // v17/v18: 2 frames tinte de acento + 2 de blanco (cambio de tema en podcast)
      return <AbsoluteFill style={{ background: f < 2 ? r.accent : "#fff", opacity: f < 2 ? 0.55 : 1 }} />;
    case "light_leak": // v11: destello dorado SOLO entre capítulos/hablantes
      return <AbsoluteFill style={{ background: "radial-gradient(ellipse at 70% 40%, rgba(255,214,140,.95), rgba(255,150,40,.55) 40%, transparent 75%)", mixBlendMode: "screen", opacity: interpolate(f, [0, 3, n], [0, 1, 0], { extrapolateRight: "clamp" }) }} />;
    case "whip": // v13/v17: 'smear' — desenfoque horizontal fuerte 4–6 frames
      return <AbsoluteFill style={{ backdropFilter: `blur(${interpolate(f, [0, n / 2, n], [6, 28, 0])}px)`, WebkitBackdropFilter: `blur(${interpolate(f, [0, n / 2, n], [6, 28, 0])}px)` }} />;
    case "zoom_blur": // punch-in con 1–2 frames de blur
      return <AbsoluteFill style={{ backdropFilter: `blur(${f < 2 ? 14 : 0}px)`, WebkitBackdropFilter: `blur(${f < 2 ? 14 : 0}px)` }} />;
    case "glitch_blocks": { // v08: rectángulos en negativo + bloques de color, entrada y salida simétricas
      const blocks = [[0.05, 0.18, 0.6, 0.12], [0.3, 0.42, 0.55, 0.09], [0.1, 0.63, 0.8, 0.07], [0.55, 0.27, 0.35, 0.05]];
      return <AbsoluteFill>{blocks.map(([x, y, w, h], i) => (
        <div key={i} style={{ position: "absolute", left: `${x * 100}%`, top: `${y * 100}%`, width: `${w * 100}%`, height: `${h * 100}%`,
          backdropFilter: (f + i) % 2 ? "invert(1)" : "none", WebkitBackdropFilter: (f + i) % 2 ? "invert(1)" : "none",
          background: (f + i) % 2 ? "transparent" : i === 1 ? "#F2C230" : r.accent, transform: `translateX(${((f * 37 + i * 53) % 60) - 30}px)` }} />
      ))}</AbsoluteFill>;
    }
    case "invert_sandwich": // v08: negativo 1 frame → amarillo 1 frame → escena (entrada a una cita)
      return f === 0 ? <AbsoluteFill style={{ backdropFilter: "invert(1)", WebkitBackdropFilter: "invert(1)" }} /> : f === 1 ? <AbsoluteFill style={{ background: "#F2C230" }} /> : null;
    case "wipe": // v06/v10: barrido izquierda→derecha con el color de acento
      return <AbsoluteFill style={{ background: r.accent, clipPath: `inset(0 ${interpolate(f, [0, n / 2, n], [100, 0, 0])}% 0 ${interpolate(f, [0, n / 2, n], [0, 0, 100])}%)` }} />;
    case "iris": { // v10: esquinas redondeadas → círculo (abre la escena nueva)
      const k = interpolate(f, [0, n], [0, 1], { extrapolateRight: "clamp" });
      return <AbsoluteFill style={{ boxShadow: `0 0 0 ${2000 * (1 - k)}px ${r.secondary}`, borderRadius: `${50 * (1 - k)}%`, margin: `${30 * (1 - k)}%` }} />;
    }
    case "ink_wipe": // v04: mancha de tinta que crece y cubre en 5 frames
      return <AbsoluteFill style={{ display: "flex", alignItems: "center", justifyContent: "center" }}><div style={{ width: 120 + f * 520, height: 120 + f * 520, borderRadius: "48% 52% 45% 55%", background: r.secondary, opacity: f < n - 1 ? 1 : 0.0 }} /></AbsoluteFill>;
    default:
      return null;
  }
};
