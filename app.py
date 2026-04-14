import streamlit as st
import os

from src.audio_processing import transcribe_audio
from src.nlp_analysis import analyze_transcript
from src.utils import save_uploaded_file, generate_mock_transcript
from src import ui_components as ui

# Streamlit config
st.set_page_config(
    page_title="AI Scam Call Analyzer Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for contest-winning premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 55px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        background: linear-gradient(90deg, #00FFA3 0%, #00B8FF 100%);
        color: #090B10 !important;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 255, 163, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 255, 163, 0.6);
        background: linear-gradient(90deg, #00FFbA 0%, #00c8FF 100%);
    }
    
    .h1-title {
        background: -webkit-linear-gradient(45deg, #00FFA3, #00B8FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    
    .h2-subtitle {
        color: #94A3B8;
        font-weight: 400;
        font-size: 1.2rem;
        margin-top: 5px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="h1-title">🛡️ AI Scam Call Analyzer Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="h2-subtitle">Analyze call recordings instantly using hybrid AI models. Detect threats before they happen with our premium risk engine.</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("Upload Call Audio")
        audio_file = st.file_uploader("Upload an audio file (.wav, .mp3, .m4a)", type=["wav", "mp3", "m4a"])
        
        st.markdown("---")
        st.header("Test with Samples")
        test_safe = st.button("Use Sample Safe Call")
        test_scam = st.button("Use Sample Scam Call")
        
        st.markdown("---")
        st.markdown("**Powered by:**")
        st.markdown("- **Whisper (Speech-to-Text)**")
        st.markdown("- **Hybrid LLM NLP Engine**")

    # Initialize session state for transcript if not present
    if "transcript" not in st.session_state:
        st.session_state.transcript = None

    # Handle sample buttons
    if test_safe:
        st.session_state.transcript = generate_mock_transcript(scam=False)
        st.experimental_rerun()
        
    if test_scam:
        st.session_state.transcript = generate_mock_transcript(scam=True)
        st.experimental_rerun()

    # Handle Audio Upload (Transcribe)
    if audio_file is not None:
        st.info("Transcribing audio using Whisper...")
        temp_dir = "temp_audio"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, audio_file.name)
        save_uploaded_file(audio_file, temp_path)
        
        try:
            transcript = transcribe_audio(temp_path)
            st.session_state.transcript = transcript
            st.success("Transcription complete!")
        except Exception as e:
            st.error(f"Error during transcription: {e}")

    # Analyze active transcript
    if st.session_state.transcript:
        transcript = st.session_state.transcript
        
        st.markdown("---")
        
        with st.spinner("Analyzing transcript using Hybrid NLP models..."):
            analysis = analyze_transcript(transcript)
            
        # Layout columns
        col1, col2 = st.columns([1, 2])
        
        with col1:
            ui.render_risk_score(analysis["risk_score"])
            ui.render_scam_type(analysis["scam_type"], analysis["confidence_score"])
            ui.render_recommendation(analysis["recommendation"], analysis["summary_for_10_yr_old"])
            
        with col2:
            ui.render_flagged_transcript(analysis["flagged_sentences"])
            
        # History logger (append to session state)
        if "history" not in st.session_state:
            st.session_state.history = []
            
        # Avoid duplicating same transcript logically (for mock demo)
        if len(st.session_state.history) == 0 or st.session_state.history[-1]["transcript"] != transcript:
            st.session_state.history.append({
                "transcript": transcript,
                "score": analysis["risk_score"],
                "type": analysis["scam_type"]
            })
            
        st.markdown("---")
        with st.expander("View Processing Logs & Recent History Session"):
            st.write(st.session_state.history)

if __name__ == "__main__":
    main()
