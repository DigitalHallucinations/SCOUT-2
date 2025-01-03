#gui\Google\GglCldSvcs\stt.py

import os
import sounddevice as sd
import numpy as np
import soundfile as sf
from google.cloud import speech_v1p1beta1 as speech
from modules.logging.logger import setup_logger

logger = setup_logger('Ggl_stt.py')

class SpeechToText:
    def __init__(self, fs=16000, sample_rate_hertz=16000, enable_automatic_punctuation=True):
        logger.info("Initializing SpeechToText")
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=enable_automatic_punctuation
        )
        
        self.fs = fs
        self.frames = []
        self.recording = False
        self.stream = sd.InputStream(callback=self.callback, channels=1, samplerate=self.fs)

    def callback(self, indata, frames, time, status):
        if self.recording:
            self.frames.append(indata.copy())

    def listen(self):  
        logger.info("Listening...")
        self.frames = []
        self.recording = True
        self.stream = sd.InputStream(callback=self.callback, channels=1, samplerate=self.fs)
        self.stream.start()

    def stop_listening(self):
        logger.info("Stopping listening")
        if self.recording:
            self.stream.stop()
            self.recording = False
            self.save_recording()
            logger.debug("Recording stopped")
        else:
            logger.warning("Tried to stop listening, but was not recording")
        self.stream.close()
        self.frames = []

    def save_recording(self, filename='output.wav'):
        logger.info("Saving recording")
        output_dir = 'assets/user/sst_output'
        os.makedirs(output_dir, exist_ok=True)  
        output_file = os.path.join(output_dir, filename)

        if self.frames:
            data = np.concatenate(self.frames)
            sf.write(output_file, data, self.fs)
            logger.info(f"Audio recorded and saved as {output_file}")
        else:
            logger.warning("No frames to save")

    def transcribe(self, audio_file):
        logger.info(f"Transcribing file {audio_file}")
        audio_file_path = os.path.join('assets/user/sst_output', audio_file)

        with open(audio_file_path, 'rb') as audio:
            audio_content = audio.read()

        audio = speech.RecognitionAudio(content=audio_content)
        response = self.client.recognize(config=self.config, audio=audio)

        if not os.path.exists(audio_file_path):
            logger.error(f"Audio file not found: {audio_file_path}")
            return "No audio file to transcribe"

        transcript = []
        for result in response.results:
            transcript.append(result.alternatives[0].transcript)

        # Delete the audio file after transcription
        os.remove(audio_file_path)
        logger.info(f"Deleted audio file {audio_file_path}")

        return ' '.join(transcript)