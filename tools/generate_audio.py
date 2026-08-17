#!/usr/bin/env python3
"""Render a session script to a guided-audio recording.

The script in `script/*.md` is the single source of truth. Everything between
the `<!-- narration:start -->` and `<!-- narration:end -->` markers is spoken,
except headings and blockquoted delivery notes. A line of the form `[pause N]`
becomes N seconds of silence.

Two engines are supported:

  elevenlabs  (default) neural voices via the ElevenLabs API. Needs
              ELEVENLABS_API_KEY in the environment and outbound access to
              api.elevenlabs.io.
  piper       fully offline neural TTS. Needs `pip install piper-tts` and a
              downloaded voice (see tools/fetch_piper_voice.sh).

Examples
--------
    export ELEVENLABS_API_KEY=...
    python3 tools/generate_audio.py script/arm-heaviness.md -o audio/arm-heaviness.mp3

    python3 tools/generate_audio.py script/arm-heaviness.md \
        --engine piper --piper-model voices/en-us-lessac-medium.onnx \
        -o audio/arm-heaviness.mp3
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import wave
from pathlib import Path

NARRATION_START = "<!-- narration:start -->"
NARRATION_END = "<!-- narration:end -->"
PAUSE_RE = re.compile(r"^\[pause\s+([0-9]+(?:\.[0-9]+)?)\]$", re.IGNORECASE)
# A line tagged `<!-- safety -->` carries clinical/safety framing rather than
# the exercise itself, so it can be dropped with --no-safety.
SAFETY_RE = re.compile(r"<!--\s*safety\s*-->")
# A script may carry its own render settings, e.g.
#   <!-- render: --speed 1.0 --stretch 1.0 -->
# An explainer needs normal delivery; a relaxation session does not. Keeping
# that with the script stops it being lost on the next re-render.
RENDER_RE = re.compile(r"<!--\s*render:(.*?)-->", re.DOTALL)
# `[stretch 1.0]` changes the time-stretch for everything after it. Stretch is
# applied after the cache, so varying it mid-script costs no API calls. Used to
# let the cancellation wake the listener up rather than drifting on at
# induction pace.
STRETCH_RE = re.compile(r"^\[stretch\s+([0-9]*\.?[0-9]+)\]$", re.IGNORECASE)
# `[speed 1.1]` re-synthesises everything after it at a different rate. Unlike
# [stretch] this costs API calls, but the model does the work, so there are no
# resampling artefacts — which matters on a low voice.
SPEED_RE = re.compile(r"^\[speed\s+([0-9]*\.?[0-9]+)\]$", re.IGNORECASE)


def script_render_args(path: Path) -> list[str]:
    """Return CLI args declared inside the script, if any."""
    import shlex

    m = RENDER_RE.search(path.read_text(encoding="utf-8"))
    return shlex.split(m.group(1)) if m else []

# ElevenLabs defaults. Chosen by measurement, not by name: across an
# instructional line and a formula, this voice sits at 104-112 Hz with a 9 Hz
# swing between the two, against 206/190 Hz and a 16 Hz swing for Charlotte,
# which read as animated. Its natural rate on a formula is already 127 wpm.
DEFAULT_VOICE_ID = "Dj7pgiuloVNRtSboSnjm"   # Meditative Narrator
DEFAULT_MODEL_ID = "eleven_multilingual_v2"
EL_SAMPLE_RATE = 24000  # pcm_24000


# --------------------------------------------------------------------------
# script parsing
# --------------------------------------------------------------------------

def parse_script(path: Path, omit_safety: bool = False
                 ) -> list[tuple[str, object]]:
    """Return a list of ("speak", text) and ("pause", seconds) segments."""
    text = path.read_text(encoding="utf-8")
    if NARRATION_START not in text or NARRATION_END not in text:
        raise SystemExit(
            f"{path}: missing {NARRATION_START} / {NARRATION_END} markers"
        )
    body = text.split(NARRATION_START, 1)[1].split(NARRATION_END, 1)[0]

    segments: list[tuple[str, object]] = []
    buffer: list[str] = []

    def flush() -> None:
        if buffer:
            spoken = " ".join(" ".join(buffer).split())
            if spoken:
                segments.append(("speak", spoken))
            buffer.clear()

    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            flush()
            continue
        if line.startswith("#") or line.startswith(">"):
            flush()  # heading or delivery note: structural, never spoken
            continue
        m = PAUSE_RE.match(line)
        if m:
            flush()
            segments.append(("pause", float(m.group(1))))
            continue
        m = STRETCH_RE.match(line)
        if m:
            flush()
            segments.append(("stretch", float(m.group(1))))
            continue
        m = SPEED_RE.match(line)
        if m:
            flush()
            segments.append(("speed", float(m.group(1))))
            continue
        if SAFETY_RE.search(line):
            if omit_safety:
                continue
            line = SAFETY_RE.sub("", line).strip()
        buffer.append(line)
    flush()
    return segments


# --------------------------------------------------------------------------
# engines — each returns raw mono s16le PCM at its own sample rate
# --------------------------------------------------------------------------

class ElevenLabsEngine:
    name = "elevenlabs"
    sample_rate = EL_SAMPLE_RATE

    def __init__(self, voice_id: str, model_id: str, stability: float,
                 similarity: float, speed: float) -> None:
        import requests  # imported lazily so the piper path needs no network deps

        self.requests = requests
        self.api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not self.api_key:
            raise SystemExit(
                "ELEVENLABS_API_KEY is not set.\n"
                "  export ELEVENLABS_API_KEY=sk_...\n"
                "Never commit the key — pass it through the environment."
            )
        self.voice_id = voice_id
        self.model_id = model_id
        self.voice_settings = {
            "stability": stability,
            "similarity_boost": similarity,
            "style": 0.0,
            "use_speaker_boost": False,
            "speed": speed,
        }
        self.url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            f"?output_format=pcm_{EL_SAMPLE_RATE}"
        )

    def cache_key(self, text: str, prev: str, nxt: str) -> str:
        blob = json.dumps(
            [self.name, self.voice_id, self.model_id, self.voice_settings,
             text, prev],
            sort_keys=True,
        )
        return hashlib.sha256(blob.encode()).hexdigest()[:20]

    def synthesize(self, text: str, prev: str = "", nxt: str = "") -> bytes:
        payload = {
            "text": text,
            "model_id": self.model_id,
            "voice_settings": self.voice_settings,
        }
        # previous_text carries voice character across the join. next_text is
        # deliberately NOT sent: it makes the model lean into a phrase that is
        # actually seconds of silence away, so the segment ends mid-decay at
        # full amplitude and clicks when silence is appended.
        if prev:
            payload["previous_text"] = prev

        last_error = None
        for attempt in range(5):
            try:
                r = self.requests.post(
                    self.url,
                    headers={"xi-api-key": self.api_key,
                             "Content-Type": "application/json"},
                    json=payload,
                    timeout=180,
                )
            except Exception as exc:  # transport error: retry
                last_error = exc
            else:
                if r.status_code == 200:
                    return r.content
                if r.status_code in (429, 500, 502, 503, 504):
                    last_error = f"HTTP {r.status_code}: {r.text[:300]}"
                else:
                    raise SystemExit(
                        f"ElevenLabs returned HTTP {r.status_code}: {r.text[:500]}"
                    )
            time.sleep(2 ** attempt)
        raise SystemExit(f"ElevenLabs request failed after retries: {last_error}")


class PiperEngine:
    name = "piper"

    def __init__(self, model_path: str, length_scale: float) -> None:
        from piper import PiperVoice, SynthesisConfig

        model = Path(model_path)
        if not model.exists():
            raise SystemExit(
                f"piper model not found: {model}\n"
                "Run tools/fetch_piper_voice.sh to download one."
            )
        config = model.with_suffix(model.suffix + ".json")
        self.voice = PiperVoice.load(
            str(model),
            config_path=str(config) if config.exists() else None,
        )
        # length_scale > 1 slows delivery, which suits a relaxation script.
        self.syn_config = SynthesisConfig(length_scale=length_scale)
        self.length_scale = length_scale
        self.model_path = str(model)
        self.sample_rate = self.voice.config.sample_rate

    def cache_key(self, text: str, prev: str = "", nxt: str = "") -> str:
        blob = json.dumps(
            [self.name, self.model_path, self.length_scale, text],
            sort_keys=True,
        )
        return hashlib.sha256(blob.encode()).hexdigest()[:20]

    def synthesize(self, text: str, prev: str = "", nxt: str = "") -> bytes:
        out = io.BytesIO()
        for chunk in self.voice.synthesize(text, syn_config=self.syn_config):
            out.write(chunk.audio_int16_bytes)
        return out.getvalue()


# --------------------------------------------------------------------------
# assembly
# --------------------------------------------------------------------------

def trim_and_fade(pcm: bytes, rate: int, fade_in_ms: float = 10.0,
                  fade_out_ms: float = 30.0, threshold: float = 120.0,
                  keep_tail: float = 0.05) -> bytes:
    """Strip a segment's own leading/trailing silence and fade its edges.

    Two reasons. The engine pads each segment unpredictably (up to 1.15s here),
    which silently lengthens every scripted pause; and a segment that ends at
    non-zero amplitude clicks when digital silence follows it.
    """
    import numpy as np

    a = np.frombuffer(pcm, dtype=np.int16).astype(np.float32)
    if a.size == 0:
        return pcm
    win = max(1, rate // 100)
    n = a.size // win
    if n == 0:
        return pcm
    rms = np.sqrt((a[:n * win].reshape(n, win) ** 2).mean(axis=1))
    voiced = np.flatnonzero(rms > threshold)
    if voiced.size == 0:
        return b""
    a = a[voiced[0] * win:
          min(a.size, (voiced[-1] + 1) * win + int(keep_tail * rate))].copy()

    fi, fo = int(rate * fade_in_ms / 1000), int(rate * fade_out_ms / 1000)
    if a.size > fi + fo:
        a[:fi] *= np.linspace(0.0, 1.0, fi, dtype=np.float32)
        a[-fo:] *= np.linspace(1.0, 0.0, fo, dtype=np.float32)
    return a.astype(np.int16).tobytes()


def stretch_pcm(pcm: bytes, rate: int, factor: float) -> bytes:
    """Slow speech without shifting pitch, via ffmpeg's atempo filter.

    Applied per segment, never to the assembled timeline, so the inserted
    silences keep their exact scripted lengths.
    """
    if abs(factor - 1.0) < 1e-3:
        return pcm
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error",
           "-f", "s16le", "-ar", str(rate), "-ac", "1", "-i", "pipe:0",
           "-filter:a", f"atempo={factor}",
           "-f", "s16le", "-ar", str(rate), "-ac", "1", "pipe:1"]
    r = subprocess.run(cmd, input=pcm, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    if r.returncode != 0:
        raise SystemExit(f"atempo failed: {r.stderr.decode()[:300]}")
    return r.stdout


def ffmpeg_exe() -> str:
    exe = os.environ.get("FFMPEG_BINARY")
    if exe:
        return exe
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def encode_mp3(wav_path: Path, mp3_path: Path, bitrate: str,
               lufs: float | None, sample_rate: int) -> None:
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(wav_path)]
    if lufs is not None:
        # Guided-relaxation audio is listened to quietly and often in the dark;
        # normalise to a calm target with headroom rather than mastering hot.
        cmd += ["-af", f"loudnorm=I={lufs}:TP=-2.0:LRA=7"]
    # loudnorm resamples to 192 kHz internally; pin the output back to the
    # source rate so the encoder is not spending bits on empty spectrum.
    cmd += ["-codec:a", "libmp3lame", "-b:a", bitrate, "-ac", "1",
            "-ar", str(sample_rate), str(mp3_path)]
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        raise SystemExit(
            "ffmpeg not found. Either `pip install imageio-ffmpeg`, install "
            "ffmpeg, or pass --format wav."
        )


def build(segments, engine, out_path: Path, cache_dir: Path, bitrate: str,
          fmt: str, lead_in: float, tail: float, lufs: float | None,
          stretch: float, trim: bool, timings: Path | None = None) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    rate = engine.sample_rate
    pcm = bytearray()

    def silence(seconds: float) -> bytes:
        return b"\x00\x00" * int(round(seconds * rate))

    speech = [s for s in segments if s[0] == "speak"]
    cur_stretch = stretch
    marks = []                       # start/end of every spoken line, for video
    spoken_texts = [s[1] for s in segments if s[0] == "speak"]
    done = 0
    pcm += silence(lead_in)

    speak_index = 0
    for kind, value in segments:
        if kind == "pause":
            pcm += silence(float(value))
            continue
        if kind == "stretch":
            cur_stretch = float(value)
            continue
        if kind == "speed":
            if hasattr(engine, "voice_settings"):
                engine.voice_settings["speed"] = float(value)
            continue

        text = str(value)
        prev = spoken_texts[speak_index - 1] if speak_index > 0 else ""
        nxt = (spoken_texts[speak_index + 1]
               if speak_index + 1 < len(spoken_texts) else "")
        speak_index += 1

        key = engine.cache_key(text, prev, nxt)
        cached = cache_dir / f"{key}.pcm"
        if cached.exists():
            audio = cached.read_bytes()
        else:
            audio = engine.synthesize(text, prev, nxt)
            cached.write_bytes(audio)
        audio = stretch_pcm(audio, rate, cur_stretch)
        audio = trim_and_fade(audio, rate) if trim else audio
        start = len(pcm) / (2 * rate)
        pcm += audio
        marks.append({"i": len(marks), "text": text,
                      "start": round(start, 3),
                      "end": round(len(pcm) / (2 * rate), 3)})

        done += 1
        secs = len(pcm) / (2 * rate)
        print(f"  [{done}/{len(speech)}] {secs//60:02.0f}:{secs%60:05.2f}  "
              f"{text[:58]}{'…' if len(text) > 58 else ''}", flush=True)

    pcm += silence(tail)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    wav_path = out_path if fmt == "wav" else out_path.with_suffix(".tmp.wav")
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(pcm))

    if fmt == "mp3":
        encode_mp3(wav_path, out_path, bitrate, lufs, rate)
        wav_path.unlink()

    if timings:
        timings.parent.mkdir(parents=True, exist_ok=True)
        timings.write_text(json.dumps(
            {"duration": round(len(pcm) / (2 * rate), 3), "segments": marks},
            indent=2), encoding="utf-8")
        print(f"  timings -> {timings}")

    total = len(pcm) / (2 * rate)
    size = out_path.stat().st_size / 1_048_576
    print(f"\nWrote {out_path}  —  {int(total//60)}m {total % 60:04.1f}s, "
          f"{size:.1f} MB, {rate} Hz mono ({engine.name})")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("script", type=Path, help="path to the session markdown")
    p.add_argument("-o", "--output", type=Path,
                   default=Path("audio/session.mp3"))
    p.add_argument("--engine", choices=("elevenlabs", "piper"),
                   default="elevenlabs")
    p.add_argument("--format", choices=("mp3", "wav"), default=None,
                   help="defaults to the output file's extension")
    p.add_argument("--bitrate", default="96k")
    p.add_argument("--no-trim", action="store_true",
                   help="keep each segment's own leading/trailing silence "
                        "instead of trimming to the scripted pause lengths")
    p.add_argument("--stretch", type=float, default=1.0,
                   help="per-segment time stretch; <1 slows speech without "
                        "changing pitch. Default 1.0, i.e. off: atempo smears "
                        "low frequencies audibly, and on a ~100 Hz narrator "
                        "that reads as robotic. Prefer --speed, which the "
                        "model applies cleanly")
    p.add_argument("--lufs", type=float, default=-19.0,
                   help="integrated loudness target; use --no-normalize to skip")
    p.add_argument("--no-normalize", action="store_true")
    p.add_argument("--lead-in", type=float, default=1.0,
                   help="seconds of silence before the first word")
    p.add_argument("--tail", type=float, default=3.0,
                   help="seconds of silence after the last word")
    p.add_argument("--cache-dir", type=Path, default=Path(".cache/tts"))
    p.add_argument("--timings", type=Path,
                   help="write per-line start/end times as JSON, so video "
                        "slides can be cut on the narration")
    p.add_argument("--dry-run", action="store_true",
                   help="parse only: print segments and estimated duration")
    p.add_argument("--no-safety", action="store_true",
                   help="drop lines tagged <!-- safety --> from the narration")
    p.add_argument("--export-prompt", type=Path, metavar="PATH",
                   help="write the narration text for pasting into a TTS UI "
                        "and exit, instead of synthesising")
    p.add_argument("--prompt-style",
                   choices=("markers", "speech-only", "breaks"),
                   default="markers",
                   help="markers: keep [pause Ns] cues (reference / review). "
                        "speech-only: narration alone, safe to paste into a "
                        "TTS UI, which would otherwise read the cues aloud. "
                        "breaks: <break/> tags the ElevenLabs UI understands, "
                        "capped at --break-cap seconds each")
    p.add_argument("--break-cap", type=float, default=3.0,
                   help="longest single <break/> tag; ElevenLabs ignores or "
                        "mangles anything above 3 seconds (default: 3.0)")
    # ElevenLabs options
    p.add_argument("--voice-id", default=DEFAULT_VOICE_ID)
    p.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    p.add_argument("--stability", type=float, default=0.55,
                   help="higher is flatter and calmer; 0.55 reads as animated, "
                        "which is wrong for a formula meant to sound identical "
                        "every time")
    p.add_argument("--similarity", type=float, default=0.75)
    p.add_argument("--speed", type=float, default=0.90,
                   help="ElevenLabs speaking rate; <1 is slower. Kept off the "
                        "0.7 floor, where the model starts to sound strained; "
                        "the remaining slowdown comes from --stretch, which is "
                        "a clean pitch-preserving resample")
    # piper options
    p.add_argument("--piper-model", default="voices/en-us-lessac-medium.onnx")
    p.add_argument("--length-scale", type=float, default=1.15,
                   help="piper speaking rate; >1 is slower")
    # Settings declared in the script come first so explicit CLI flags, parsed
    # later, win over them.
    known, _ = p.parse_known_args()
    file_args = script_render_args(known.script) if known.script.exists() else []
    args = p.parse_args(file_args + sys.argv[1:])
    if file_args:
        print(f"{known.script}: applying render settings from script: "
              f"{' '.join(file_args)}")

    fmt = args.format or (args.output.suffix.lstrip(".").lower() or "mp3")
    if fmt not in ("mp3", "wav"):
        raise SystemExit(f"unsupported output format: {fmt}")

    segments = parse_script(args.script, omit_safety=args.no_safety)
    words = sum(len(str(v).split()) for k, v in segments if k == "speak")
    pause_total = sum(float(v) for k, v in segments if k == "pause")
    # ~135 wpm is a typical guided-relaxation delivery rate.
    est = words / 135 * 60 + pause_total + args.lead_in + args.tail

    print(f"{args.script}: {len(segments)} segments "
          f"({sum(1 for k, _ in segments if k == 'speak')} spoken, "
          f"{sum(1 for k, _ in segments if k == 'pause')} pauses)")
    print(f"  {words} words, {pause_total:.0f}s of silence, "
          f"estimated {est/60:.1f} min total\n")

    if args.export_prompt:
        lines = []
        truncated = []
        for kind, value in segments:
            if kind in ("stretch", "speed"):
                continue
            if kind == "speak":
                lines.append(str(value))
            elif args.prompt_style == "markers":
                lines.append(f"[pause {float(value):g}s]")
            elif args.prompt_style == "breaks":
                want = float(value)
                cap = args.break_cap
                # ElevenLabs caps a single break tag; longer rests have to be
                # chained, and chaining many is what destabilises the voice.
                tags, left = [], want
                while left > 0.05:
                    step = min(cap, left)
                    tags.append(f'<break time="{step:.1f}s" />')
                    left -= step
                if want > cap:
                    truncated.append((want, len(tags)))
                lines.append(" ".join(tags))
        text = "\n\n".join(lines) + "\n"
        args.export_prompt.parent.mkdir(parents=True, exist_ok=True)
        args.export_prompt.write_text(text, encoding="utf-8")
        print(f"Wrote {args.export_prompt} — {len(text)} characters")
        if args.prompt_style == "breaks" and truncated:
            worst = max(t[1] for t in truncated)
            print(f"\n  WARNING: {len(truncated)} pauses exceed the "
                  f"{args.break_cap:g}s tag limit and are chained "
                  f"(up to {worst} tags in a row).")
            print("  ElevenLabs degrades with long break chains. For exact "
                  "silence, drop --export-prompt and let this tool render "
                  "the audio.")
        return 0

    if args.dry_run:
        for kind, value in segments:
            print(f"  {kind:5}  {value}")
        return 0

    if args.engine == "elevenlabs":
        engine = ElevenLabsEngine(args.voice_id, args.model_id, args.stability,
                                  args.similarity, args.speed)
    else:
        engine = PiperEngine(args.piper_model, args.length_scale)

    build(segments, engine, args.output, args.cache_dir, args.bitrate, fmt,
          args.lead_in, args.tail,
          None if args.no_normalize else args.lufs, args.stretch,
          not args.no_trim, args.timings)
    return 0


if __name__ == "__main__":
    sys.exit(main())
