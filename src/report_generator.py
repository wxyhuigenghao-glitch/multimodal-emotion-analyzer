"""
report_generator.py — Generate a downloadable HTML emotion report.
"""

from datetime import datetime

from typing import Optional
from src.emotion_analyzer import EmotionResult

# Emotion → accent color mapping for the report
EMOTION_COLORS = {
    "happy": "#4CAF50",
    "sad": "#2196F3",
    "angry": "#F44336",
    "fearful": "#9C27B0",
    "surprised": "#FF9800",
    "disgusted": "#795548",
    "neutral": "#9E9E9E",
    "anxious": "#FF5722",
    "excited": "#FFEB3B",
    "calm": "#8BC34A",
}


def generate_html_report(
    result: EmotionResult,
    transcript: str = "",
    heart_rate: Optional[int] = None,
    key_frames: Optional[list] = None,
) -> str:
    """
    Generate a standalone HTML emotion analysis report.

    Args:
        result: EmotionResult from emotion_analyzer.
        transcript: Full speech transcription text.
        heart_rate: Heart rate in bpm (optional).
        key_frames: List of key frame dicts with base64_jpeg (optional).

    Returns:
        Complete HTML document as a string.
    """
    color = EMOTION_COLORS.get(result.emotion_type, "#9E9E9E")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Key frames HTML ──
    frames_html = ""
    if key_frames:
        cards = ""
        for frame in key_frames:
            label = f"{frame['timestamp_sec']}s"
            if frame.get("has_face"):
                label += " · Face detected"
            cards += (
                '<div class="frame-card">'
                f'<img src="data:image/jpeg;base64,{frame["base64_jpeg"]}" alt="Frame {frame["timestamp_sec"]}s" />'
                f"<p>{label}</p>"
                "</div>"
            )
        frames_html = f'<div class="section"><h2>Key Frames</h2><div class="frames">{cards}</div></div>'

    # ── Heart rate metric card ──
    hr_card = ""
    if heart_rate is not None:
        hr_card = (
            '<div class="metric-card">'
            '<div class="metric-label">Heart Rate</div>'
            f'<div class="metric-value">{heart_rate} bpm</div>'
            "</div>"
        )

    # ── Secondary emotions ──
    secondary_html = ""
    if result.secondary_emotions:
        tags = " · ".join(
            f'<span class="tag">{e}</span>' for e in result.secondary_emotions
        )
        secondary_html = (
            f'<div class="secondary"><strong>Secondary:</strong> {tags}</div>'
        )

    # ── Signal cues ──
    cue_items = ""
    if result.facial_cues:
        cue_items += f'<div class="cue"><strong>😮 Face:</strong> {result.facial_cues}</div>'
    if result.speech_cues:
        cue_items += f'<div class="cue"><strong>🗣 Speech:</strong> {result.speech_cues}</div>'
    if result.physiological_cues:
        cue_items += f'<div class="cue"><strong>💓 Physiology:</strong> {result.physiological_cues}</div>'
    cues_html = f'<div class="section"><h2>Signal Cues</h2><div class="cues">{cue_items}</div></div>' if cue_items else ""

    # ── Summary ──
    summary_html = ""
    if result.summary:
        summary_html = (
            '<div class="section"><h2>Summary</h2>'
            f'<div class="summary-box">{result.summary}</div></div>'
        )

    # ── Suggestion ──
    suggestion_html = ""
    if result.interaction_suggestion:
        suggestion_html = (
            '<div class="section"><h2>Interaction Suggestion</h2>'
            f'<div class="suggestion-box">🤖 {result.interaction_suggestion}</div></div>'
        )

    # ── Transcript ──
    transcript_html = ""
    if transcript:
        display_text = transcript.strip() if transcript.strip() else "(no speech detected)"
        transcript_html = (
            '<div class="section"><h2>Transcript</h2>'
            f'<div class="transcript-box">{display_text}</div></div>'
        )

    # ── Assemble full document ──
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Emotion Analysis Report</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f0f1a; color: #e0e0e0; padding: 24px; }}
  .container {{ max-width: 800px; margin: 0 auto; }}
  h1 {{ font-size: 28px; margin-bottom: 4px; }}
  .timestamp {{ color: #888; font-size: 14px; margin-bottom: 24px; }}
  .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .metric-card {{ background: #1a1a2e; border-radius: 12px; padding: 20px; text-align: center; border: 1px solid #2a2a3e; }}
  .metric-label {{ font-size: 13px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }}
  .metric-value {{ font-size: 32px; font-weight: 700; margin-top: 4px; }}
  .emotion-type {{ color: {color}; }}
  .secondary {{ margin: 16px 0; }}
  .tag {{ display: inline-block; background: #2a2a3e; padding: 4px 12px; border-radius: 16px; font-size: 13px; margin: 2px; }}
  .section {{ margin-bottom: 24px; }}
  .section h2 {{ font-size: 18px; margin-bottom: 12px; border-bottom: 1px solid #2a2a3e; padding-bottom: 8px; }}
  .cue {{ padding: 8px 0; border-bottom: 1px solid #1a1a2e; }}
  .cue strong {{ color: #aaa; }}
  .summary-box {{ background: #1a1a2e; border-radius: 12px; padding: 20px; border: 1px solid #2a2a3e; margin-bottom: 16px; line-height: 1.6; }}
  .suggestion-box {{ background: #1a2e1a; border-radius: 12px; padding: 20px; border: 1px solid #2a3e2a; line-height: 1.6; }}
  .frames {{ display: flex; gap: 12px; flex-wrap: wrap; }}
  .frame-card {{ flex: 1; min-width: 150px; background: #1a1a2e; border-radius: 8px; overflow: hidden; }}
  .frame-card img {{ width: 100%; display: block; }}
  .frame-card p {{ padding: 8px; font-size: 12px; color: #888; text-align: center; }}
  .transcript-box {{ background: #1a1a2e; border-radius: 8px; padding: 16px; font-size: 14px; line-height: 1.6; white-space: pre-wrap; border: 1px solid #2a2a3e; }}
</style>
</head>
<body>
<div class="container">
  <h1>🧠 Emotion Analysis Report</h1>
  <div class="timestamp">Generated: {now}</div>

  <div class="metrics">
    <div class="metric-card">
      <div class="metric-label">Primary Emotion</div>
      <div class="metric-value emotion-type">{result.emotion_type.capitalize()}</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Intensity</div>
      <div class="metric-value">{result.emotion_level} / 10</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Valence</div>
      <div class="metric-value">{result.valence:+.2f}</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Arousal</div>
      <div class="metric-value">{result.arousal:+.2f}</div>
    </div>
    {hr_card}
  </div>

  {secondary_html}
  {cues_html}
  {summary_html}
  {suggestion_html}
  {frames_html}
  {transcript_html}
</div>
</body>
</html>"""