# YouTube Shorts Extraction Agent — Initial Plan

## Goal

Extend the existing `youtube_shorts_agent` (`src/agents/youtube_shorts_agent/workflow.py`) so that, instead of just generating idea text from a topic string, it takes a real YouTube video and automatically pulls out a short (<1 min) clip — audio + video — built around the "hook"/most engaging moment of the source content.

## Pipeline

1. **Parse node (LangGraph + OpenAI)** — reuses `youtube_shorts_agent` as the base. User input is a single free-form string containing both the YouTube link and natural-language instructions (e.g. desired tone/focus for the short). This node sends that raw string to the LLM and parses the response into a structured JSON model — at minimum `{ "link": ..., "instructions": ... }`, plus any other fields the LLM extracts. This becomes the graph's entry node, replacing the current `ideas_node`/`build_workflow()` (topic → static idea list).
2. **Download tool** — connects to the internet, downloads the YouTube video, and denies/rejects source videos longer than **5 minutes**.
3. **Transcription** — extract audio from the downloaded video and transcribe it to text via the OpenAI Whisper API.
4. **Hook detection** — analyze the transcript (and/or video) to identify timestamp ranges worth turning into a Short.
5. **Clip assembly** — cut and join the video + audio for the selected timestamp range(s) into a final output clip **under 1 minute**.

## Open questions

- **Parsed JSON schema**: beyond `link` and `instructions`, which other fields should the parse node extract (e.g. desired style/tone, target duration override)? Needs a concrete schema (e.g. a Pydantic/TypedDict model) so downstream nodes can rely on fixed keys.
- **Hook detection method**: not yet specified — likely an LLM pass over the transcript (e.g. asking it to find the most quotable/engaging span and return timestamps), but could also involve audio/scene-based signals. Needs a decision before step 4 can be designed.
- **Download tool**: which library — `yt-dlp` is the common choice, but not yet decided. Also need to confirm legal/ToS considerations for downloading YouTube content.
- **Video cut/join tool**: likely `ffmpeg`, not yet decided.
- **Output**: where the final clip gets written/returned (local file path? uploaded somewhere?) is not yet defined.

## Fit with existing architecture

- Builds on `src/agents/youtube_shorts_agent/` rather than a new agent package — `get_agent()`/registration in `registry.py` stay as-is, but `agent_state.py` (`YoutubeShortsState`) and `build_workflow()` need new fields (video URL, transcript, hook timestamps, output path) and new graph nodes (download, transcribe, hook-detect, cut/join) replacing the current single `ideas` node.
- New nodes get wired into the LangGraph graph, likely via the `simple_react_agent` tool-binding pattern in `src/agents/prebuilt/` once that module's `Agent` contract mismatch is fixed (see note in CLAUDE.md).
- Whisper transcription and any LLM hook-detection step go through `src/utils/models.get_model`, consistent with how the rest of the codebase constructs LLM clients.
