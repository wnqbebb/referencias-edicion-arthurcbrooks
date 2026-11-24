# Empieza aquí · Skill de edición Arthur Brooks

Un solo paquete. Súbelo a cualquier chat o modelo y obtienes el mismo resultado: el estilo vive en estos archivos, no en el modelo.

## Subirla a un chat nuevo (2 minutos)
| Dónde | Qué subes | Cómo |
|---|---|---|
| **Claude.ai** | este zip completo | Ajustes → Capacidades → Skills → Subir skill. Si pide algo más pequeño, sube los archivos de `knowledge/` a un Proyecto y pega las instrucciones de `MODELOS.md` |
| **Claude Code** | la carpeta descomprimida | Cópiala a `.claude/skills/arthur-brooks-editing/` de tu proyecto (o `~/.claude/skills/`). Para renderizar usa `system/` |
| **ChatGPT** | los 9 archivos de `knowledge/` + `ANIMACIONES.md` | GPT personalizado o Proyecto → Conocimiento; pega las instrucciones de `MODELOS.md` |
| **Gemini** | los mismos archivos | Gem → Conocimiento; pega las instrucciones de `MODELOS.md` |
| **Codex / Gemini CLI** | la carpeta `system/` | Ábrela y di «lee SKILL.md y AGENTS.md y síguelos» |

## Reglas generales
`REGLAS_GENERALES.md`: obligatorias en esta skill y en todas las skills de estilo.

## Herramientas
Lee `HERRAMIENTAS.md`: el MCP de Playwright (buscar en internet), las skills de Remotion y HyperFrames y el instalador `system/instalar_herramientas.sh`.

## Primer mensaje en el chat nuevo
Copia el prompt 2 de `PROMPTS.md` y adjunta tu video. El modelo te devuelve el plan por beats (A/B/C) para que elijas.

## Mismo resultado en cualquier modelo
1. Siempre el mismo flujo con 3 STOPs (plan → assets → vista previa).
2. Siempre eligiendo de la misma biblioteca (`ANIMACIONES.md`, IDs `VNN-ANN`).
3. Siempre el mismo contrato (`CONTRATO.md`) y el mismo render (`system/`).
