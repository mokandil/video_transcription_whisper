# Video Transcription App with Whisper

This project is a Streamlit-based web application that uses OpenAI's Whisper model to transcribe spoken content from video files. It provides a simple user interface to upload videos or insert a YouTube video URL, select the desired Whisper model for transcription accuracy, and display or copy the transcription results.

## Features

- Upload video files in various formats (e.g., MP4, MOV, AVI).
- Or insert a YouTube video URL to transcribe.
- Select different sizes of the Whisper model based on accuracy needs and resource availability.
- Transcribe audio content from video files to text.
- Copy the transcribed text to the clipboard.
- Reset the application to start a new transcription session.

## Installation

To run this application on your local machine, follow these steps:

### Prerequisites

- Python 3.8 or higher
- pip and virtualenv

### Setting Up the Environment

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Create a virtual environment:


   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
Install the required dependencies:

Copy code
`pip install -r requirements.txt`

## Running the Application
With all dependencies installed and the environment set up, you can run the application using:

`streamlit run app.py`

## How to Use
1. Open your web browser and go to http://localhost:8501 (or the URL indicated in your terminal).
2. Use the file uploader to select a video file you wish to transcribe.
3. Choose the Whisper model size for the transcription process.
4. Click the 'Transcribe' button to start the transcription process.
5. Once transcribed, use the 'Copy to Clipboard' button to copy the text or manually select and copy the text from the text area.
6. Click 'Start New Transcription' to reset the application and transcribe a new video.


## License
This project is licensed under the MIT License - see the LICENSE file for details.