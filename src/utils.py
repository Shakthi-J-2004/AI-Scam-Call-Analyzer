import io
from pydub import AudioSegment

def save_uploaded_file(uploaded_file, save_path: str):
    """Saves a streamlit uploaded file to a local path."""
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

def generate_mock_transcript(scam: bool = False) -> str:
    """Generates mock transcripts for testing purposes when audio is not available."""
    if scam:
        return (
            "Hello, am I speaking with the account holder? "
            "This is an urgent call regarding your bank account. "
            "We have detected suspicious activity and your account will be suspended in 2 hours. "
            "To prevent this, please share the OTP sent to your phone immediately. "
            "Failure to do so will result in permanent blocking of your card."
        )
    return (
        "Hi, this is Alice from the dentist's office. "
        "I'm just calling to remind you about your appointment tomorrow at 10 AM. "
        "Please let us know if you need to reschedule. "
        "Have a great day, bye!"
    )
