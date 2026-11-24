import React from "react";
import { Composition } from "remotion";
import { Edit } from "./Edit";

export const Root: React.FC = () => (
  <Composition
    id="Edit"
    component={Edit as any}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={300}
    defaultProps={{ project: "", video: "", duration: 10, style: null, palette: {}, plan: { scenes: [] }, captions: [] } as any}
    calculateMetadata={({ props }: any) => ({
      durationInFrames: Math.max(1, Math.round(props.duration * (props.style?.format?.fps ?? 30))),
      fps: props.style?.format?.fps ?? 30,
      width: props.style?.format?.width ?? 1080,
      height: props.style?.format?.height ?? 1920,
    })}
  />
);
