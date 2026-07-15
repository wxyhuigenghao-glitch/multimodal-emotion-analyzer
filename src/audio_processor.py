"""
audio_processor.py — Extract audio from video and transcribe with Whisper.
"""

import whisper


def extract_and_transcribe(
    media_path: str,
    model_size: str = "base",
) -> dict:
    """
    Transcribe audio from a video or audio file using Whisper.

    Args:
        media_path: Path to the input media file (video or audio).
        model_size: Whisper model size (tiny, base, small, medium, large).

    Returns:
        dict with keys:
            - text (str): Full transcription text.
            - language (str): Detected language code (e.g., 'en').
            - segments (list): List of segment dicts (start, end, text).
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(media_path)

    return {
        "text": result["text"].strip(),
        "language": result.get("language", "unknown"),
        "segments": result.get("segments", []),
    }