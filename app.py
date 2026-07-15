"""
app.py -- Multimodal Emotion Analyzer
Streamlit entry point.

Run with:
    streamlit run app.py
"""

import base64
import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.audio_processor import extract_and_transcribe
from src.video_processor import extract_key_frames
from src.emotion_analyzer import analyze_emotion
from src.report_generator import generate_html_report

load_dotenv()

# Page config
st.set_page_config(
    page_title="Multimodal Emotion Analyzer",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Multimodal Emotion Analyzer")
st.caption(
    "Upload a video monologue + enter your heart rate → "
    "get a multimodal emotion report"
)

# Sidebar: settings
with st.sidebar:
    st.header("⚙ Settings")

    whisper_model = st.selectbox(
        "Whisper Model Size",
        options=["tiny", "base", "small", "medium"],
        index=1,
        help="Larger = more accurate but slower. 'base' is a good default.",
    )

    max_frames = st.slider("Max Key Frames", min_value=1, max_value=8, value=4)

    st.divider()
    st.markdown("**About**")
    st.markdown(
        "This tool fuses speech transcription, facial expression, "
        "and heart rate data to analyze emotional state using a multimodal LLM."
    )
    st.markdown(
        "[GitHub](https://github.com/wxyhuigenghao-glitch/multimodal-emotion-analyzer)"
    )

# Main input area
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "📹 Upload Video or Audio",
        type=["mp4", "mov", "avi", "mkv", "webm", "mp3", "wav", "m4a"],
        help="A short monologue video works best (10-120 seconds).",
    )

with col2:
    heart_rate = st.number_input(
        "💓 Heart Rate (bpm)",
        min_value=30,
        max_value=220,
        value=72,
        step=1,
        help="Enter your current heart rate. Normal resting: 60-100 bpm.",
    )
    hr_provided = st.checkbox("Include heart rate in analysis", value=True)

# Run analysis
run_btn = st.button(
    "▶ Analyze Emotion", type="primary", use_container_width=True
)

if run_btn:
    # Validate inputs
    active_api_key = os.environ.get("GEMINI_API_KEY", "")
    if not active_api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
        st.stop()

    if not uploaded_file:
        st.error("Please upload a video or audio file.")
        st.stop()

    hr_value = int(heart_rate) if hr_provided else None

    # Save upload to a temp file
    suffix = Path(uploaded_file.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        # Step 1: Transcribe
        with st.status(
            "🎙 Transcribing audio with Whisper...", expanded=True
        ) as status:
            transcript_result = extract_and_transcribe(
                tmp_path, model_size=whisper_model
            )
            transcript = transcript_result["text"]
            lang = transcript_result["language"]
            status.update(
                label=f"✅ Transcription complete ({lang.upper()})",
                state="complete",
            )

        # Step 2: Extract key frames
        is_video = suffix.lower() in {".mp4", ".mov", ".avi", ".mkv", ".webm"}
        key_frames = []
        if is_video:
            with st.status(
                "🎞 Extracting key frames...", expanded=True
            ) as status:
                try:
                    key_frames = extract_key_frames(
                        tmp_path,
                        max_frames=max_frames,
                        prefer_faces=True,
                    )
                    face_count = sum(
                        1 for f in key_frames if f["has_face"]
                    )
                    status.update(
                        label=f"✅ {len(key_frames)} frames extracted "
                        f"({face_count} with face)",
                        state="complete",
                    )
                except Exception as e:
                    st.warning(f"Frame extraction skipped: {e}")
                    status.update(
                        label="⚠ Frame extraction skipped", state="error"
                    )

        # Step 3: LLM Emotion Analysis
        with st.status(
            "🤖 Analyzing emotion with Gemini...", expanded=True
        ) as status:
            result = analyze_emotion(
                transcript=transcript,
                heart_rate=hr_value,
                key_frames=key_frames,
                api_key=active_api_key,
            )
            status.update(
                label="✅ Emotion analysis complete", state="complete"
            )

        # Display results
        st.divider()
        st.subheader("📊 Results")

        # Top metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(
            "Primary Emotion", f"{result.emotion_type.capitalize()}"
        )
        m2.metric("Intensity", f"{result.emotion_level} / 10")
        m3.metric(
            "Valence",
            f"{result.valence:+.2f}",
            help="-1 (negative) to +1 (positive)",
        )
        m4.metric(
            "Arousal",
            f"{result.arousal:+.2f}",
            help="-1 (calm) to +1 (activated)",
        )

        # Secondary emotions
        if result.secondary_emotions:
            st.markdown(
                "**Secondary emotions:** "
                + " · ".join(f"`{e}`" for e in result.secondary_emotions)
            )

        st.divider()

        # Signal breakdown
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📡 Signal Cues**")
            if result.facial_cues:
                st.markdown(f"😮 **Face:** {result.facial_cues}")
            if result.speech_cues:
                st.markdown(f"🗣 **Speech:** {result.speech_cues}")
            if result.physiological_cues:
                st.markdown(
                    f"💓 **Physiology:** {result.physiological_cues}"
                )

        with c2:
            st.markdown("**💡 Summary**")
            st.info(result.summary)
            if result.interaction_suggestion:
                st.markdown("**🤖 Interaction Suggestion**")
                st.success(result.interaction_suggestion)

        # Key frames preview
        if key_frames:
            st.divider()
            st.markdown("**🎞 Key Frames**")
            cols = st.columns(min(len(key_frames), 4))
            for i, (col, frame) in enumerate(
                zip(cols, key_frames[:4])
            ):
                img_bytes = base64.b64decode(frame["base64_jpeg"])
                label = (
                    f"{frame['timestamp_sec']}s "
                    f"{'✓ face' if frame['has_face'] else ''}"
                )
                col.image(
                    img_bytes, caption=label, use_container_width=True
                )

        # Transcript
        with st.expander("📝 Full Transcript", expanded=False):
            st.write(
                transcript if transcript.strip()
                else "_(no speech detected)_"
            )

        # Step 4: Generate & offer HTML report download
        st.divider()
        html_report = generate_html_report(
            result=result,
            transcript=transcript,
            heart_rate=hr_value,
            key_frames=key_frames,
        )

        st.download_button(
            label="⬇ Download HTML Report",
            data=html_report.encode("utf-8"),
            file_name="emotion_report.html",
            mime="text/html",
            use_container_width=True,
        )

    except Exception as e:
        st.error(f"Analysis failed: {e}")
        import traceback

        st.code(traceback.format_exc())

    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)