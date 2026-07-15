"""
emotion_analyzer.py — Analyze emotion using Gemini multimodal LLM.
"""

import json
import re
from typing import Optional
from dataclasses import dataclass, field

import google.generativeai as genai


@dataclass
class EmotionResult:
    """Structured result from multimodal emotion analysis."""

    emotion_type: str = "neutral"
    emotion_level: int = 5
    valence: float = 0.0
    arousal: float = 0.0
    secondary_emotions: list = field(default_factory=list)
    facial_cues: str = ""
    speech_cues: str = ""
    physiological_cues: str = ""
    summary: str = ""
    interaction_suggestion: str = ""


def _build_prompt(
    transcript: str,
    heart_rate: Optional[int] = None,
    has_frames: bool = False,
    has_hr: bool = False,
) -> str:
    """Build the multi-signal analysis prompt for Gemini."""
    parts = [
        "You are an expert emotion analyst performing multimodal emotion recognition. "
        "You fuse speech transcription, facial expression images, "
        "and physiological (heart rate) signals to infer the subject's emotional state.",
    ]

    parts.append(f"\n## Speech Transcript\n```\n{transcript}\n```")

    if has_hr:
        parts.append(
            f"\n## Physiological Signal\n"
            f"Heart rate: {heart_rate} bpm. "
            "Normal resting heart rate is 60–100 bpm. "
            "Elevated heart rate (>100 bpm) may indicate stress, anxiety, excitement, or physical exertion. "
            "Low heart rate (<60 bpm) may indicate calmness or relaxation."
        )

    if has_frames:
        parts.append(
            "\n## Facial Expression Frames\n"
            "Analyze the provided images for facial cues: eye openness, mouth shape, "
            "eyebrow position, head tilt, and overall facial muscle tension."
        )

    parts.append(
        "\n## Required Output Format\n"
        "Return ONLY a valid JSON object (no markdown code fences, no surrounding text) "
        "with exactly these fields:\n\n"
        "{\n"
        '  "emotion_type": "one of: happy, sad, angry, fearful, surprised, disgusted, neutral, anxious, excited, calm",\n'
        '  "emotion_level": <integer 1-10>,\n'
        '  "valence": <float -1.0 to +1.0>,\n'
        '  "arousal": <float -1.0 to +1.0>,\n'
        '  "secondary_emotions": ["<emotion1>", "<emotion2>", "<emotion3>"],\n'
        '  "facial_cues": "<what facial expressions suggest, or empty string>",\n'
        '  "speech_cues": "<what speech patterns suggest>",\n'
        '  "physiological_cues": "<what heart rate suggests, or empty string>",\n'
        '  "summary": "<2-3 sentence overall multimodal emotion analysis>",\n'
        '  "interaction_suggestion": "<one practical suggestion for how to interact with this person right now>"\n'
        "}\n\n"
        "IMPORTANT: Output raw JSON only. No backticks, no explanation, no markdown."
    )

    return "\n".join(parts)


def _parse_result(raw_text: str) -> EmotionResult:
    """Parse Gemini's JSON response into an EmotionResult dataclass."""
    text = raw_text.strip()
    # Strip markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError:
                return EmotionResult()
        else:
            return EmotionResult()

    return EmotionResult(
        emotion_type=data.get("emotion_type", "neutral"),
        emotion_level=int(data.get("emotion_level", 5)),
        valence=float(data.get("valence", 0.0)),
        arousal=float(data.get("arousal", 0.0)),
        secondary_emotions=data.get("secondary_emotions", []),
        facial_cues=str(data.get("facial_cues", "")),
        speech_cues=str(data.get("speech_cues", "")),
        physiological_cues=str(data.get("physiological_cues", "")),
        summary=str(data.get("summary", "")),
        interaction_suggestion=str(data.get("interaction_suggestion", "")),
    )


def analyze_emotion(
    transcript: str,
    heart_rate: Optional[int] = None,
    key_frames: Optional[list] = None,
    api_key: str = "",
) -> EmotionResult:
    """
    Perform multimodal emotion analysis using Gemini.

    Args:
        transcript: Speech transcription text.
        heart_rate: Heart rate in bpm (optional).
        key_frames: List of key frame dicts from video_processor (optional).
        api_key: Gemini API key.

    Returns:
        EmotionResult dataclass with structured analysis.
    """
    if not api_key:
        raise ValueError("Gemini API key is required")

    genai.configure(api_key=api_key)

    has_frames = bool(key_frames)
    has_hr = heart_rate is not None

    prompt = _build_prompt(
        transcript=transcript,
        heart_rate=heart_rate,
        has_frames=has_frames,
        has_hr=has_hr,
    )

    # Build multimodal content parts (text + images)
    content_parts = [prompt]

    if key_frames:
        for frame in key_frames:
            if frame.get("base64_jpeg"):
                content_parts.append({
                    "mime_type": "image/jpeg",
                    "data": frame["base64_jpeg"],
                })

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(content_parts)

    return _parse_result(response.text)