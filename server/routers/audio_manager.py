from flask import Blueprint, request
import json
import operators.db as db
import os
from werkzeug.utils import secure_filename
# import sys
# sys.path.append('../')
from openai import OpenAI
client = OpenAI()

audio_manager_api = Blueprint('audio_manager_api', __name__)

def sttoaivsgr(speech_file_path):
    import  speech_recognition as sr
    recognizer=sr.Recognizer()

    print("-----in stt----------")
    audio_file= open(speech_file_path, "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
    )
    print("openai tts:  ",transcript)
    recognizer = sr.Recognizer()
    with sr.AudioFile(speech_file_path) as source:
        audio_data = recognizer.record(source)
    text=recognizer.recognize_google(audio_data, language="he")
    print("recognize_google:  ",text)
    return (transcript)


def stt(speech_file_path):
    audio_file= open(speech_file_path, "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
    )
    return (transcript)
def sttt(speech_file_path):
    audio_file= open(speech_file_path, "rb")
    transcript = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcript


@audio_manager_api.route('/audio_manager/uploade', methods=['POST'])
def audio_manager_uploade():
    if 'audioFile' not in request.files:
        return 'No audio file part', 400

    file = request.files['audioFile']

    if file.filename == '':
        return 'No selected file', 400

    if file:
        filename = secure_filename(file.filename)
        file_path=os.path.join('audio_files', filename)
        file.save(file_path)
        text= stt(file_path)
        print("------------",text[::-1])
        print("------------",sttt(file_path))
        # sttoaivsgr(file_path)
        return 'File uploaded successfully', 200
