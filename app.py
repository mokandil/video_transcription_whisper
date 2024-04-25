import streamlit as st
import streamlit.components.v1 as components
import os
import tempfile
from moviepy.editor import VideoFileClip
import whisper

# Folder for temporary files
temp_dir = "temp_files"
os.makedirs(temp_dir, exist_ok=True)

# Add title and instructions to the user
st.title('Video Transcription App with Whisper')
st.subheader('Upload your video file below')

# Model selection
model_sizes = ["tiny", "base", "small", "medium", "large"]
selected_model_size = st.selectbox('Select Whisper model size:', model_sizes, index=model_sizes.index("base"))

# File uploader
uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "mov", "avi", "mkv"])

# Function to transcribe the video  and return the text
def transcribe_video(video_file_buffer, model_size):
    """
    Transcribes the audio from a video file.

    Args:
        video_file_buffer (file-like object): The video file to transcribe.
        model_size (str): The size of the model to use for transcription.

    Returns:
        str: The transcribed text from the video.

    Raises:
        FileNotFoundError: If the video file or audio file does not exist.

    """
    video_file_path = os.path.join(temp_dir, "temp_video.mp4")
    audio_file_path = os.path.join(temp_dir, "temp_audio.wav")

    # Write the uploaded file to the specific temporary folder
    with open(video_file_path, "wb") as f:
        f.write(video_file_buffer.read())

    # Load the video file and extract audio
    video = VideoFileClip(video_file_path)
    progress_bar = st.progress(0)
    st.text("Preparing video and audio files...")

    # Actual transcription process with progress and time display
    try:
        with VideoFileClip(video_file_path) as video:
            video.audio.write_audiofile(audio_file_path, codec='pcm_s16le', nbytes=2, fps=16000)
        progress_bar.progress(50)

        model = whisper.load_model(model_size)
        result = model.transcribe(audio_file_path)
        progress_bar.progress(100)
        st.text("Transcription completed.")
        text = result['text']
    finally:
        os.remove(video_file_path)
        os.remove(audio_file_path)

    return text

# Transcribe the video and display the transcription 
# if the user has uploaded a file and clicked the "Transcribe" button
if uploaded_file is not None:
    if st.button('Transcribe'):
        try:
            st.write("Transcribing...")
            transcript = transcribe_video(uploaded_file, selected_model_size)
            transcript_area = st.text_area("Transcription:", transcript, height=300)
            html_code = f"""
                <html>
                <body>
                <textarea id="textCopy" style="display:none;">{transcript}</textarea>
                <button onclick='copyText()'
                        style="color: white; background-color: #4CAF50; border: none; padding: 10px 20px; 
                        text-align: center; text-decoration: none; display: inline-block; font-size: 16px;
                        margin: 4px 2px; cursor: pointer; border-radius: 12px;">
                    Copy to Clipboard
                </button>
                <script>
                    function copyText() {{
                        var copyText = document.getElementById("textCopy");
                        copyText.style.display = "block";
                        copyText.select();
                        document.execCommand("copy");
                        copyText.style.display = "none";
                        alert("Copied the text: " + copyText.value);
                    }}
                </script>
                </body>
                </html>
            """
            components.html(html_code, height=50)
        except Exception as e:
            st.write("An error occurred during transcription:")
            st.write(str(e))

# Button to start a new transcription
if st.button('Start New Transcription'):
    st.experimental_rerun()
