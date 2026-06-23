from pathlib import Path

import pytest

from malyarka_telegram.voice import (
    VoiceTranscriptionNotConfigured,
    transcribe_voice_file,
)


def test_transcribe_voice_file_requires_api_key(tmp_path: Path):
    voice_path = tmp_path / "voice.ogg"
    voice_path.write_bytes(b"fake-ogg")

    with pytest.raises(VoiceTranscriptionNotConfigured):
        transcribe_voice_file(voice_path, api_key=None)


def test_transcribe_voice_file_requires_existing_local_stt_files(tmp_path: Path):
    voice_path = tmp_path / "voice.ogg"
    voice_path.write_bytes(b"fake-ogg")

    with pytest.raises(VoiceTranscriptionNotConfigured):
        transcribe_voice_file(
            voice_path,
            api_key=None,
            local_command=str(tmp_path / "missing-whisper"),
            local_model_path=str(tmp_path / "missing-model.bin"),
        )
