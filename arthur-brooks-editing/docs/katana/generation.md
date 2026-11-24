# Generation cookbook for reference-led footage

## Execution contract

Read `analysis/task-contract.json` (`explicit_locks`, `creative_freedoms`, `references`) and
`plan/creative-plan.json` before choosing jobs. A lock applies only to the property or interval it
names; everything else is open to the authored plan.

Preserve the intended identity, explicit locks and selected source visual grammar while
authoring a new story/visual motif, scenes, text, framing and duration. Route the authored **output shot
IDs**, using suitable existing footage first, necessary image preparation second and Seedance 2.5 for
missing new scenes. Do not make motion transfer the default for people. Genjutsu is justified by a
particular required source movement or a suitable verified preset. The recipes' source-lock language
applies only to an explicitly locked property or interval; every other scene follows its authored shot
specification.

**Mandatory complete-reference gate.** Before finalizing any generation plan or submitting any video generation, complete [reference analysis](references/analysis.md): decode the entire source on its native frame grid, inspect every native-frame sheet, and finish the per-second log covering the full timeline with no unexamined interval. Sparse keyframes, a few sampled seconds, a scene summary or an uninspected frame export do not satisfy this gate. Read the full source audio too. Any unreadable section remains explicitly unresolved; do not fill it with guessed production defaults or start dependent generation.

Keep exact observed start/end/peak frames, intensity, texture scale/direction, blend/opacity, font
geometry and cadence in `analysis/breakdown.json`. `plan/creative-plan.json` records the selected
grammar, its source evidence and authored output timing; observations are not rewritten as invented
events. Each job serves a necessary output role or explicit lock. Hidden-face identity
continuity still matters. A QA score never closes unexamined details.

**Video model lock.** New video footage, drafts, retries, extensions and newly generated motion use only `seedance_2_5` (Seedance 2.5). Never substitute another Seedance version, Kling, Veo, Wan or an aliased video engine to save time or credits. Before every cost preflight and submission, including each batch item, verify this allowlist: fresh video = `seedance_2_5`; a shot requiring particular source motion/re-performance = `hf_mult_motion_control`. Anime and stylized hero stills do not require Genjutsu presets: prefer the two-reference image route in G4 when it fits the planned shot. Genjutsu presets or Styles are optional routes only when their verified contract fits the requested change; never force a restyle or an extra paid job. Never invent or interchange a catalog preset ID, Styles model or API parameter. Image models remain available for still images and identity/keyframe preparation; Seedance 2.5 is used only for video. Post-production utilities, `sam_3_video` segmentation, `remove_background` and local masks are allowed; the model lock restricts newly generated creative scene footage, not masking or processing existing footage. Load [Genjutsu routing](references/genjutsu-routing.md) for celebrity-source edits or anime/Styles transformations before choosing that route.

**Genjutsu prompt limit.** For direct Genjutsu edits and optional Genjutsu presets, write one short sentence, at most two and at most 40 words. State only the operation and a small preservation rule; the supplied media carries identity, appearance, style, scene and choreography. Do not re-describe demographics, wardrobe, camera, effects or every object unless a minimal target distinction is required. A preset may use an empty prompt when its verified contract permits it and selected preset + inputs already specify the result. This limit does not apply to the two-reference image-edit prompt or detailed Seedance 2.5 timing instructions.

**Celebrity and anime references.** A celebrity appearing in supplied source footage is not a categorical reason to refuse or replace the person with a generic lookalike. Reuse authorized source footage where it serves an output role, and use a supported Genjutsu route (motion transfer or a verified preset) only where the shot needs it. For an anime/stylized hero still, combine the reference frame with the uploaded user identity in an image model (G4); the frame supplies composition, pose and camera, and style/identity ownership is assigned explicitly. Use the resulting still with code, or Seedance 2.5 only where new motion is required; direct Genjutsu motion transfer is appropriate when specific driving choreography requires it. A Genjutsu preset is optional, and an anime reference alone never authorizes a forced restyle. Do not describe generated celebrity scenes as genuine archival footage. Never disguise identity, remove evidence or switch routes to defeat an actual content refusal; unsupported changes remain a declarative limitation with no question.

Explicit locks and the authored shot plan own props, composition, text, logos, audio, frame grid and
effects. The user's own image(s) own the hero's identity and clothing: the hero wears the
outfit from the user's photo in every scene unless the user explicitly asks for different clothing.
Never put the reference performer's outfit on the hero and never invent a new one; the portrait's
lighting and background are not imported automatically. Keep the user's intended hero across every
output appearance, including hidden faces. Full regeneration covers every required output shot;
automatic KEEP cannot reduce that scope. Reuse actual suitable source pixels/audio where the contract permits.

**Never change a face in code.** Do not use Python, OpenCV, Pillow, Canvas, ffmpeg filters, mesh/landmark
warps or local pixel editing to replace a face, blend identities, repaint or paste facial parts, change
expression/eyes/mouth/nose/jaw, retouch skin, beautify, or apply face-only color/lighting corrections.
Required identity or facial changes and generated-face defects use a verified authorized image-editing
model, the appropriate Genjutsu transformation, or Seedance 2.5 for new footage, within the existing
attempt/cost limits. Missing capability or budget never authorizes a code-based face substitute.
Code may track coordinates, move/rotate/uniformly scale an entire unaltered frame or subject layer,
refine its outer matte edges, and apply whole-shot grades or separate graphic/text overlays consistent
with the selected grammar and explicit locks. These operations must not reshape or reconstruct the face beneath them; a face crop is for
inspection/reference preparation, not a patch to paste onto a different head.

Never ask intake, taste, character, voice, font, budget or approval questions, and never open a consent or selection widget. Infer production choices from the reference and choose the closest matching result internally. No waiting-for-user state is permitted. If a required asset, capability, account authorization or mandatory service consent is unavailable, do not bypass the requirement: use an already authorized suitable supported fallback or report the dependent branch as blocked or partial declaratively. Continue independent work.

