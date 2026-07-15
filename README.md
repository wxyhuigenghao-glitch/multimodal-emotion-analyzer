# 🧠 Multimodal Emotion Analyzer

A lightweight, open-source tool for analyzing human emotional states from **video/audio monologues** combined with **physiological signals** (heart rate). Powered by Whisper for transcription, OpenCV for facial frame extraction, and a multimodal LLM (Gemini) for emotion reasoning.

> **Research Direction:** This project explores how multimodal signals — language, facial expression, and biometrics — can be fused to produce interpretable emotion scores and actionable interaction strategies.

---

## ✨ Demo Screenshot

```
[Upload Video] + [Enter Heart Rate]
        ↓
┌─────────────────────────────────────┐
│  Emotion: 😟 Anxious   Level: 7/10  │
│  Valence: -0.3  Arousal: +0.8       │
│  ─────────────────────────────────  │
│  📝 Speech: fast pace, rising tone  │
│  😮 Face: furrowed brows, tense jaw │
│  💓 HR: 95 bpm (elevated)           │
│  ─────────────────────────────────  │
│  💡 Summary: ...                    │
└─────────────────────────────────────┘
```
click to try：https://multimodal-emotion-analyzer-gqwxiszsbab79kkipgcy2h.streamlit.app/

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────┐
│                        INPUT LAYER                       │
│   Video/Audio File          Heart Rate (manual input)    │
└────────────┬───────────────────────────┬─────────────────┘
             │                           │
    ┌────────▼────────┐         ┌────────▼────────┐
    │  Audio Track    │         │  Video Frames   │
    │  (Whisper ASR)  │         │  (OpenCV + Face │
    │                 │         │   Detection)    │
    └────────┬────────┘         └────────┬────────┘
             │                           │
             └──────────┬────────────────┘
                        │
              ┌─────────▼──────────┐
              │   Gemini 1.5 Flash │
              │  Multimodal Prompt │
              │  (Text + Images)   │
              └─────────┬──────────┘
                        │
              ┌─────────▼──────────┐
              │  Structured JSON   │
              │  Emotion Output    │
              └─────────┬──────────┘
                        │
              ┌─────────▼──────────┐
              │  Streamlit UI  +   │
              │  HTML Report       │
              └────────────────────┘
```

---
---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/multimodal-emotion-analyzer.git
cd multimodal-emotion-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** Whisper requires `ffmpeg`. Install it via:
> - macOS: `brew install ffmpeg`
> - Ubuntu: `sudo apt install ffmpeg`
> - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### 3. Configure API key

```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com).

### 4. Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📦 Tech Stack

| Component | Library | Role |
|-----------|---------|------|
| Speech-to-Text | `openai-whisper` | Transcribe audio from video |
| Video Processing | `opencv-python` | Extract key frames, detect faces |
| Multimodal LLM | `google-generativeai` (Gemini 1.5 Flash) | Fuse signals, reason about emotion |
| UI | `streamlit` | Web interface |
| Visualization | Chart.js + Tailwind CSS | HTML report rendering |

---

## 📊 Output Format

The LLM returns a structured JSON:

```json
{
  "emotion_type": "anxious",
  "emotion_level": 7,
  "valence": -0.3,
  "arousal": 0.8,
  "secondary_emotions": ["worried", "tense"],
  "facial_cues": "furrowed brows, slightly averted gaze",
  "speech_cues": "fast speech rate, rising intonation, frequent pauses",
  "physiological_cues": "elevated heart rate (95 bpm) suggests sympathetic activation",
  "summary": "The user appears to be experiencing moderate anxiety...",
  "interaction_suggestion": "Use a calm, low-pace voice response. Offer structured options rather than open questions."
}
```

---

## 🗺 Roadmap

This demo is **Stage 1** of a broader research agenda:

### Stage 1 — Current (Demo)
- [x] Manual video upload + heart rate text input
- [x] Whisper speech transcription
- [x] Key frame extraction with face detection
- [x] Gemini multimodal emotion analysis
- [x] Streamlit UI + HTML report export

### Stage 2 — Real-world Signal Collection
- [ ] Replace manual HR input with wearable sensor integration (BLE/ANT+)
- [ ] Support real-time webcam + microphone stream
- [ ] Add GSR (galvanic skin response) as additional physiological channel

### Stage 3 — Model Specialization
- [ ] Collect labeled multimodal samples via controlled experiments
- [ ] Fine-tune emotion classification model on domain-specific data
- [ ] Benchmark against general-purpose models

### Stage 4 — Interaction Strategy Generation
- [ ] Map [emotion type × level] → interaction strategy taxonomy
- [ ] Implement strategy output for AI assistant (voice/text)
- [ ] Explore embodied interaction for social robots

### Stage 5 — Personal Memory Augmentation
- [ ] Build per-user emotion history profile
- [ ] Use retrieval-augmented generation (RAG) to personalize emotion interpretation
- [ ] "This user tends to underreport anxiety — adjust calibration accordingly"

---

## ⚠ Limitations

1. **Passive input model**: Current version requires manual upload. Does not support continuous real-time monitoring.
2. **General-purpose models**: Using off-the-shelf Whisper + Gemini, not fine-tuned for clinical emotion recognition.
3. **Single-frame facial analysis**: Extracts key frames rather than continuous facial action unit (FAU) tracking.
4. **No ground truth validation**: Emotion scores are LLM interpretations, not clinically validated measures.

---

## 📚 References

- [Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)
- [Gemini: A Family of Highly Capable Multimodal Models](https://arxiv.org/abs/2312.11805)
- [Multimodal Sentiment Analysis: A Survey](https://arxiv.org/abs/1812.00784)

