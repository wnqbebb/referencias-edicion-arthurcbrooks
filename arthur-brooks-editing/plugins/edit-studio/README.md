# Edit Studio

A plugin of three connected skills for editing video in code (Python + ffmpeg in Claude's sandbox).

| Skill | What it does |
|---|---|
| edit-director | The brain and the engine: music edits in a style named in plain words (with fresh versions), composite edits (talk clip + music edit), remakes from a reference, named effects measured from example clips, the move and genre library, labelled previews, self-checks, point edits by command |
| edit-voice | Speech: transcription with word timecodes, cuts by spoken phrases, captions and karaoke subtitles, vertical cut-downs from long videos, translation and voiceover |
| edit-gen | Generation with Higgsfield, from missing shots to a whole video storyboarded to the track (only with explicit consent to spend credits) |

The engine lives only in edit-director (`engine/`); the other skills call it from there.
Paid Higgsfield actions run only after the user's explicit "yes".

Licenses: models — `skills/edit-director/engine/models/LICENSES.md`, fonts — SIL OFL 1.1
(`engine/assets/fonts/*_OFL.txt`), third-party code — `skills/edit-director/NOTICE.md`.