Before any paid work, live-price a finite plan of required jobs, one take each, with a bounded retry reserve. Use existing task authorization under account and platform rules; a numeric user budget is optional. Apply any user cap or account spending limit, record the actual authorization, and set the internal ceiling to the required quoted plan plus bounded reserve. Continue automatically within that ceiling without confirmations or option menus. Internal ledger registration is not fabricated user approval. No purchase, top-up, subscription or discretionary experiment is implied. Unknown prices or permissions cannot authorize a paid submit: use an already authorized suitable fallback or report the blocked branch declaratively. At most three still attempts (a line's registered takes plus one documented re-roll per take; a one-take line has two) and one corrective video retry are allowed within the plan; never increase its ceiling autonomously.

Price the whole workflow under [budget.md §8.2](references/budget.md): one `get_cost` preflight per distinct settings and
one finite cap. A job waiting for a generated input keeps a `"<result of LINE>"` placeholder until it exists; no
invented IDs, guessed prices or paid pricing probes are permitted, and the cap never rises on its own.

The API examples are request shapes. Resolve the current operation and contract from available tools before any call. For image/video costing send the same prepared request to `estimate_image_cost` / `estimate_video_cost` (single call; batch items take no `get_cost`): it returns the credit cost and creates no job and no charge. Audio uses `estimate_audio_cost` the same way. A `generate_*` call submits a paid job and is never a price probe. References below to a cost preflight mean this `get_cost` call. Current contracts govern roles, batch limits and model IDs; the historical observations are not fresh verification.

This file covers _how_ to generate once `routing.md` has decided _what_ to generate. Every recipe gives
the model id, a params shape, historical price (dated per row or recipe; re-price with the `get_cost` preflight), the count policy, when
to use it, and the prompt. Where the prompt actually produced accepted or used footage, it is quoted
**VERBATIM**. Anything that has not been run is marked **UNTESTED**. Sibling docs named here
(`routing.md`, `budget.md`, `mcp-api.md`, ...) are `references/<name>.md`, read with
the available skill-resource reader or the local package path. Do not invent an unavailable bundle tool.

Status labels:

- **PROVEN**: used in a shipped or approved film, with the project named.
- **WORKED**: the output was usable, but the film it went into was not accepted, or its acceptance is
  unknown.
- **UNTESTED**: reasoned from the evidence, never run.
- **VERIFIED (live 2026-10-08)**: seen in the paid test run of this workflow on 2026-10-08 (a full
  reference edit with one Seedance plate; 111.12 cr in all, reconciled exactly with `transactions`).
- **VERIFIED (live 2026-10-13)**: seen in the paid stills test of that day (keyframe-first image
  preparation and location plates; job counts, prices and per-model outcomes in `references/stills.md` §6).

**VERBATIM prompts are someone else's project. Copy the structure, never the identity items.**

- Every VERBATIM block below belongs to a past user's hero: one hero's lime wig, micro shorts, cross
  thigh-highs, green lipstick and katana; another's striped top, bangles and mop-handle backstage; a past
  project's boxer. None of it belongs in a new user's prompt.
- Take from an example: the block order, the sentence types (identity-lock sentence, inventory, style
  line, timecoded shots, closing exclusion), the observed structure and technical lessons.
- Identity, clothing and explicit locks come from the current request and its authorized references:
  the hero wears the clothing from the user's own image(s) unless the user explicitly asks for another
  outfit. Unlocked props and scene details come from `plan/creative-plan.json`, with their reference
  grammar recorded. Never import the reference performer's outfit, a portrait's background or a
  historical example's styling.
- Leak check before every `get_cost` preflight (§5 check #10): read the prompt against the example you
  started from; any garment, prop, colour or place that came from the example and not from this user is
  a leak. Evidence: a dry-run eval copied a past hero's micro shorts, green lipstick and cross thigh-highs
  into a different user's brief.

**Every params block below is a SHAPE, not settings.**

- `model`, `mode`, `resolution`, `duration` (for Genjutsu: the driving clip's length) and `aspect_ratio`
  come from the job's line in `plan/gen_plan.json`. They are written `"<from plan line>"`, or
  `"<from plan line: seedance_2_5>"` where the recipe fixes the value and the plan line must say the
  same. Never copy a value from this cookbook or from a VERBATIM project: one past project's 1080p and 15 s were
  that project's choices, not defaults.
- The plan line gets its resolution from `budget.md` §5, measured in the **delivery frame from
  `plan/creative-plan.json.output_target`**. Select the output size for the brief before pricing.
  Test 720p coverage against all the visible detail the shot needs, including texture, lettering,
  silhouettes and props. Face readability
  and a 1.3× upscale are useful risk signals, not the sole criteria. Windowing, letterboxing or a stylized
  grade does not automatically justify lower resolution. Use the required supported resolution within
  the cap; never hide a loss of detail behind the absence of a visible face. Historical examples:
  - a past 900×720 reference delivered at its own size → 720p (the eval that measured it in a
    1440×1080 frame bought 1080p plates for +109 cr nobody would see);
  - a past 996 px window → 720p (996 ÷ 1112 < 1; windowed anyway);
  - a full-frame 1080×1920 face close-up → 1080p (1080 ÷ 720 = 1.5);
  - a past remake, 1440×1080 delivery: the 720p 4:3 plate is 1112×834 (VERIFIED live), a 1.29× upscale
    at full frame under a xerox look → 720p; it shipped that way.
- The plan line gets its duration from `budget.md` §4: plate slots, or the driving clip's seconds.
- `python3 $RR/ledger.py params $W --line <ID>` prints the exact request for a line whose inputs exist.
  Its prompt and real media IDs must already be in the plan. `--check '<params json>'` compares what
  you are about to send with the line (exit 1 = mismatch). Deferred lines are rejected, not executable
  skeletons to fill with invented upstream IDs.
- Every Seedance call carries `"generate_audio": false` and `"bitrate_mode": "high"`. High bitrate is
  free. **They are plan fields too:** every Seedance line in `plan/gen_plan.json` states
  `"generate_audio": false` and `"bitrate_mode": "high"` (and `"draft": true` only on a draft line), so
  the quote, `params` and `--check` all see them. `ledger.py quote` warns when a Seedance line lacks
  them; fix the line, do not rely on defaults (the model default is audio ON). Plan line shape:
  ```json
  {
    "id": "plate_A",
    "stage": "canary",
    "tool": "generate_video",
    "model": "seedance_2_5",
    "mode": "omni_reference",
    "resolution": "<budget.md §5>",
    "duration": "<Σ slot_s>",
    "aspect_ratio": "<output target or format lock>",
    "count": 1,
    "generate_audio": false,
    "bitrate_mode": "high",
    "identity": true,
    "location_line": "loc_street",
    "stills": {"<photo media_id>": "ref/photo.jpg"},
    "medias": [
      {"role": "image", "value": "<result of st_o04>"},
      {"role": "image", "value": "<photo media_id>"},
      {"role": "image", "value": "<result of loc_street>"}
    ],
    "prompt_file": "plan/prompts/plate_A.txt",
    "serves_cuts": ["o03", "o05"],
    "screen_seconds": 4.6
  }
  ```
  `@imageN` ownership lives in the prompt; a `refs` list is only a pre-pricing note that `ledger.py params`
  expands into `<...>` placeholders. Before `guard` the line carries real `medias`, `location_line` (a
  `soul_cinematic` or `location_plate` line; or `location: "n/a: <reason>"` for retained footage) and
  `stills` for image inputs that are not ledger jobs; the guard refuses placeholders first and a missing
  location/stills next. Image inputs resolve job-first: a value that is a ledger job resolves to its image
  line's `still` file and needs a current-hash `match` pair in `qa/styleframes.json`; a value that is not a
  ledger job may be mapped in `stills` and then only has to exist (identity/source anchors such as the user's
  photo or a reference-frame crop are not judged for medium and need no pair); a job id mapped in `stills`
  is refused (stills.md §5, budget.md §8.1).
  `serves_cuts` retains the ledger's field name but contains output shot IDs. Store observed
  source cut IDs separately in route evidence.
- Pre-submit check #9 (§5): the params equal the plan line. A mismatch is unplanned spend: stop.

MCP mechanics are in `mcp-api.md` and prices in `budget.md`. The short version:

- **Count.** Use `count: 1` for every image, video and audio request. Select results internally; never open a character or voice selection gate.
- **Attempts.** At most three attempts per still need (the line's registered takes plus one documented re-roll per take: a one-take line has two) and one corrective retry per video job, within the finite priced plan and remaining authorized spend. Stop the paid branch when either bound is reached. Reuse matching source material or report the unresolved mismatch without a question.
- **Price check.** Use the `get_cost` preflight: the prepared single `generate_image` / `generate_video` request sent to `estimate_image_cost` / `estimate_video_cost`, which creates no job and no charge (batch items take no `get_cost`). One current preflight per distinct settings (model, mode, resolution, duration or frames, quality, media roles) prices every line with those settings; prompt text and media IDs do not change it. A quote is not a generation-readiness or moderation pass. A call without `get_cost:true` is a paid submit, never a pricing probe.
- **Guarded submissions and job polling.** One ledger reservation per submit call: reserve, submit exactly that request or batch, then immediately register every returned job ID before reserving again. After a family's canary passes, its remaining independent planned jobs of one kind go out together: one `generate_image_batch` / `generate_video_batch` call of up to 12 jobs (a line repeats for its registered takes) under one `ledger.py guard` with a `--line` per job. Canaries, re-rolls and length changes stay single requests. Never run several guards and then send one batch.
  - Multiple jobs may remain pending after their individual submissions are registered. Between `jobs_wait` polls, do reference-side work: text layers, `fx.js`, the audio map and QA preparation.
  - Do not finalize the footage catalogue, in-points or EDL until every submitted paid job in the planned group is terminal and accounted for. A late job must be catalogued before rendering.
- **Logic check of every generated clip before it gets in-points.** `python3 $RR/prodcheck.py logic $W --clip gen/<clip>.mp4`
  lays out one whole frame every 0.5 s at ≥ 960 px, two per page; open every page. Check hands and finger
  count, props obeying physics (held, not glued to a lip), objects merging or popping, identity drift against
  the identity reference, stray text/logos/UI and whether the shot still plays its planned role. Record
  unusable seconds as `bad_ranges` `[[t0, t1, "reason"]]` and a `verdict` (`ok` | `partial` | `reroll`) in
  `qa/logic/<clip>.json`. Choose in-points outside the bad ranges; a clip whose needed range is broken goes to the
  bounded corrective retry. `prodcheck.py ranges` (qa-delivery #17) later fails any placement inside a bad range.
- **Refunds require verification.** `nsfw`, `ip_detected` and `failed` jobs are charged at submit and were
  refunded automatically within ~5 s–4 min on this account (VERIFIED from its records, mcp-api §13).
  These are historical observations, not a refund guarantee. Keep each debit charged against the plan
  until its refund is verified; completed unusable footage also consumes the budget.
  - Report a current refund only after verifying it in current `transactions`. If unresolved, report the debit and unknown refund status; never repeat a historical account claim as a current result.
- **Canaries** (`budget.md` §7). The canary is the planned job that covers the family's hardest fidelity constraints, submitted alone
  at the final settings, so a pass is usable footage.
  - A family is model + identity image set + set or world. A new style line or new shot content is not a
    new family.
  - Submit each family's canary through its own reservation → single request → immediate ledger registration. Each family's other jobs wait for that canary to pass; never submit a multi-item canary batch.
  - Never add a canary job that serves no cut.
- **Style frames before the first Seedance job of a family.** The stills a family depends on already exist
  (the required location plate, the identity sheet, any keyframe), so this costs no extra job: put each
  next to the reference frame(s) it serves with
  `python3 $RR/prodcheck.py styleframes $W --pair <still> ref/ref.mp4 <t> <label> ...` and look at every page.
  Judge light key, palette, medium and texture (the selected visual grammar, not the composition).
  The metric flags (luma ±15 %, saturation ±20 %, mean-Lab ΔE > 18)
  are prompts to look, not verdicts. Write `verdict` (`match` | `rewrite`) and a note per pair in
  `qa/styleframes.json`; a `rewrite` changes the still's brief and regenerates that still within its attempt
  limit before any video job that uses it. Reference grammar that only motion can show is judged on the canary. `ledger.py guard` refuses a video line whose still inputs lack a `match` pair or whose still file changed since it was judged; the image line's `still` field names the judged file ([stills.md](references/stills.md) §5).
- **Timeouts.** After a transport timeout, never resubmit until you have checked the jobs: a resubmit can
  charge twice.
- **Allowance selection.** When the live contract defines `use_unlim:false` as ordinary existing-credit
  billing, set it from already-established task/account credit authority to avoid an unnecessary picker;
  this creates no new authority. Set `use_unlim:true` or `use_free_gens:true` only from an applicable
  existing explicit allowance choice verified against live entitlements. Never start a trial or bypass
  genuinely required fresh consent; use an authorized fallback or state the limitation.
- **Media.** `medias[].value` must be a media_id or job_id, never a URL.
  - Roles: Seedance and image models take `image` (Seedance also `start_image`). `image` is the canonical
    role on plan lines and requests; the server maps it to the model's slot (observed as `adjustments` to
    `image_references` for `gpt_image_2_5` and `ideogram_4_5`; `soul_cinematic` accepted `image` unchanged;
    other models UNTESTED) and that needs no action. The ledger also
    accepts `image_references` on a plan line as `image`.
  - Genjutsu takes `image` (at least 1) plus exactly one `video`. Send these current schema keys (mcp-api §6.3).
  - Confirm roles with `models_get` once per session.
- **Generated-input dependencies.** A line that needs another line's result keeps a `"<result of LINE>"` placeholder
  in that input (`medias.N.value`, `media_id` or `draft_job_id`); everything else stays concrete. Its price
  comes from its settings, so it is in the cap from the start. When the upstream job completes, put its real
  job ID in, then guard → submit → immediate add. A placeholder can never be guarded or sent; an unavailable
  cost preflight or capability selects a declarative gap, never a consent gate.
- **Where tech specs go.** Aspect ratio, duration, fps and resolution go in params, never in the prompt
  body (user memory rule).
- **Showing prompts.** When you show a prompt to the user, put it in one fenced code block.

---

## 0. Index

| #   | Purpose                                                                                                       | Model                                                              | Historical price (date noted, not a quote) | Status                                                                                                          |
| --- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | -------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| G0  | New location plate for generated scenes (environment only, no people), one per distinct location              | `soul_cinematic` for a photoreal look (quality 1.5k/2k, at most 1 input image); `gpt_image_2_6_flare` (high, 2k; style owner `@image1`, location evidence `@image2`, line `"location_plate": true`) for a stylised look | Current quote for the selected settings | REQUIRED by SKILL.md for every generated scene; every plate inspected for people (Soul Cinema drew one into 6 of 8 measured plates and ignored the cartoon style, VERIFIED (live 2026-10-13); the line registers `takes: 2` with a `take_reason`); see "Soul Cinema location assets" below |
| G1  | Identity sheet from the user's photo                                                                          | `seedream_5_5`                                                  | Current quote | Earlier tests used Seedream 5.0 Pro. |
| G2  | Fictional hero (UGC-real or fashion identity still)                                                           | `soul_2`                                                           | 0.12 / image                           | PROVEN-ish (1 past run); VERIFIED live 2026-10-08 (remake identity, 2k 3:4 = 1536×2048)                         |
| G3  | Requested look or outfit change that keeps the face                                                           | `seedream_5_5` i2i                                              | Current quote | Earlier tests used Seedream 5.0 Pro. |
| G4  | Reference-frame + user-character still: anime/stylized hero, finished still, keyframe or MT input             | `gpt_image_2_6_flare` (default); `nano_banana_2_1` as the cheaper secondary fallback (price or latency); `seedream_5_5` only for a photoreal, identity-first look | Current quote for the selected settings | S1 two-reference baseline (later stills are S3 secondaries, keyframe first); VERIFIED (live 2026-10-13) on `gpt_image_2_5`, see [stills.md](references/stills.md) |
| S1–S3 | Keyframe-first stills: primary hero keyframe, its judgement, secondary stills from the accepted keyframe (two to four references) | `gpt_image_2_6_flare` or `gpt_image_2_6` (quality high, 2k); `nano_banana_2_1` fallback | Current quote for the selected settings | Order, gates and historical 2.5 comparison in [stills.md](references/stills.md) |
| G5  | REPERFORM still: the hero inside the cut's frame, as the MT image                                             | `gpt_image_2_6_flare` (G4's models)                                      | Current quote for the selected settings | In-scene still PROVEN (1 past run, 3/5 won, text-described form); the S1 two-reference / S3 keyframe-first form is UNTESTED as an MT input |
| G6  | Die-cut stickers                                                                                              | `seedream_5_5` + `background: "transparent"`                                    | Current quote | Earlier tests used Seedream 5.0 Pro. |
| G7  | Multi-shot plate (new footage)                                                                                | `seedance_2_5` `omni_reference`                                    | 12 / 7 / 3 cr/s                        | PROVEN-ish (2 past runs); VERIFIED live 2026-10-08 (10 s 720p 4:3 = 70 cr, 1112×834)                            |
| G8  | Per-cut clip from a keyframe, including sub-second cuts                                                       | `seedance_2_5` start image                                         | 12 / 7 / 3 cr/s, min 4 s               | WORKED (/test-edit, 720p)                                                                                       |
| G10 | Re-performance (motion transfer)                                                                              | `hf_mult_motion_control`                                           | 11 / 7 / 3 cr/s of driving video       | PROVEN (4 past runs; one with 5 cuts)                                                                           |
| G11 | Mattes                                                                                                        | `remove_background` / `sam_3_video` / local masks                  | 1 / ≈1.14                              | PROVEN (4 past runs); remove_background 1 cr VERIFIED live 2026-10-08                                           |
| G12 | Chant or VO                                                                                                   | `seed_audio` / `elevenlabs_v4`                                     | 0.3–2 / ≈0.23 per 30 chars             | PROVEN-ish (1 past run, chant)                                                                                  |
| G13 | Texture plates                                                                                                | prefer CODE; `gpt_image_2_6`                                       | Current quote for the selected settings | Historical paper texture run on 2.5 |
| G14 | Seedance 2.5 motion previews                                                                                  | `seedance_2_5` with `draft:true` only                              | Historical draft rate: 3 cr/s          | Draft and finalize prices VERIFIED live 2026-10-08; preview fidelity UNTESTED                                   |

"PROVEN-ish" means the film shipped with no explicit approval recorded.
Worked example: see references/examples.md → "PROVEN-ish history of past projects".

---

## Soul Cinema location assets

A location plate is generated with Soul Cinema (`soul_cinematic`) only when the planned look is photoreal. When the look is stylised (anime, manga, cartoon, illustration, any drawn or painted look) the plate is a `gpt_image_2_6_flare` still (quality high, 2k) with the style owner (the accepted keyframe or style frame) as `@image1` and the location evidence (source frame or location photo) as `@image2`, environment only, and its plan line carries `"location_plate": true`. Every plate, from either model, is inspected for people before acceptance: Soul Cinema drew a person into 6 of 8 measured plates despite "no people" in the prompt (2/2 in the stage 8 test, 4/6 in the 2026-10-13 power-suit run, even from performer-free source crops) and ignored the cartoon style entirely (stills test stage 8, VERIFIED (live 2026-10-13)); a plate with a person is rejected and regenerated within the line's attempts (a `soul_cinematic` plate line registers `takes: 2` with a `take_reason`, so the people check has two takes plus one re-roll; `faces.py detect <plate>` is the free first filter: a detection is a reject, no detection is not acceptance). `ledger.py require_location` and the `quote` warning accept a `location_line` whose plan line is `soul_cinematic` or carries `"location_plate": true` (image kind).

Generate every distinct location needed by newly generated scene footage as a separate location-only plate (model per the rule above) before its Seedance jobs. This applies to interiors, exteriors, studios and stylized or anime worlds, including a location used by only one shot. An existing source frame or supplied location photo can guide this generation, but is not a substitute for the separate plate result. Reuse an already accepted location plate when its required environment is unchanged; do not regenerate it per shot. A KEEP/source-reuse edit or source-anchored Genjutsu transformation that generates no new environment needs no unused location job.

Plan architecture, spatial landmarks, materials, palette and rendering medium from the creative plan and user locks. Keep foreground heroes/products out of the location plate; place them through separate references in the video. Soul Cinema does not reproduce a drawn or painted look (it ignored the cartoon style entirely on 2/2 runs, stills test stage 8), which is why a stylised look takes the flare plate. Soul Cinema's inspected contract uses `quality` 1.5k or 2k (default 2k), not a video `resolution`, and accepts at most one input image with role `image`. A Soul character ID is optional and unnecessary for an empty environment. Use the source frame only as the environment reference; do not send the hero portrait as its background reference.

Record each location ID, generated job/media ID, plate provenance (model and inputs), served output shots and owned visual properties in the creative plan and routes. Keep any explicit geometry/style locks and inspect the result against them; generation is not evidence of pixel identity. If the plate model for the planned look is unavailable or cannot satisfy required locks, retain a permitted original-footage route or report the affected generated scene as partial. Never silently substitute another location-image model or let Seedance invent the missing location from text.

For every Seedance scene, attach the actual accepted location image as its own `medias` item with role `image`, separate from identity/product/style images and any `start_image`. Use `omni_reference` for new scenes and a verified image-reference-capable contract for other allowed modes. Name each reference's ownership using its actual image index: identity references own the subject and the clothing from the user's photo; the location plate owns the environment; the source/start frame owns only its assigned composition and locks. A merged hero-in-location keyframe does not replace the separate location input. Retain the location on drafts, retries and extensions where supported; never switch to text-only `t2v` to omit it. If a mode or reference limit cannot carry the required location and other locks, split into supported jobs or report the limitation without dropping required inputs.

Price each necessary location and its dependent videos within the initial finite plan. Use `stage:"keyframe"` for location ledger lines, with `model:"soul_cinematic"` (`takes: 2`, `take_reason` = the people check) for a photoreal look or `model:"gpt_image_2_6_flare"` (quality high, 2k) plus `"location_plate": true` for a stylised look; run its `generate_image` `get_cost` preflight before `params`. A future Seedance line keeps the location's separate `medias.N.value` as `"<result of LINE>"` (likewise any identity job it waits for). Generate and inspect locations, then put their real IDs into the video lines and submit them inside the unchanged cap. Historical image-only or two-reference examples below do not waive this required location input. The Seedance line also names that line in `location_line`; `ledger.py guard` refuses a `seedance_2_5` `omni_reference` line whose `location_line` does not name a `soul_cinematic` or `location_plate` plan line with a completed job among the line's `role: image` medias (unless `location: "n/a: <reason>"` records retained footage) (stills.md §5).

## Asset ownership and optional prompt structure

Use role-based output slots from `plan/creative-plan.json`: for example hook, context, hero, action,
detail, contrast, payoff or release. Choose only the roles needed by the story/visual motif. Each
slot records its output ID, purpose, start/end state where relevant, screen duration, source evidence,
explicit locks and required assets. A visual montage need not invent a literal character goal.

Prepare hero and prop assets only when existing inputs cannot meet a real need. Location assets follow the mandatory location-plate stage above (Soul Cinema for a photoreal look, a stylised flare plate otherwise), even for a single generated shot. Reuse an accepted location plate across its served slots; do not buy one duplicate per video. No mandatory character sheet, neutral studio, fixed location count or draft purchase.
Never erase, paint over or reshape a face/head with code to create a sheet; a needed model-generated body reference is a separate permitted image operation. Asset preparation uses supported image models;
Seedance 2.5 is reserved for video.

Assign **one explicit ownership per reference** rather than letting every image control everything:

| Input                             | Ownership when selected                                                                                                                                                                  |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| User portrait/character           | Intended identity, distinguishing traits and the clothing the hero wears in every scene (another outfit only on the user's request); background and lighting only if explicitly assigned |
| Reference frame in a G4/G5 still  | Composition, pose, camera angle, framing and assigned style/texture; setting and light only where the plan assigns them; never the performer's identity or clothing                      |
| Source style frame in a new scene | Selected palette, texture, rendering or typography grammar; it need not dictate cast, pose or composition                                                                                |
| Location plate (Soul Cinema or stylised flare plate) | Specified architecture, material and spatial landmarks; shot lighting/camera are separate unless explicitly locked to this plate                                      |
| Prop reference                    | Design, proportions, material and actual markings; scene context only if assigned                                                                                                        |
| Accepted shot keyframe            | Planned shot composition/start state; it does not replace the original identity check                                                                                                    |

Use the smallest sufficient set within the current tool's limits. G4's reference-frame + identity baseline
uses two images; broader scene/asset preparation may use other verified reference combinations
only when their ownership and need are recorded. Never drop a required structural reference to make room
for an unnecessary sheet, blend two people into one identity, or copy the portrait background by accident.

For image and Seedance prompts, include only fields that clarify the selected shot:

1. **Reference ownership and locks:** which image supplies identity and clothing (the user's photo),
   space, prop or selected style.
2. **Optional causal context:** what happened before and its visible trace; want/obstacle if there is a
   story; start state → meaningful end state. Omit irrelevant narrative fields for graphics or pure texture.
3. **Spatial map:** subject count, foreground/midground/background, screen positions, landmarks and
   motion direction when continuity needs them. Specify who acts and who remains unchanged.
4. **One legible action:** a concrete beat or state change. Multi-shot jobs give each slot its own
   action and time interval; do not cram an unrelated routine into one shot.
5. **Camera:** framing/angle and, only if needed, one move + dose + limit (for example, a short lateral
   move ending before the subject leaves the frame). A locked camera is valid; no compulsory movement.
6. **Light and texture:** selected source grammar and shot-specific motivated light/material response.
   Avoid contradictory ownership between a location plate and a separate light instruction.
7. **End constraints:** identity and the clothing from the user's photo, stated explicitly ("wears
   <the photo's garments> in every shot"), intended cast, prop design, required text/graphics and continuity.
   Generated clean layers have a concrete later text/compositing plan; they do not silently remove locks.

Fill unlocked fields from the creative plan and retain the selected visual grammar. Image prompts describe the
chosen still state, not a motion sequence. Technical duration/aspect/resolution stay in API params.
This structure is optional guidance, not a sentence-preservation template. It does not apply to
Genjutsu, whose operation prompt remains at most two sentences / 40 words.

## G1. Optional identity sheet

- **When to use:** only when a measured identity-consistency problem requires an additional prepared
  anchor and a suitable supplied image or reference-frame + identity still (G4) does not already solve it.
  A small face or an F2 classification alone does not require a paid sheet. Never create one per cut.
- Preserve the assigned reference ownership. The user's photo supplies the identity and the clothing
  the hero wears; a sheet preserves both without locking all future shots to one pose/background. A
  sheet does not replace a required composition frame or original identity reference.
- **Params shape** (verify multi-reference support and actual settings for the selected image model):
  ```json
  {
    "model": "<verified image model from plan>",
    "aspect_ratio": "<planned sheet layout>",
    "resolution": "<from plan line>",
    "count": 1,
    "medias": [
      { "role": "image", "value": "<style frame media_id>" },
      { "role": "image", "value": "<authorized user photo media_id: identity and clothing>" }
    ],
    "prompt": "Prepare only the planned identity reference views. Image 1 supplies <assigned material/style ownership> only, never its performer or outfit; image 2 supplies the identity and the exact clothing the person wears in every view. Preserve <explicit locks> without importing the portrait background."
  }
  ```
- Record the necessary views. Do not claim unseen facial details or garments were observed in a
  cropped photograph; lock the clothing the user's photo shows and record any part it hides as unobserved rather than designing a new look. Compare the sheet to both inputs before reuse. Keep the original photo available for
  identity checks: historical sheets sometimes widened the face.
- Use a neutral isolation background only for a needed intermediate, never as the automatic final
  setting. Its background/light must not overwrite the authored scene.
- Reuse the sheet only where needed and supported. Composition frames retain their reference role;
  any extra identity input must fit the verified model limits and the priced plan. Never drop a required
  composition frame to make room for a redundant sheet. The G7 wardrobe inventory lists the clothing from the user's photo.
- **Historical price:** Seedream 5.0 Pro was 2.5 cr. Re-price the actual selected model/settings. Use
  count 1, at most three planned attempts, no character picker or approval gate.

## G2. Fictional UGC-real hero: Soul 2.0 selfie

- **When to use**
  - The user wants an invented hero ("a girl generated in Soul 2.0").
  - The reference is phone or UGC footage.
  - Soul gives a realistic selfie look.
  - It also made the identity still of the 2026-10-08 live-test remake (a full-length fashion portrait on a
    white studio backdrop, the only identity ref of its Seedance plate): VERIFIED live, 0.12 cr, 2k 3:4
    output = **1536×2048** PNG. The "seamless white" backdrop came back slightly grey: harmless for a
    Seedance ref, but lift levels in code before thresholding or keying the still itself.
- **Params**. These are the param names as recorded. Verify the names with `models_get`.
  ```json
  {
    "model": "<from plan line: soul_2>",
    "aspect_ratio": "<from plan line: 4:3>",
    "quality": "<from plan line: 2k>",
    "count": 1,
    "prompt": "<below>"
  }
  ```
  - `style_id` and `enhance_prompt` are not in the verified MCP contract (mcp-api.md §5.1) and `ledger.py params --check` rejects them as invented provider fields; do not add them.
  - Soul takes at most 1 image ref.
  - Use `soul_id` only for a trained Soul.
- **Price**: 0.12 cr per image. The `get_cost` preflight ignores `count`, so multiply it yourself (mcp-api §4).
- **Count**: 1. Use this branch for an explicitly requested fictional hero or an unlocked supporting
  character required by the story; never replace the user's intended hero. Select internally; no
  character picker. At most three attempts within the plan (the line's registered takes plus one documented re-roll per take).
- Worked example: see references/examples.md → "Soul 2.0 selfie hero prompt".
- **Historical structure**, adapt to the selected output role and ownership; do not invent age or ethnicity unnecessarily:
  1. Capture device and framing.
  2. The permitted fictional character and story role; age/ethnicity only if necessary to the actual brief.
  3. The planned location.
  4. Hair.
  5. Skin and makeup.
  6. Contracted outfit/accessories (as the user specified them; never the reference performer's outfit).
  7. The planned gesture or still pose.
  8. Planned background props and explicit prop locks.
  9. Selected light/texture grammar and planned scene lighting.
- Describe the actual permitted subject plainly. Do not relabel a subject or remove reference evidence to evade a rejection; see §2.
- Do not use `soul_cast` for creatures, quadrupeds or stylised media. It forces photoreal humanoids and
  drifts the background to grey (an older note). Use `gpt_image_2_6_flare` instead (`nano_banana_2_1` as the cheaper fallback, stills.md §6).

## G3. Requested look or outfit change that keeps the face: Seedream i2i

- **When to use**: only when the user explicitly asks for a different look or outfit than the one in
  their photo, or a prepared identity image has drifted from the clothing in the user's photo and must
  be restored. Never use it to dress the hero in the reference performer's outfit or an invented look.
- **Params**
  ```json
  {
    "model": "<from plan line: seedream_5_5>",
    "aspect_ratio": "<from plan line: 4:3>",
    "resolution": "<from plan line: 2k>",
    "count": 1,
    "medias": [{ "role": "image", "value": "<chosen identity still job_id>" }],
    "prompt": "<below>"
  }
  ```
- **Price**: 2.5 cr.
- **Count**: 1.
  - One past run held a 4-image shootout with 2 × `gpt_image_2` 2k high (6.5 each) and 2 × Seedream.
  - Seedream #3 was used. Seedream #4 was also fine.
  - Both `gpt_image_2` outputs gave a beige coat instead of caramel-brown.
- Worked example: see references/examples.md → "Seedream look-change prompt".
- **Structure**, in this order:
  1. "Keep the exact same <person>" + the identity features to preserve.
  2. "Change only <the requested outfit/pose>: …", with every new item's colour and material.
  3. The same location, light and camera.
  4. Exclusions.
- "slipping off her shoulders" passed here, on an image. It was removed from the Seedance prompt
  (see §3).

## G4. Reference-frame + user-character still: the S1 two-reference baseline

The keyframe-first order (the first accepted still becomes `@image1` of every later still), the judged-still gate, the measured model matrix and the failure modes of this recipe are in [stills.md](references/stills.md); this section keeps the API shape and the ownership rules.

This recipe makes a still that combines a reference frame's composition and pose evidence with the
user's character, for a planned shot whose composition that frame should supply. A scene whose
composition, pose and setting are authored from scratch uses the optional asset/prompt structure above
instead: a source frame there may own selected style only. Do not force G4's composition lock onto
every new scene or a two-image limit onto another supported, explicitly mapped asset need.

Use this route for an anime, stylized or photographic hero still, a finished still/code-composited shot, a Seedance 2.5 start frame, or a motion-transfer input. It is not limited to video keyframe preparation. Before a keyframe is accepted (S1, stills.md §2) the still takes two current user-authorized images: the style owner frame first (for a stylised look the `owner` of `analysis/style.json`, stills.md §2; `ledger.py guard` refuses another frame), the uploaded character/person image second. Once a keyframe is accepted, every later still is an S3 secondary (stills.md §3): the accepted keyframe `@image1`, the photo `@image2`, the reference frame `@image3` only when the shot's composition comes from a cut, the accepted location plate `@image4` only when the still must sit in that location. Never add a third identity image or replace the frame with a text description of its composition.

The first image owns composition, pose, camera angle and framing, plus the art style, textures, lighting, setting, props, other people and typography the plan assigns to it. The second image owns the hero's identity and clothing: the hero wears exactly the outfit from the user's photo, never the reference performer's garments, unless the user explicitly asked for another outfit. This applies to every appearance of the hero, including back views, silhouettes, helmets, body/hand crops, occlusions and distant shots; facial visibility is never a prerequisite. Do not average the user's face with the reference performer's face, keep the performer's identity or outfit by accident, or import the uploaded photo's background or lighting unless explicitly requested. Keep a hidden face hidden: do not turn a back view toward camera, remove a helmet or brighten a silhouette merely to display the hero's face. Track the hero through neighboring shots and record the relationship; unrelated B-roll and other people are not identity targets.

Default to `gpt_image_2_6_flare` (use the plan’s Sunburst ID when identity takes priority; pass the plan quality); `nano_banana_2_1` only as the cheaper secondary fallback once a keyframe is accepted (a fallback for price or latency, never for a refusal); `seedream_5_5` only for a photoreal, identity-first look. `nano_banana_2`, `nano_banana_pro`, `ideogram_4_5` and `flux_3_image` are not keyframe models (stills.md §6). Resolve the actual supported image parameters and price; image models remain distinct from the Seedance 2.5 video restriction.

```json
{
  "model": "<from plan: gpt_image_2_6_flare, gpt_image_2_6 or verified selected multi-reference image model>",
  "quality": "<from plan line: high; the ledger refuses a quality-priced image line without it>",
  "resolution": "<from plan line: 2k>",
  "aspect_ratio": "<from plan: the shot's ratio, supported by the model>",
  "count": 1,
  "medias": [
    { "role": "image", "value": "<reference frame media_id>" },
    { "role": "image", "value": "<uploaded user character/person image media_id>" }
  ],
  "prompt": "The first reference owns the composition, pose, camera angle, framing and <assigned style, texture, light and setting>. Place the person from the second reference in <the hero's position>, with the same face and identity and wearing exactly the clothing from the second reference, rendered in the first reference's style. Do not blend their face with the first reference's performer and do not use that performer's clothes. Do not copy the second reference's background. Keep the first reference's face visibility and occlusions; a hidden face stays hidden. <Planned changes to setting, props, other people and text, or: keep them unchanged.>"
}
```

Extract each relevant reference frame at full source resolution (`frames.py keyframes`) after complete reference analysis, including the frames for the hero's hidden-face shots. Do not substitute a frontal close-up for a back view or crop just to simplify identity verification. Text and graphics in the frame stay only where the plan keeps them; authored wording is a separate overlay (`compositing.md`). Describe first/second input roles in prose as well as any image tags supported by the actual model. One result per request; the line's attempts (its registered takes plus one documented re-roll per take, at most three per item) within the finite plan, selected internally without questions.

Choose the least generative continuation that serves the shot. A still plus measured whole-frame/layer camera motion may be sufficient; never animate facial landmarks, reshape the face or simulate expressions in code. If new motion is needed, use the accepted frame as a supported Seedance 2.5 start/reference image. If specific source choreography requires direct motion transfer, use G5/G10 with the existing driving video. Do not buy both routes as automatic alternatives.

Genjutsu catalog presets are an optional route, not the default for every anime reference. Read [Genjutsu routing](references/genjutsu-routing.md) before selecting one. A catalog `genjutsu:<id>` and a public Restyle API preset identifier belong to different contracts and are never interchangeable. Any real content refusal still forbids identity disguise, removal of evidence or model switching to evade the restriction; use a supported fallback or declare the affected branch unresolved.

## G5. REPERFORM still: the hero inside the cut's frame, as the Motion Transfer image

- **When to use**: a supported REPERFORM cut whose existing supplied or prepared image does not already show the hero (identity and the clothing from the user's photo) in the driving clip's framing (`routing.md` §2.2). Reuse a suitable existing image; do not generate a new still for every cut automatically.
- **Why**: with the bare user photo, MT rebuilt the background from the photo. One past project's cut c03 came back
  as a TED-like stage with giant letters.
- **Evidence**
  - A still of the hero already inside the cut's set won on 3 of 5 cuts and tied on the other 2
    (one past run). Those stills were text-described (hero photo + a description of the set), because the
    user's 2-ref rule did not exist yet.
  - Another past run used a frame of the hero already in its hangar set.
  - A third used 2 real photos with plain backgrounds.
- **When a new image is needed:** with no accepted keyframe yet it is the S1 still (G4's shape: `@image1` = the
  reference cut frame from `frames.py keyframes`, `@image2` = the hero photo; two refs). Once a keyframe is
  accepted it is an S3 secondary (stills.md §3): `@image1` = the accepted keyframe, `@image2` = the hero photo,
  `@image3` = the reference cut frame, which still owns the composition and is never replaced by a text
  description.
  - As an MT input neither form is tested. A moderation or IP rejection does not authorize transferring the same blocked request to this model.
  - Reuse one suitable image across cuts only while it preserves their measured composition and appearance. For a take or part needing a new image, use its relevant source frame. Do not purchase comparison images or extra MT jobs merely to compare routes.
- **Params**: G4's block (S1) or stills.md §3's block (S3) with the measured source-frame aspect and geometry. Never force historical 4:3 or 3:4 examples onto another source. If the verified model requires a supported input shape, use a documented reversible pad/coordinate mapping that preserves the intended composition; inspect actual output dimensions before mapping it back.
- **Prompt**: G4's template (S1) or stills.md §3's structure (S3). When the user wants a different world from the reference (as in some past MT films),
  keep both refs and name the world changes after the placement sentence: place, materials, light;
  wardrobe changes only when the user requests them. The source video and identity images anchor the actual subject; do not replace a celebrity with a generic identity or conceal who is depicted.
- **Price**: obtain the current one-job estimate for the selected 2.6 ID and settings. The line’s attempts (its registered takes plus one documented re-roll per take, at most three per item; a one-take line has two) within the plan; then another planned route or a declarative limitation.
- **Fallback.** A text-only scene approximation must not be used to evade moderation or an IP restriction. If no permitted route can produce the shot within the plan, record the blocked cut and report it without a question.

## G6. Die-cut stickers: Seedream transparent background

- **When to use**: an output role needs graphic stickers whose required pixels cannot be reused.
  Author an appropriate set from the selected graphic grammar. Prefer suitable existing assets and
  generate only missing planned items.
- **Params**: one sticker per `generate_image` request, `count:1`, through its own reservation and immediate ledger registration. The platform batch limit does not enable multi-item submissions in this workflow.
  ```json
  {
    "model": "<from plan line: seedream_5_5>",
    "aspect_ratio": "<from plan line: 1:1>",
    "resolution": "<from plan line: 1k>",
    "background": "transparent",
    "prompt": "<below with {ITEM}>"
  }
  ```
- **Output**: 1024×1024 RGBA PNG. Visible art covers 50–85% of the canvas. Crop to the alpha bbox
  (+6 px) before sizing, or the stickers look too small.
- **Price**: get a current quote for the selected resolution and background. Run the `get_cost` preflight first.
- **Count**: match the planned output inventory/timing.
  Reuse suitable assets before buying missing ones. One past project's historical 30-sticker set is not a default.
- Worked example: see references/examples.md → "Die-cut sticker prompt and item list".
- **Historical recipe details, not defaults:** the example used three colours, a white die-cut border and a grey removable background. Follow the selected palette, edge treatment and lettering grammar instead; do not copy the example's text exclusions when a planned sticker has letters or logos.
- **Building the item list**
  - Derive the planned items from the story and selected shape/texture/palette/border/lettering
    grammar; preserve explicit locks.
  - Worked example: see references/examples.md → "Die-cut sticker prompt and item list".
  - The historical "cute ghost" was pulled for a past project's taste decision. Do not drop a current planned item on that basis.
- **Sticker-sheet alternative (UNTESTED)**
  - One 2k image of about 12 stickers, evenly spaced on plain light grey and not touching, with
    `background: "transparent"`.
  - Slice it in code by alpha connected components.
  - Historical price comparison: one 2k image (2.5) instead of 12 × 1.25 (15). Use only when it serves the planned set within the verified finite plan; the first required sheet can be its canary. Do not buy duplicate comparison jobs.

## G7. Seedance 2.5 `omni_reference` multi-shot plate

- **When to use**: required new output footage that existing usable footage cannot supply, grouped
  only where the authored roles and locks remain intact (`routing.md` §3.1). Scenes are authored
  using the selected reference grammar. A clean set is appropriate
  when planned for the actual scene or a documented compositing intermediate, never by generic default.
- **Params**
  ```json
  {
    "model": "<from plan line: seedance_2_5>",
    "mode": "<from plan line: omni_reference>",
    "duration": "<from plan line: sum of the shot slots>",
    "resolution": "<from plan line>",
    "aspect_ratio": "<from plan line>",
    "bitrate_mode": "high",
    "generate_audio": false,
    "medias": [
      { "role": "image", "value": "<composition/style frame or accepted keyframe id>" },
      { "role": "image", "value": "<identity + clothing reference id: photoreal look = the user photo media_id as supplied or a G1 character-sheet job_id, never a generated hero still; stylised look = the accepted stills.md keyframe job_id; omit this entry if unnecessary>" },
      { "role": "image", "value": "<accepted location plate job_id or media_id (a soul_cinematic or location_plate line)>" }
    ],
    "prompt": "<below>"
  }
  ```
  - Image tags follow the actual submitted image order; after omitting an optional entry, update every tag and ownership instruction. The separate location plate remains required.
  - Use explicitly assigned image ownership: a composition frame for structure where the plan keeps it,
    a style frame only for selected visual grammar, the identity reference for the hero's identity and
    clothing, necessary prop references. The location plate separately owns the environment.
    Use a supported `start_image` where the first frame must be pinned; in `omni_reference` it is
    treated as a reference, so take in-points from the returned frames. Omit unnecessary references
    rather than generating an extra sheet; never omit the required separate location plate input.
  - Set `generate_audio: false` every time. The model default is TRUE.
  - Never use audio refs. Audio refs with `generate_audio:true` gave nsfw 4/4 in one past run. Seedance also
    re-speaks an audio ref instead of passing it through.
  - Set mode, resolution, duration and aspect explicitly, from the plan line. The model default is t2v
    at 720p, 5 s, 16:9 with audio on. `t2v` rejects all reference media.
  - Duration is an integer from 4 to 30.
  - The plan line itself states `"generate_audio": false` and `"bitrate_mode": "high"` (header), so
    `ledger.py params` and `--check` carry them; `ledger.py quote` warns on a Seedance line without them.
  - Output is 24 fps. 1080p 4:3 = 1664×1248 HEVC Main10. **720p 4:3 = 1112×834 H.264, 24 fps**: a
    10 s plate came back as 241 frames (VERIFIED live 2026-10-08). Size the k720 arithmetic
    (`budget.md` §5) on 1112 / 834, not on 960 / 720.
- **Duration** (the plan line's, from `budget.md` §4.3; one formula, no extra multiplier):
  - Multi-shot plate: duration = Σ slot_s, where slot_s = clamp(2 × the screen seconds the EDL needs
    from that shot, 2, 4).
  - Continuous-routine plate (the selfie gesture-routine A1 kind): duration = ceil(1.6–2 × the prompted routine
    length), with the must-have beats in the first half.
  - Round up to the required integer duration, respecting the verified model minimum. Use that full
    duration within the live supported maximum (historically 30 s), or split into sufficient jobs before
    pricing. Never clamp a longer sum to 15 s, truncate the routine or drop a planned slot. The prompt's
    `Shot n (a-bs)` timecodes are these slots.
- **Price**: 12 / 7 / 3 cr per second at 1080p / 720p / 480p.
  - The rate is the same for t2v, omni_reference and extension.
  - Audio on or off, bitrate high, aspect ratio and ref count do not change the price. So bitrate high
    is free.
  - Examples at 1080p: 4 s = 48, 10 s = 120, 12 s = 144, 15 s = 180.
  - An older note's 63/135 cr figure is stale; the price is now 33% higher.
  - VERIFIED live 2026-10-08: one 10 s 720p 4:3 plate (five 2 s shots) was charged exactly 70. That
    single plate, plus a 0.12 cr Soul identity still and a 1 cr matte, carried a whole fashion-film
    remake at 7.9 cr per final second (the original past project spent ~120 per final second).
- **Composition and evidence.** Record each output shot and its input ownership in `plan/routes.json`.
  Scenes use authored geometry with selected style/location/identity evidence; an existing matching
  keyframe, a G4 still or a necessary prepared scene image may anchor them. Do not replace a required available structural
  reference with text alone merely because a clean studio plate is convenient.
  - Use the accepted frame as a supported Seedance reference or `start_image`. A start image anchors only its own initial frame; validate each later shot. Split into the necessary jobs if one multi-shot plate cannot retain all required compositions, rather than dropping a planned one.
  - A scene follows its planned set/light and selected grammar.
    Never recolour an identity-locked prop merely for easier keying.
  - A per-cut G8 clip is justified whenever it serves the shot best, including a short but important shot. Model minimum duration is a billing constraint, not permission to change the planned output timing.
- **Preserve the planned full cast.** Scenes retain their authored cast and explicit identity locks. A separately isolated plate may contain
  one person only if all other required people remain in verified layers. Never accidentally drop a
  planned person to simplify face tracking or background removal.
- **Count**: 1 take.
  - **Canary**: the planned plate covering the family's hardest fidelity constraints, alone, at final settings (header and
    `budget.md` §7).
  - **Second take**: no discretionary alternative. A corrective retry needs an observable failure of
    the selected shot contract, within the plan reserve and retry limit.
  - **Re-roll** (`budget.md` §3 rung 5). Log every re-roll with its reason; "a better take" is not a
    failure.
    - Shot failure: a planned shot fails a check from the fail list: identity, wardrobe, garbled text
      or logo, anatomy, a matte-hostile background, or a missing beat the EDL needs that no other plate
      second supplies. Re-roll that shot alone as a single-shot job of max(4, ceil(2 × its slot)) s at
      the same resolution.
    - Job failure: the canary fails, or half or more of a job's planned shots fail for one cause. Fix
      the cause and re-run the whole job once (that is the job's re-roll).
    - Re-roll spend per job stays ≤ that job's own cost, within the pre-priced reserve, and only while
      `ledger.py guard $W --line <ID> --reroll-of <job> --reason <fail-list item>` passes. For a
      single-shot re-roll add `--slot <the shot's slot seconds>`; `ledger.py params $W --line <ID> --slot
      <s>` prints that job's skeleton.
- **Prompt shape**: use the optional ownership/causal/spatial structure above, then the required shot
  slots. Leave technical specs in params; keep separately composed effects in the layer plan.
  1. **Header**: what each `@image` is, plus an exhaustive inventory of identity items to keep "in
     every shot", including every garment from the user's photo. Use HEADER-FULL for body shots and HEADER-CU for close-ups.
  2. **Prop line** (when needed): preserve the prop reference's material, colour and shape; solve keying in compositing without changing the prop.
  3. **Style and scene line**: planned set, light, camera behaviour and selected reference grammar.
  4. **`Shot n (a-bs): …`**: only the necessary shots, each with its role, framing and action. The timecodes are the slots
     above.
  5. **Closing line**: preserve explicit locks and planned details. Authored wording/graphics are
     composed later as overlays. Never exclude required final content without its documented later layer.
- **Prompt examples (VERBATIM, one past fashion-film project)**: two headers, then four used scenes.
  Worked example: see references/examples.md → "Fashion-film multi-shot plate prompts".
  - **EXAMPLE ONLY: copy the structure, never these identity items** (header rule). A dry-run eval
    pasted that hero's wardrobe and props into another user's plates. Keep the
    shot-list structure only; derive subject, scene, camera, light, expression, text and motion from the authored creative plan and selected grammar, and wardrobe from the user's photo. These historical studio scenes are not default prompts.
  - **Do not copy their durations.** These prompts ran as 15 s plates (`Shot 5 (12-15s)`) in a project
    that generated 11× what it used: 270 s for about 24 s on screen, 180 cr per plate at 1080p. Copy the
    timing grammar only, author shot text for the current plan, then re-time it to the measured slots and set the plan line's
    duration to their sum. Never set duration 15 because the timecodes end at 15. A worked re-timing
    of those scenes (full text in `references/examples.md` → "Fashion-film multi-shot plate prompts") follows.
  - Scene f1 of the example is the **aura recipe**: slow motion + side wind + "calm, unbothered … no smiling".
  - Scene f3 of the example (Prop line):
    - Lessons from that scene, under a hard threshold look:
      - Shot 1 came out as a backlit silhouette, a black blob.
      - Shot 3's glint became an unreadable white bar. A lime star was drawn in code instead.
    - Those were historical failures, not reasons to drop a planned shot. Keep a planned silhouette or
      glint readable; fix the local tonal treatment or compositing layer instead.
    - VERIFIED live 2026-10-08: on identity-legible medium close-ups the xerox threshold crushed the
      face to near-black, while the reference keeps facial detail there. If the compositor introduced
      this error, correct the whole-shot grade (`compositing.md`), not a face mask
      or face-only retouch. A defect already present in the generated face requires a supported
      generation correction within the plan.
  - **Re-timing example** (the `budget.md` §4.3 arithmetic; this re-timed prompt has not been run).
    Suppose the EDL needs 1.0, 0.75, 1.5, 1.0 and 0.5 s from scene b's five shots.
    - Slots: clamp(2 × need, 2, 4) = 2, 2, 3, 2, 2 s. The plate is 11 s: 132 cr at 1080p or 77 at 720p,
      against 180 / 105 for the 15 s original.
    - Keep the shot texts and change only the timecodes: `Shot 1 (0-2s)`, `Shot 2 (2-4s)`,
      `Shot 3 (4-7s)`, `Shot 4 (7-9s)`, `Shot 5 (9-11s)`. The plan line says duration 11.
    - Scene f1's four shots with needs of 1.5, 1.0, 1.0 and 2.0 s re-time to 3 + 2 + 2 + 4 = 11 s.
- **Selfie gesture-pool plate (VERBATIM example A1, 10 s, @image1 = Soul heroine)**. This is the skeleton
  for UGC and jump-cut refs. **EXAMPLE ONLY: copy the structure, never the identity items** (header
  rule); your beats come from your output shot list.
  Worked example: see references/examples.md → "Selfie gesture-pool plate A1".
  - Skeleton, in this order:
    1. Capture device.
    2. The hero from the identity reference, wearing the clothing from the user's photo.
    3. Location.
    4. Light.
    5. Planned camera, framing and subject placement.
    6. Action routine.
    7. Timestamped beat list.
    8. Planned expression and cut structure; a text exclusion only when the plan composes the text as a later layer.
  - **Timing reality: timecodes are ordering hints, not a schedule.** The gestures arrived 1.5–1.6×
    slower on A1 and about 2× slower on B1. In the 2026-10-08 live-test run the five 2 s shot slots of a
    10 s plate landed almost exactly on their timecodes (VERIFIED live). Both happen, so never plan an
    in-point from a timecode: put the beats you cannot lose early and choose in-points from the sheet.
  - Do not ask for "repeats the same routine". That half was never used, and it lacked the second
    cat-paw the edit needed.
  - List each needed beat once and put the beats you cannot lose early.
  - A1 ran 10 s. Under the continuous-routine rule its 4.5 s routine sizes to ceil(1.6–2 × 4.5) = 8–9 s,
    with no "repeat" half: nothing after 4.89 s of A1 was used.
  - With a second person (past plates B1 and F1), add one sentence for the friend from `@image2` with their
    position in frame. It passed in both plates.
  - A hard face-lock can crop other people. Preserve every planned performer. Use an appropriate uncropped plate or separate verified layers rather than dropping a person to simplify matting.
- **Do not**
  - Do not write `SAME FRAME` (a past project handoff).
  - Match the planned acting and identity. Do not inherit a
    stare or smile merely because a historical example preferred one.
  - Avoid backlit silhouettes, specular glints, props pointed into the lens or low-angle faces under a
    threshold look unless the plan needs one; then check it on the canary.
  - Describe the authored move, dose and limit, or a locked camera, consistent with selected grammar
    and continuity.
    Carry the energy of the reference moment a shot serves (`analysis/energy.json`: its pans, shake bursts and
    hits) into the prompt with magnitude: "fast handheld push-in", "whip pan left", "hard shaky tracking".
    Seedance plates come back calmer than the reference (past remixes: about a third of its camera movement),
    so the rest goes into the EDL as camera work (`shake`, `handheld`, `pan`, `punch`) from the same events.
    Whole-frame zooms and separate particles may use code within the face boundary.
- **Choosing in-points**: from the real plate's timestamped contact sheet (`frames.py catalog`, 4 fps by
  default), never from the prompt's timecodes, even when a plate happens to follow them (2026-10-08). Catalogue only after every submitted paid job in the planned group is
  terminal (header, "Guarded submissions and job polling").

## G8. Per-cut clip from a keyframe: Seedance start image + face ref (/test-edit). WORKED

- **When to use**: an output role needs new motion and a dedicated Seedance clip fulfills its shot
  specification better than a shared plate, existing footage or whole-layer animation. It may use a
  newly authored scene/keyframe or a G4 still. This includes brief or sub-second shots. G10 is reserved for specific desired source choreography, not every performer.
  - Satisfy the live model's minimum job duration while retaining the authored output interval.
    Do not change required timing for billing efficiency.
  - Reuse a shared plate only when it preserves every required output composition and beat equally
    well. Price and latency break ties; they do not authorize dropping explicit locks.
- **Start frame**: reuse a suitable image, prepare a G4 still when a reference frame should supply the
  composition, or prepare the authored scene under the asset-ownership rules. G4 is not mandatory for
  every new scene.
- **Params** (role names unverified, so check `models_get`; start and end images only work in
  `omni_reference`):
  ```json
  {
    "model": "<from plan line: seedance_2_5>",
    "mode": "<from plan line: omni_reference>",
    "duration": "<from plan line: >= 4>",
    "resolution": "<from plan line>",
    "aspect_ratio": "<from plan line>",
    "bitrate_mode": "high",
    "generate_audio": false,
    "medias": [
      {
        "role": "start_image",
        "value": "<suitable existing image id, or G4 keyframe only if needed>"
      },
      { "role": "image", "value": "<identity + clothing reference: the user's photo; omit this entry if unnecessary>" },
      { "role": "image", "value": "<accepted location plate job_id or media_id (a soul_cinematic or location_plate line): required for a newly generated scene>" }
    ],
    "prompt": "<below>"
  }
  ```
  - The separate location plate (Soul Cinema for a photoreal look, a stylised flare plate otherwise) is required here exactly as in G7 ("Soul Cinema location assets"): a start frame that already shows the location does not replace it, and the ledger refuses a Seedance line without its location input. Update the `@imageN` ownership sentences to the submitted order.
- **Price**: 28 cr per 4 s at 720p (48 at 1080p). /test-edit ran 6 × 5 s at 720p (35 each); all 6
  passed and were used.
- **Prompt (VERBATIM shape, /test-edit `clips.sh`, CLI tag format).** **EXAMPLE ONLY: copy the structure,
  never these identity items** (header rule): the gargoyle
  ledge, blazer and stubble are that user's.
  ```
  Slow dramatic push-in from a low angle while he crouches on the gargoyle ledge; wind moves his hair and blazer, he slowly tilts his head down and locks eyes with the camera, a slight confident smirk. The man keeps exactly the face from <<<image_1>>> in every frame: same eyes, nose, jaw, stubble and short light-brown hair. He wears his dark navy blazer and open-collar white shirt throughout. Cinematic action-film look, anamorphic, photoreal, no text. <<<image_1>>>
  ```
  - Describe the selected shot's camera/action and look from the authored plan, and the identity and
    wardrobe from the user's photo, as the example's "He wears … throughout" sentence does. The historical “no text” ending needs a later planned
    graphic layer when final text is required; it is never a blanket final-content exclusion.
  - In MCP calls, use `@image1`-style references, as past MCP runs did.
- **Caveats**
  - The keyframes in that run were inadequate text re-descriptions of reference frames: where a
    reference frame should supply the composition, send the frame itself through G4. Authored scenes
    use the prompt structure above and relevant reference ownership.
  - The film itself (v1) was rejected for compositing reasons; the clips were fine.
  - A Spider-suit costume round ended nsfw on 5 of 6 clips.

## G10. Genjutsu motion transfer: `hf_mult_motion_control`

- **When to use**: REPERFORM routes.
  - Select only when the output shot specifically needs the source's body/camera choreography.
    A new world, anime styling or a person in frame alone does not justify MT; default scene
    coverage comes from usable footage, necessary image preparation and Seedance 2.5.
  - Historical: the hero re-performs the reference's body and camera choreography in a new world, the main source
    of three accepted past films.
- **Not useful** when nothing in the reference performs: static photos, or peopleless refs (City
  Rhythm).
- **Driving video prep.** Muting, splitting at measured source cuts and padding have historical
  evidence (several past runs). Burned-in captions and graphics in the driving clip can come back as
  garbled copies (§4): prefer a window crop or a part that excludes them when the performance allows.
  Planned wording is a separate overlay.
  - **Split** (`routing.md` §3.2). MT drives only the performance interval a shot needs, never the
    whole reference. One take for an interval of about 11 s or less with no burned graphics; otherwise
    5–9 s parts cut at the reference's own cuts. A single-cut REPERFORM is one 96-frame clip.
  - **Export at 24 fps with the window crop, muted.** For one cut, two commands, then a check:
    ```bash
    python3 $RR/frames.py export $W --cut c07 --fps 24 --crop window        # -> $W/cuts/c07.mp4, muted, 24 fps
    python3 $RR/frames.py pad $W/cuts/c07.mp4 $W/gen/c07_pad.mp4 --mode pingpong --for mt   # < 4 s -> exactly 96 f
    ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames \
      -show_entries format=duration -of compact=p=0 $W/gen/c07_pad.mp4      # 96 frames, 4.000 s
    ```
    `export` works per cut, so for a multi-cut
    part or a full take run the same frame-exact trim, crop and 24 fps re-time in one ffmpeg pass (even
    w and h; `end_frame` is exclusive):
    ```bash
    ffmpeg -v error -i $W/ref/ref.mp4 -an \
      -vf "trim=start_frame=<f0>:end_frame=<f1+1>,setpts=PTS-STARTPTS,crop=<w>:<h>:<x>:<y>,fps=24" \
      -c:v libx264 -crf 12 -pix_fmt yuv420p $W/cuts/partA.mp4
    ```
    Never pad a native-fps clip of a 25/30/50/60 fps reference. `pad` writes its input frames as-is at
    24 fps, so the motion slows and the billed seconds grow: an 11 s 30 fps full take padded as-is
    bills 14 s (154 cr at 1080p) instead of 11 s (121). `pad` exits 2 on an fps mismatch unless you pass
    `--retime`. VERIFIED live 2026-10-08: `frames.py export` of a 35-frame cut of a 60p reference gave
    14 frames @24, and `pad --mode pingpong` made exactly 96 frames (4.000 s).
  - **Pad.** MT bills and returns round(seconds).
    - A cut shorter than 4 s of real time: ping-pong to exactly 96 frames (`frames.py pad … --mode
      pingpong --for mt`). Never hold-pad: repeated frames broke the pose in one past run.
    - A part whose fractional second is 0.1 s or less: do not pad. Inspect the actual missing tail and
      fill it only with verified transformed footage or a hold satisfying timing/motion and identity
      locks; otherwise use a bounded permitted correction or report the gap. Original pixels are
      eligible only when verified to contain no targeted change and to satisfy every applicable lock;
      never reintroduce the original target. One past run's unpadded 11.08 s full take billed 11 s (121) and
      kept the cuts within ±1 f.
    - Any other part: freeze-pad the tail to ceil(seconds) (`frames.py pad … --mode freeze --for mt`). Unpadded,
      such parts came back truncated or extended with invented shots (one past run's halves: 152→145 f,
      114→121 f).
  - **Check.** The probed frame count ÷ 24 must be the whole number of seconds you intend to pay for
    (96 → 4.000 s, ±0.01 s on `format=duration`). Price the plan line from the PROBED frame count, not
    from a nominal 96: run the `generate_video` `get_cost` preflight on the prepared clip, record it with
    `ledger.py price-set $W --line <ID> --frames <probed count> --credits <C> --source get_cost_video
    --evidence 'generate_video get_cost:true hf_mult_motion_control 720p 4 s: 28 cr'`, then reserve with
    `ledger.py guard $W --line <ID> --frames <probed count>` before submission. The guard does not
    fetch a live price.
  - Upscaling the input does NOT raise the output resolution. Never `reframe` a driving video.
- **Params**
  ```json
  {
    "model": "<from plan line: hf_mult_motion_control>",
    "resolution": "<from plan line>",
    "medias": [
      {
        "role": "image",
        "value": "<suitable existing image id, or a G5 still (S1 two-ref before a keyframe is accepted, S3 keyframe-first after; stills.md §1) only if needed>"
      },
      {
        "role": "image",
        "value": "<optional extra identity reference; omit this entry if unnecessary>"
      },
      {
        "role": "video",
        "value": "<prepared 24 fps driving clip, probed>"
      }
    ],
    "prompt": "<below>"
  }
  ```
  - Roles are the current schema keys: at least 1 `image`, exactly 1 `video` (mcp-api §6.3).
- **Price**
  - **11 / 7 / 3 cr per second of driving video** at 1080p / 720p / 480p.
  - MT bills round(seconds): 4 s = 44, 10 s = 110, 11 s = 121.
  - Parts pay their own rounding: one past run was 6 + 5 + 8 = 19 billed seconds = 209 at 1080p, not
    17 × 11 = 187.
  - A second image is free. Genjutsu defaults to 720p, so always pass the plan line's `resolution`.
  - The quote shows MT lines as "fixed input (min-billed)" with no utilisation target. Never group
    cuts into one input to improve the ratio (UNTESTED; Genjutsu merged and re-ordered shots on strobe
    edits in one past run).
- **Output**
  - Real time at 24 fps.
  - Historical 1080p outputs included 1664×1248 and 1248×1664; probe the actual result rather than assume either geometry. The take's frame count need not equal the padded input's: never assume 96 out for 96 in.
  - Map frames back with `gen_index = round(padded_index × gen_frames / padded_frames)` for the kept
    (unpadded) input frames: `frames.py map --gen-clip <take> --pad-json <pad json>` prints them.
  - Inspect text, invented logos/watermarks and camera motion; remove invented marks and compose planned text as separate overlays.
  - **Fit the output to the planned frame.** Keep the intended subject scale, position and visible borders, using the recorded reversible input mapping and measured per-shot geometry. Never apply a fixed crop centre such as 0.35 or cut off the hero merely to fill the canvas; choose another planned route or report the unresolved geometry limit if the take cannot fill its frame.
  - A portrait take going to a landscape canvas is a soft 1.54× upscale. Prefer correctly framed source material and measured code composition; never offer a paid-reframe choice or introduce a new approval gate (`budget.md` §1).
- **Count**: the planned take(s), at final settings.
  - The internal plan contains the necessary initial take and bounded corrective retry reserve. Price a possible retry at the full affected job length; never present optional-take menus.
  - For strobe or 1–3-frame-cut references, drive short cuts per cut and assemble them in code. Historical two-take projects are not a reason to generate duplicate full videos automatically.
  - Re-roll a part only when it fails a fail-list check, once, as the same job (`budget.md` §3 rung 5).
    "A better take" is not a failure. A past project's blanket 2-takes-per-part rule doubled spend.
- **Prompt**: let the prepared image carry the intended appearance and scene; let the driving video carry motion and timing. Use one short sentence, at most two and at most 40 words.
  ```
  Animate @Image1 with the source video's motion and camera movement, preserving the image's identity and appearance.
  ```
- **Historical observation, not a prompt rule:** earlier weak input images produced texture/colour drift and long prose was tried. Do not repeat that workflow. Improve the prepared two-reference image within the existing plan and verify the output instead of describing every object, costume, texture or camera beat in the Genjutsu prompt.
- For a verified preset with sufficient selected style and media, omit the prompt or pass an empty string only when its actual contract permits it. Otherwise name the desired operation and one preservation clause briefly. Do not append generic negative lists or a full scene reconstruction.
- **QA every take**
  - Identity on the wrong person, or a role swap.
  - Invented logos. A Nike-like swoosh appeared despite "no logos".
  - A hallucinated reference object in the first ~0.5 s (a plaster car wheel).
  - Wardrobe drift away from the clothing in the user's photo.
  - Duplicate-frame judder.
  - Shots re-ordered or merged on strobe edits: cast them by content.
  - ±1–2 f cut drift: nudge the in-point by 1 frame.

## G11. Mattes: `remove_background`, `sam_3_video` and local masks

Order mattes only after the EDL exists, and only for clips the EDL uses with contour, cut-outs,
behind-subject text or matte-limited grades.

| Model                                          | Call                                                                                                                                       | Output                                                                                                                        | Price                                                           | Use when                                                              |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------- |
| `remove_background` (video_background_remover) | MCP `remove_background` `{"params": {"media_id": "<job or media id>", "media_type": "video"}}` (mcp-api §9.1)                              | H.264 **person on black, no alpha**, same size and fps as the source. Keeps only the main subject: a past plate's friend was dropped | 1 cr flat (VERIFIED live 2026-10-08 on a 10 s 720p plate)       | High-key or white-cyc plates (past runs)                              |
| `sam_3_video`                                  | Segmentation through `generate_video` with `model: sam_3_video`, `apply_mask: false`, one `video` (mcp-api §9.2); verify the live contract | Binary source-aligned mask; not newly generated creative footage                                                              | Live-price before use; historical ~1.14 cr is not authorization | Dark clothing, hair, multiple subjects or held props                  |
| Local mask / existing mask asset               | Existing compositor or authorized local segmentation                                                                                       | Binary mask aligned to the source frame grid                                                                                  | No new video-generation call                                    | Dark clothing, multiple subjects or held props needing a precise mask |

- **Alpha recipes** (`matte.py`):
  - Division, white-cyc tuned (past runs):
    `blend=all_expr='if(lt(B,34),if(gt(A,10),255,0),clip((A*255/B-70)*1.9,0,255))'` with matte as A and
    original as B, both gray.
  - Threshold: `clip((max(RGB)-8)/10)` (one past run).
  - Close holes with dilate/erode ×8 and a slight blur.
- **Gotchas**
  - `color=…:r=<plate fps>` must match the plate fps (the default is 25).
  - Use `alphamerge=shortest=1`.
  - SAM grabs rails and mics: clamp it to an x-range around the hero. It misses held props: union with a
    difference key.
  - Check matte edges at 100% on white backdrops.
  - One `remove_background` call failed (a past run's c0) and the retry worked. Check the jobs before retrying.
- **Local keys and cut-outs (optional):** `assets.py key` (chroma backgrounds, with despill), `assets.py cut`
  (white backgrounds) and `assets.py grid` (sheets) prepare stills, frame folders or videos locally; `--help`
  for options. A subject meant only for compositing can be generated on a flat key colour it does not contain.

## G12. Chant, vocal and VO

- **No sung-vocal model exists.** `sonilo_music` is "game pipeline only" and must not be used for
  standalone audio; `mirelo_text_to_audio` generates sound effects only.
- **Default soundtrack**
  - Follow the authored audio plan and locks, using actual source/user/stock recordings
    (`creative-quality.md`). Preserve
    a locked track; no fixed house music, code-synthesized music/SFX or invented delivered stock file.
  - If a required source/stock operation is unavailable, use accessible suitable authorized audio or
    report the actual limitation. Never claim a replacement matches locked source audio when it does not.
- **Chant, `seed_audio`** for planned speech, using an
  existing noninteractive permitted voice selection; otherwise preserve suitable source vocals
  (a SHAPE like every params block here; mcp-api §10):
  ```json
  {
    "model": "<from plan line: seed_audio>",
    "prompt": "<the whole chant, one take>",
    "voice_type": "preset",
    "voice_id": "<existing user-selected voice_id>",
    "format": "wav",
    "sample_rate": 48000,
    "pitch_rate": 2
  }
  ```
  - Use the authored words and the already selected voice pair; never import historical voice IDs or example lyrics.
  - Match planned prosody; punctuation is a conditional tool, never a default cute delivery.
  - Put the whole chant in one take so it can be sliced per word.
- **Price and count**
  - 0.3–2 cr per take.
  - Use one existing user-selected voice pair. Never invoke `list_voices` when it opens a human picker, invent an ID or copy an example voice. If no selected pair is available, preserve source audio or report that replacement speech cannot be produced without the required selection.
- **Slicing**
  - Cut words by energy envelope or spectrogram, **not by Whisper**: its word starts were about 0.27 s
    late on TTS.
  - Historical +2-semitone chain, only when the requested source-matched vocal correction actually needs
    this measured shift; never pitch-shift the reference soundtrack by default:
    `atrim,asetpts=N/SR/TB,pan=mono|c0=0.5*c0+0.5*c1,asetrate=48000*1.12246,aresample=48000,atempo=0.89090,highpass=f=140`
  - Place each word on the beat in code.
- **VO with ElevenLabs v4**
  - When the user says "v4", the model is exactly `elevenlabs_v4` (`dialogue` + `stability` +
    `similarity_boost`; `prompt` is required and duplicates the text). It costs about 0.23 cr per 30
    characters.
  - Put audio tags after the first sentence. A leading tag made v4 repeat it.
  - One past project's generated epic VO direction was rejected by the client in favour of the reference's own
    audio.

## G13. Texture plates

- Use the selected reference texture grammar (grain, paper, dust, halation or glitch)
  with authored intervals and intensity recorded in its layer plan (`compositing.md`).
  Existing source texture may be retained when the requested scope permits it.
- One past run used `gpt_image_2_5` for a paper texture: 2 jobs, 1 used, 2.75 cr each as observed (Sunburst
  estimates are unreliable).
- For a new GPT texture plate use Sunburst (`gpt_image_2_6`). Set the line's quality and
  resolution explicitly. Get the exact one-job estimate for those settings and record it
  with `price-set` before submitting (budget.md §8).

## G14. Cheap motion previews (prices VERIFIED live; preview fidelity UNTESTED)

- **Seedance draft** (VERIFIED live 2026-10-08 unless marked)
  - Seedance 2.5 `draft: true` always bills at the 480p rate, 3 cr/s: a 4 s draft was charged 12. Its
    output is **752×560** for 4:3, 24 fps: a blocking preview, never footage.
  - It can be finalized within 7 days via `draft_job_id`. The `get_cost` preflight on the finalize returns the **full
    1080p price** (4 s → 48). The finalize is **always 1080p**: a `720p` resolution param is ignored.
    Without `duration` it prices 5 s (60), so always pass the draft's own duration.
  - So draft + finalize = 12 + 48 = 60 for a 4 s clip, **1.25× a direct 1080p job** (48) and 2.1× a
    direct 720p job (28). It never pays on a 720p plan.
  - It pays on a 1080p plan only when more than about 20–25% of direct takes would be rejected
    (break-even: 12 ÷ (1 − r) + 48 = 48 ÷ (1 − r) gives r = 25%; 20% if the rejected drafts' own 12 cr
    are ignored). Use it only if already explicitly requested and included in the finite plan: whether the finalized clip keeps
    the draft's motion and framing is unverified (no finalize job has run).
- Drafts use only `seedance_2_5`; no cheaper alternate video model is allowed. Use a draft only for an already justified planned composition check, never as final footage.

---

## 1. Prompt ownership and clean layers

The task contract and explicit locks govern creative ownership. Preserve the intended identity, the
clothing from the user's photo and the selected visual grammar while deriving new scenes and wording
from the creative plan.
Historical examples never supply missing content. Do not add a generic cinematic style, remove locked
glasses or change a planned gesture merely because a prior project preferred it.

Put format, duration and resolution in verified parameters. Every clean intermediate has a concrete
final-layer plan: compose the authored text/graphics and preserve locked/reused source layers. Never
erase a requested element from delivery. Prompt timecodes are approximate guidance; inspect actual
returned footage and align to the output timeline.

## 2. Rejections and permitted recovery

Follow provider restrictions. Do not disguise a restricted identity or costume, remove input evidence, rename prohibited content, or route the same refused request through another model to defeat moderation. Correct a genuine technical input error or use a clearly supported alternative that fulfills the actual request. If a planned shot cannot be produced, cover its role with allowed material or another permitted route inside the plan where possible and report the specific unresolved difference without a question.

Historical refunds are not a guarantee. Reconcile each job debit and refund against transactions. The debit remains part of spend until its refund is verified. A failed request with unknown billing never authorizes a replacement charge automatically.

Image models can return `nsfw` for harmless prompts. Word poses, clothing and objects unambiguously from the
start; after a flag, the refusal rules above apply.

## 3. Fidelity gate

Compare every candidate against its output role, ownership and explicit locks. Check story/visual-motif
continuity, the selected reference grammar and that the hero wears the clothing from the user's photo
(or the outfit the user asked for).
Reject identity/anatomy errors and unintended drift, not deliberate source traits or permitted authored
changes. Choose internally, log defects and use only bounded corrections in the priced plan. No taste
question or external creative approval gate.

## 4. Known failure modes and fixes

Compare against the authored shot contract and explicit locks. Historical incidents do
not introduce a fixed cast, soundtrack, pose or style, nor make Genjutsu the default generation route.

| Symptom                                                             | Model                                      | Cause or trigger                                                                  | Fix                                                                                                                                                                                                                                                                                                                       | Source                                                            |
| ------------------------------------------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `nsfw` on 4/4 jobs                                                  | Seedance                                   | Audio ref + `generate_audio:true`, plus suggestive wording                        | Preserve source audio; comply with the rejection and use §2 recovery                                                                                                                                                                                                                                                      | 1 past run                                                        |
| `nsfw` on 5/6 clips                                                 | Seedance, NB still                         | Copyrighted costume (Spider-suit)                                                 | Preserve permitted source material or report the unresolved change; do not disguise the refused costume                                                                                                                                                                                                                   | /test-edit                                                        |
| HTTP 422, no body, or input rejected                                | MT                                         | Input under ~4 s                                                                  | Export at 24 fps, then ping-pong pad to 96 f (G10)                                                                                                                                                                                                                                                                        | 2 past runs                                                       |
| Output truncated, or extended with invented shots                   | Genjutsu                                   | Input not a whole number of seconds                                               | Freeze-pad to ceil(seconds); an MT part with a fractional second ≤ 0.1 s may stay unpadded (G10); map frames proportionally                                                                                                                                                                                               | 2 past runs                                                       |
| Driving clip bills 1.25–2.5× more; motion slowed                    | Genjutsu                                   | A 25/30/50/60 fps cut padded at 24 fps as-is                                      | `frames.py export --fps 24` before `pad`; price from the probed frame count                                                                                                                                                                                                                                               | Local frames.py test (cost review); a past run exported 24p first |
| Background pulled from the photo (stage, giant letters)             | MT                                         | Bare photo as the image                                                           | Reuse a suitable source-aligned image, or prepare G5 only when needed                                                                                                                                                                                                                                                     | 1 past run (cut c03)                                              |
| Dark, textureless objects; colours lost                             | MT                                         | Depth-mask driven; thin prompt                                                    | Improve the prepared reference image and verify colours; keep the Genjutsu prompt short (G10)                                                                                                                                                                                                                             | 2 past runs                                                       |
| Garbled copies of reference captions or graphics                    | MT                                         | Burned text in the driving video; long parts                                      | Drive shorter parts cut at the reference's own cuts and keep burned text out of the driving input where the performance allows; compose planned wording as an overlay (G10)                                                                                                                                               | 2 past runs                                                       |
| Invented swoosh or stripes                                          | MT                                         | — ("no logos" does not stop it)                                                   | Remove only newly invented marks; use a bounded retry only for a measured unresolved defect                                                                                                                                                                                                                               | 1 past run (take t3)                                              |
| Second performer becomes a faceless mannequin, or roles swap        | MT                                         | Two performers                                                                    | Use a minimal target-position cue; check roles on every take (G10 QA)                                                                                                                                                                                                                                                     | 2 past runs                                                       |
| A plaster car wheel in the first ~0.5 s                             | MT                                         | Reference object hallucinated at the take start                                   | Use a later in-point only if all required source motion still aligns; otherwise correct within the bounded plan                                                                                                                                                                                                           | 1 past run                                                        |
| Shots re-ordered or merged                                          | MT                                         | Strobe or 1-frame cuts                                                            | Drive short cuts per cut, cast takes by content and assemble the planned order in code; report any missing beat                                                                                                                                                                                                           | 1 past run                                                        |
| Wardrobe drift (boots for sneakers)                                 | MT                                         | Wardrobe not spelled out                                                          | Prepare the clothing from the user's photo in the input image; use one short preservation clause                                                                                                                                                                                                                          | 1 past run (v4→v5)                                                |
| Gestures arrive 1.5–2.7× late (or, in another plate, right on time) | Seedance                                   | Timecodes are ordering hints; adherence varies per plate                          | Slots of 2× the needed seconds (G7 duration rule); critical beats early; in-points from the sheet, never from timecodes                                                                                                                                                                                                   | 1 past run (late); 2026-10-08 live-test run (on time)             |
| Coy grin instead of a cool stare                                    | Seedance                                   | "barely visible smirk"                                                            | Correct the generated expression through the permitted generation route within the reserve; never warp or repaint the face in code                                                                                                                                                                                        | 1 past run (f2b)                                                  |
| Black blob or white bar under a threshold                           | Seedance                                   | Backlit silhouette, specular glint, prop into the lens, worm's-eye                | Avoid them under a threshold look unless the plan needs one; repair introduced defects with the tonal treatment in compositing                                                                                                                                                                                            | 1 past run (f3b, f4, f1)                                          |
| Face crushed to near-black on identity-legible medium close-ups     | Seedance + code xerox                      | The full-strength threshold, where the reference keeps facial detail              | If the compositor caused it, correct the whole-shot grade; no face-only mask, retouch or repaint. A generated facial defect needs a permitted generation correction                                                                                                                                                       | 2026-10-08 live-test run (VERIFIED live)                          |
| A past project's wardrobe or props in a new user's plate            | any prompt                                 | VERBATIM example copied with its identity items                                   | Copy the structure only; leak check (§5 #10)                                                                                                                                                                                                                                                                              | Dry-run eval, 2026-10-08                                          |
| A second person cropped away or dropped by the matte                | Seedance + face-lock / `remove_background` | Extra identity in a face-locked plate                                             | Restore every planned performer via an appropriate full-cast plate or separate preserved layers (G7)                                                                                                                                                                                                                      | 1 past run (friend)                                               |
| Garbled lettering on waistbands                                     | Seedance                                   | —                                                                                 | Remove only invented marks; garbled lettering on a garment from the user's photo is a wardrobe fail-list item                                                                                                                                                                                                             | 1 past run                                                        |
| A different man across shots                                        | Seedance                                   | Sheet only (face widens); glasses; mixing a real close-up with generated identity | Sheet + real face frame; preserve reference glasses; one identity source per sequence                                                                                                                                                                                                                                     | 1 past run (v1/v3)                                                |
| Wrong coat colour                                                   | gpt_image_2                                | —                                                                                 | Seedream i2i (G3)                                                                                                                                                                                                                                                                                                         | 1 past run                                                        |
| Phone camera-UI overlay                                             | Soul 2.0                                   | —                                                                                 | Reject; pick another variant                                                                                                                                                                                                                                                                                              | 1 past run (friend #8)                                            |
| Bipedal "wolf", photoreal "anime", grey background                  | soul_cast                                  | Photoreal-humanoid prior                                                          | gpt_image_2_6_flare (nano_banana_2_1 as the cheaper fallback, stills.md §6)                                                                                                                                                                                                                                                    | An older note                                                     |
| Stickers look small                                                 | Seedream transparent background                         | Large transparent margins                                                         | Crop to the alpha bbox +6 px                                                                                                                                                                                                                                                                                              | 1 past run                                                        |
| Holes in dark clothing or hair                                      | remove_background                          | Person-on-black alpha is ambiguous on dark                                        | Use `sam_3_video` or a local/existing binary mask; validate one clip first                                                                                                                                                                                                                                                | /test-edit, 1 past run                                            |
| Matte grabs rails or mics; misses held props                        | sam_3_video                                | —                                                                                 | Clamp the x-range; union with a difference key                                                                                                                                                                                                                                                                            | 2 past runs                                                       |
| Whisper word times ~0.27 s late                                     | faster_whisper on TTS                      | —                                                                                 | Slice by energy envelope                                                                                                                                                                                                                                                                                                  | 1 past run                                                        |
| v4 repeats the opening audio tag                                    | elevenlabs_v4                              | Leading tag                                                                       | Tags after the first sentence                                                                                                                                                                                                                                                                                             | A past project journal                                            |
| A plate arrives after planning started and is never used (180 cr)   | any                                        | Cataloguing and EDL work before `jobs_wait` finished                              | Between polls only reference-side work; no catalogue, in-points or EDL until every paid job is terminal; a late job is catalogued and the EDL reviewed before rendering                                                                                                                                                   | 1 past run (f3a)                                                  |
| Double charge risk                                                  | any                                        | Resubmitting after a transport timeout                                            | Check jobs first; never auto-resubmit                                                                                                                                                                                                                                                                                     | MCP tool doc                                                      |

## 5. Pre-submit checklist (every paid call)

1. Complete the native-frame inspection and per-second log required by `analysis.md`. The task
   contract records locks and freedoms and the creative plan supplies output target/roles/evidence. The
   job traces to an output shot and relevant source evidence.
   Its route is in `plan/routes.json` and fits the finite priced plan authorized by task/account rules:
   its inputs exist (no placeholder left), every upstream input is a completed ledger job, and a current
   `get_cost` preflight for its settings fits the unchanged cap.
   `ledger.py guard $W --line <ID>` passes (a re-roll adds `--reroll-of <job> --reason
   <fail-list item>`).
2. For direct Genjutsu or a Genjutsu preset, keep the prompt to one short sentence (at most two, at most 40 words), or empty only where the preset contract permits it. Check the execution-contract model allowlist on this exact request or batch item: fresh video is `seedance_2_5`; only justified Genjutsu motion transfer or a verified preset/Styles route are exceptions. Segmentation and post-production utilities are allowed exceptions, not creative video engines. Image preparation remains on image models. Supply only fields supported by that exact live operation: applicable model, mode, resolution, duration and aspect values come from the plan. Direct Genjutsu follows the source input and does not receive unsupported mode/duration/aspect fields. Every Seedance call
   has `generate_audio:false` and `bitrate_mode:"high"`, stated on its plan line too (header). None of
   them appear in the prompt.
3. Media are media_ids or job_ids. Roles are the schema keys (Genjutsu: `image` +
   exactly one `video`). G4/G5 use the S1 two-reference frame/identity baseline until a keyframe is accepted,
   then the S3 keyframe-first set of stills.md §3. Other necessary
   scene/asset combinations use the smallest sufficient set within verified limits, with each
   input's ownership recorded. MT/Seedance preparation is conditional, never an automatic extra job.
4. The prompt fulfills the output role, explicit locks and assigned reference ownership, implements
   the authored scene and selected visual grammar, and states that the hero wears the clothing from the
   user's photo (unless the user asked for another outfit). Intermediate clean layers have a final
   compositing plan and §2 restrictions are followed. Its `get_cost` preflight returned a price.
5. Genjutsu input: prepared according to the verified live contract and G10. Input is retimed to 24 fps before padding
   (exactly 96 f for cuts under 4 s). Its probed duration is the intended whole number of seconds, and
   the line was priced from the probed frame count.
6. `count: 1`; no character or voice picker.
7. This is its family's canary (a planned job covering the family's hardest fidelity constraints, submitted individually), or its family's canary has passed. Never collect separate reservations into one batch submit.
8. Log the job id, params, quoted credits and purpose in `plan/ledger.json` at submit time
   (`ledger.py add $W --line <ID> --job <job_id>`).
9. Every supported request field equals the plan line, including model and any applicable mode, resolution and billed seconds. Do not inject unsupported fields into Genjutsu. `ledger.py params $W
   --line <ID>` prints the skeleton, and `--check '<params json>'` compares (exit 1 = mismatch). A
   mismatch is unplanned spend: stop and fix the params or the plan, and re-quote if the plan changes.
10. Leak check: no garment, prop, colour, place or gesture in the prompt comes from a cookbook example
    instead of the user's photo, explicit request, current source evidence or authored creative plan, and
    no garment comes from the reference performer (header rule; a past hero's micro shorts, green lipstick
    and cross thigh-highs leaked into another user's plates in a dry-run eval).
11. Every planned performer and layer survives tracking/cropping/matting. Intended identity and
    clothing are checked across all output appearances, including back views, silhouettes, helmets,
    hands, crops and occlusions. A hidden-face appearance of the hero cannot silently become KEEP or
    reveal a face solely to prove identity.
    Full regeneration covers every required output shot. Reuse suitable images; G4/G8 and reusable
    hero/prop assets are conditional; the location-plate stage (Soul Cinema for a photoreal look, a stylised flare plate otherwise) is required for generated scenes. Clean intermediates have an explicit final
    layer plan; generic studio/crop defaults cannot overwrite explicit locks or the planned scene design.
12. No face was generated, replaced, deformed, retouched, repainted or locally relit by code. Identity
    changes and facial corrections trace to the authorized model job; tracking and whole-layer
    composition preserve that result's facial geometry and appearance.
