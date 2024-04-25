import streamlit as st
import streamlit.components.v1 as components
import os
import tempfile
from moviepy.editor import VideoFileClip
import whisper
from pytube import YouTube

# Folder for temporary files
temp_dir = "temp_files"
os.makedirs(temp_dir, exist_ok=True)

st.title('Video Transcription App with Whisper')
st.subheader('Choose your input method')

# Model selection
model_sizes = ["tiny", "base", "small", "medium", "large"]
selected_model_size = st.selectbox('Select Whisper model size:', model_sizes, index=model_sizes.index("base"))

# Input method selection
input_method = st.radio("Do you want to upload a video or enter a YouTube URL?", ("Upload a video", "Enter a YouTube URL"))

uploaded_file = None
youtube_url = ""

if input_method == "Upload a video":
    uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "mov", "avi", "mkv"])
elif input_method == "Enter a YouTube URL":
    youtube_url = st.text_input("Paste a YouTube video URL here:")

def download_youtube_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    temp_video_path = os.path.join(temp_dir, yt.title.replace("/", "_") + ".mp4")  # Replace "/" to avoid file path issues
    stream.download(output_path=temp_dir, filename=yt.title.replace("/", "_") + ".mp4")
    return temp_video_path

def transcribe_video(video_file_path, model_size):
    audio_file_path = os.path.join(temp_dir, "temp_audio.wav")
    progress_bar = st.progress(0)
    st.text("Preparing video and audio files...")

    try:
        with VideoFileClip(video_file_path) as video:
            if video.audio is None:
                raise ValueError("The video file does not contain an audio track.")
            video.audio.write_audiofile(audio_file_path, codec='pcm_s16le', nbytes=2, fps=16000)
        progress_bar.progress(50)

        model = whisper.load_model(model_size)
        result = model.transcribe(audio_file_path)
        progress_bar.progress(100)
        st.text("Transcription completed.")
        text = result['text']
    finally:
        if os.path.exists(video_file_path):
            os.remove(video_file_path)
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)

    return text

if uploaded_file is not None or youtube_url:
    if st.button('Transcribe'):
        try:
            st.write("Transcribing...")
            video_file_path = ""
            if uploaded_file:
                video_file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(video_file_path, "wb") as f:
                    f.write(uploaded_file.read())
            elif youtube_url:
                video_file_path = download_youtube_video(youtube_url)
                st.write(f"Downloaded '{video_file_path}' for transcription.")
            
            transcript = transcribe_video(video_file_path, selected_model_size)
            transcript_area = st.text_area("Transcription:", transcript, height=300)
            # JavaScript for copy to clipboard
            copy_button_code = f"""
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
            components.html(copy_button_code, height=50)
        except Exception as e:
            st.write("An error occurred during transcription:")
            st.write(str(e))

if st.button('Start New Transcription'):
    st.experimental_rerun()
