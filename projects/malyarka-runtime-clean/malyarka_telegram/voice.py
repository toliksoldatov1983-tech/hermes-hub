"""Voice transcription helpers for Telegram voice messages."""

from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile


def transcribe_voice_file(
    path: str | Path,
    *,
    api_key: str | None,
    model: str = "gpt-4o-mini-transcribe",
    local_command: str | None = None,
    local_model_path: str | None = None,
) -> str:
    """Transcribe an audio file through local STT or OpenAI when configured."""

    if local_command and local_model_path:
        return _transcribe_voice_file_local(
            path,
            command=local_command,
            model_path=local_model_path,
        )

    if not api_key:
        raise VoiceTranscriptionNotConfigured("Voice transcription is not configured.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise VoiceTranscriptionNotConfigured("openai package is not installed.") from exc

    client = OpenAI(api_key=api_key)
    with Path(path).open("rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
        )

    text = str(getattr(transcription, "text", "") or "").strip()
    if not text:
        raise VoiceTranscriptionFailed("Voice transcription returned empty text.")
    return text


def _transcribe_voice_file_local(
    path: str | Path,
    *,
    command: str,
    model_path: str,
) -> str:
    input_path = Path(path)
    command_path = Path(command)
    model = Path(model_path)
    if not command_path.exists() or not model.exists():
        raise VoiceTranscriptionNotConfigured("Local STT command or model is missing.")

    with tempfile.TemporaryDirectory(prefix="malyarka_stt_") as temp_dir:
        wav_path = Path(temp_dir) / "voice.wav"
        ffmpeg_result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(input_path),
                "-ar",
                "16000",
                "-ac",
                "1",
                "-c:a",
                "pcm_s16le",
                str(wav_path),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if ffmpeg_result.returncode != 0:
            raise VoiceTranscriptionFailed("ffmpeg failed to convert voice file.")

        output_prefix = Path(temp_dir) / "result"
        whisper_result = subprocess.run(
            [
                str(command_path),
                "-m",
                str(model),
                "-f",
                str(wav_path),
                "-l",
                "ru",
                "-otxt",
                "-of",
                str(output_prefix),
                "-nt",
                "-np",
            ],
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        if whisper_result.returncode != 0:
            raise VoiceTranscriptionFailed("local whisper.cpp failed.")

        text_path = output_prefix.with_suffix(".txt")
        if not text_path.exists():
            raise VoiceTranscriptionFailed("local whisper.cpp did not create text output.")
        text = text_path.read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            raise VoiceTranscriptionFailed("local whisper.cpp returned empty text.")
        return " ".join(text.split())


class VoiceTranscriptionNotConfigured(RuntimeError):
    """Raised when voice transcription cannot run because config is missing."""


class VoiceTranscriptionFailed(RuntimeError):
    """Raised when transcription provider fails or returns unusable text."""
