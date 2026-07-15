{\rtf1\ansi\ansicpg936\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww14080\viewh9820\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # \uc0\u55358 \u56800  Multimodal Emotion Analyzer\
\
A lightweight, open-source tool for analyzing human emotional states from **video/audio monologues** combined with **physiological signals** (heart rate). Powered by Whisper for transcription, OpenCV for facial frame extraction, and a multimodal LLM (Gemini) for emotion reasoning.\
\
> **Research Direction:** This project explores how multimodal signals \'97 language, facial expression, and biometrics \'97 can be fused to produce interpretable emotion scores and actionable interaction strategies.\
\
---\
\
## \uc0\u10024  Demo Screenshot\
\
```\
[Upload Video] + [Enter Heart Rate]\
\'a0 \'a0 \'a0 \'a0 \uc0\u8595 \
\uc0\u9484 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9488 \
\uc0\u9474  \'a0Emotion: \u55357 \u56863  Anxious \'a0 Level: 7/10 \'a0\u9474 \
\uc0\u9474  \'a0Valence: -0.3 \'a0Arousal: +0.8 \'a0 \'a0 \'a0 \u9474 \
\uc0\u9474  \'a0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472  \'a0\u9474 \
\uc0\u9474  \'a0\u55357 \u56541  Speech: fast pace, rising tone \'a0\u9474 \
\uc0\u9474  \'a0\u55357 \u56878  Face: furrowed brows, tense jaw \u9474 \
\uc0\u9474  \'a0\u55357 \u56467  HR: 95 bpm (elevated) \'a0 \'a0 \'a0 \'a0 \'a0 \u9474 \
\uc0\u9474  \'a0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472  \'a0\u9474 \
\uc0\u9474  \'a0\u55357 \u56481  Summary: ... \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0\u9474 \
\uc0\u9492 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9496 \
```\
\
---\
\
## \uc0\u55356 \u57303  Architecture\
\
```\
\uc0\u9484 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9488 \
\uc0\u9474  \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0INPUT LAYER \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \u9474 \
\uc0\u9474  \'a0 Video/Audio File \'a0 \'a0 \'a0 \'a0 \'a0Heart Rate (manual input) \'a0 \'a0\u9474 \
\uc0\u9492 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9516 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9516 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9496 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0\uc0\u9474  \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \u9474 \
\'a0 \'a0 \uc0\u9484 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9660 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9488  \'a0 \'a0 \'a0 \'a0 \u9484 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9660 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9488 \
\'a0 \'a0 \uc0\u9474  \'a0Audio Track \'a0 \'a0\u9474  \'a0 \'a0 \'a0 \'a0 \u9474  \'a0Video Frames \'a0 \u9474 \
\'a0 \'a0 \uc0\u9474  \'a0(Whisper ASR) \'a0\u9474  \'a0 \'a0 \'a0 \'a0 \u9474  \'a0(OpenCV + Face \u9474 \
\'a0 \'a0 \uc0\u9474  \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \u9474  \'a0 \'a0 \'a0 \'a0 \u9474  \'a0 Detection) \'a0 \'a0\u9474 \
\'a0 \'a0 \uc0\u9492 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9516 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9496  \'a0 \'a0 \'a0 \'a0 \u9492 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9516 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9496 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0\uc0\u9474  \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0\uc0\u9492 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9516 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9496 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9484 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9660 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9488 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9474  \'a0 Gemini 1.5 Flash \u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9474  \'a0Multimodal Prompt \u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9474  \'a0(Text + Images) \'a0 \u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9492 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9516 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9496 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9484 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9660 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9488 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9474  \'a0Structured JSON \'a0 \u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9474  \'a0Emotion Output \'a0 \'a0\u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9492 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9516 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9496 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9484 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9660 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9488 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9474  \'a0Streamlit UI \'a0+ \'a0 \u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9474  \'a0HTML Report \'a0 \'a0 \'a0 \u9474 \
\'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \'a0 \uc0\u9492 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9496 \
```\
\
---\
\
---\
\
## \uc0\u55357 \u56960  Quick Start\
\
### 1. Clone the repo\
\
```bash\
git clone https://github.com/YOUR_USERNAME/multimodal-emotion-analyzer.git\
cd multimodal-emotion-analyzer\
```\
\
### 2. Install dependencies\
\
```bash\
pip install -r requirements.txt\
```\
\
> **Note:** Whisper requires `ffmpeg`. Install it via:\
> - macOS: `brew install ffmpeg`\
> - Ubuntu: `sudo apt install ffmpeg`\
> - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH\
\
### 3. Configure API key\
\
```bash\
cp .env.example .env\
# Edit .env and add your Gemini API key\
```\
\
Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com).\
\
### 4. Run the app\
\
```bash\
streamlit run app.py\
```\
\
Open `http://localhost:8501` in your browser.\
\
---\
\
## \uc0\u55357 \u56550  Tech Stack\
\
| Component | Library | Role |\
|-----------|---------|------|\
| Speech-to-Text | `openai-whisper` | Transcribe audio from video |\
| Video Processing | `opencv-python` | Extract key frames, detect faces |\
| Multimodal LLM | `google-generativeai` (Gemini 1.5 Flash) | Fuse signals, reason about emotion |\
| UI | `streamlit` | Web interface |\
| Visualization | Chart.js + Tailwind CSS | HTML report rendering |\
\
---\
\
## \uc0\u55357 \u56522  Output Format\
\
The LLM returns a structured JSON:\
\
```json\
\{\
\'a0 "emotion_type": "anxious",\
\'a0 "emotion_level": 7,\
\'a0 "valence": -0.3,\
\'a0 "arousal": 0.8,\
\'a0 "secondary_emotions": ["worried", "tense"],\
\'a0 "facial_cues": "furrowed brows, slightly averted gaze",\
\'a0 "speech_cues": "fast speech rate, rising intonation, frequent pauses",\
\'a0 "physiological_cues": "elevated heart rate (95 bpm) suggests sympathetic activation",\
\'a0 "summary": "The user appears to be experiencing moderate anxiety...",\
\'a0 "interaction_suggestion": "Use a calm, low-pace voice response. Offer structured options rather than open questions."\
\}\
```\
\
---\
\
## \uc0\u55357 \u56826  Roadmap\
\
This demo is **Stage 1** of a broader research agenda:\
\
### Stage 1 \'97 Current (Demo)\
- [x] Manual video upload + heart rate text input\
- [x] Whisper speech transcription\
- [x] Key frame extraction with face detection\
- [x] Gemini multimodal emotion analysis\
- [x] Streamlit UI + HTML report export\
\
### Stage 2 \'97 Real-world Signal Collection\
- [ ] Replace manual HR input with wearable sensor integration (BLE/ANT+)\
- [ ] Support real-time webcam + microphone stream\
- [ ] Add GSR (galvanic skin response) as additional physiological channel\
\
### Stage 3 \'97 Model Specialization\
- [ ] Collect labeled multimodal samples via controlled experiments\
- [ ] Fine-tune emotion classification model on domain-specific data\
- [ ] Benchmark against general-purpose models\
\
### Stage 4 \'97 Interaction Strategy Generation\
- [ ] Map [emotion type \'d7 level] \uc0\u8594  interaction strategy taxonomy\
- [ ] Implement strategy output for AI assistant (voice/text)\
- [ ] Explore embodied interaction for social robots\
\
### Stage 5 \'97 Personal Memory Augmentation\
- [ ] Build per-user emotion history profile\
- [ ] Use retrieval-augmented generation (RAG) to personalize emotion interpretation\
- [ ] "This user tends to underreport anxiety \'97 adjust calibration accordingly"\
\
---\
\
## \uc0\u9888  Limitations\
\
1. **Passive input model**: Current version requires manual upload. Does not support continuous real-time monitoring.\
2. **General-purpose models**: Using off-the-shelf Whisper + Gemini, not fine-tuned for clinical emotion recognition.\
3. **Single-frame facial analysis**: Extracts key frames rather than continuous facial action unit (FAU) tracking.\
4. **No ground truth validation**: Emotion scores are LLM interpretations, not clinically validated measures.\
\
---\
\
## \uc0\u55358 \u56605  Contributing\
\
PRs and issues welcome. This is an exploratory research prototype \'97 contributions toward any Roadmap item are appreciated.\
\
---\
\
## \uc0\u55357 \u56516  License\
\
MIT License. See [LICENSE](LICENSE).\
\
---\
\
## \uc0\u55357 \u56538  References\
\
- [Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)\
- [Gemini: A Family of Highly Capable Multimodal Models](https://arxiv.org/abs/2312.11805)\
- [Multimodal Sentiment Analysis: A Survey](https://arxiv.org/abs/1812.00784)}