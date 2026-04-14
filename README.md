# AI Scam Call Analyzer Pro 🛡️

A production-ready web application that detects and explains scam calls using an advanced hybrid AI approach. Built with Streamlit, OpenAI Whisper, and an intensive NLP rule-engine designed to model advanced LLM capability without requiring API keys.

## Core Features
1. **Audio Transcription**: Uses `openai-whisper` for fast and accurate local speech-to-text.
2. **Hybrid NLP Analysis**: Detects fraud intent, phrasing urgency, and known scam keywords.
3. **Scam Risk Score**: 0-100 visual metric representing the probability of the call being a scam.
4. **Contextual Highlighting**:
   - 🔴 **Red**: Critical high-risk sentences (e.g. asking for OTP).
   - 🟡 **Yellow**: Medium-risk or urgent phrasing.
   - 🟢 **Green**: Safe sentences.
5. **Explain Like I'm 10**: Non-technical explanations and recommendations for end-users.

## Steps to Run Locally

### 1. Prerequisites
- Python 3.9+ installed.
- Ensure `ffmpeg` is installed on your system (Required by Whisper).
  - Windows: `choco install ffmpeg` or download from official site and add to PATH.
  - Mac: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

### 2. Setup Environment
```bash
git clone <your-repository>
cd "AI Scam Call Analyzer"

# Create a virtual environment (optional but recommended)
python -m venv venv
# Activate virtual env
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

## Deployment Guide (Streamlit Cloud)
1. Push this repository to GitHub.
2. Ensure you have `packages.txt` in your root folder containing `ffmpeg` if you are using Streamlit Cloud.
   - *Create a file named `packages.txt` with exactly the word `ffmpeg` inside.*
3. Go to [share.streamlit.io](https://share.streamlit.io).
4. Click **New App**, select your GitHub repository.
5. Select `app.py` as the entrypoint.
6. Click **Deploy**.

## Demo Usage
If you don't have an audio file ready, use the **Test with Samples** buttons in the left sidebar to instantly simulate a scam or safe call scenario.
