from flask import Flask, request, jsonify
from flask_cors import CORS  # 🔹 Import du module CORS
import requests
import os
import wave
import speech_recognition as sr
import subprocess

app = Flask(__name__)
CORS(app)  # 🔹 Active CORS pour toutes les routes

# Configurer l'URL de Rasa
RASA_URL = "http://localhost:5005/webhooks/rest/webhook/"

def convert_audio_to_wav(audio_path):
    """
    Convertit l'audio en WAV PCM 16-bit, 16kHz
    """
    converted_path = audio_path.replace(".wav", "_converted.wav")
    subprocess.run(["ffmpeg", "-i", audio_path, "-acodec", "pcm_s16le", "-ar", "16000", converted_path, "-y"])
    return converted_path

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"message": "Aucun fichier reçu"}), 400

    audio_file = request.files['audio']
    audio_path = "recordings/audio.wav"
    audio_file.save(audio_path)

    # Convertir l’audio en format compatible
    converted_audio_path = convert_audio_to_wav(audio_path)

    # Reconnaissance vocale
    recognizer = sr.Recognizer()
    with sr.AudioFile(converted_audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="fr-FR")
        print(f"✅ Texte reconnu : {text}")
    except sr.UnknownValueError:
        text = "Je n'ai pas compris"
    except sr.RequestError:
        text = "Erreur du service de reconnaissance"

    # Envoyer le texte à Rasa
    rasa_data = {"sender": "user", "message": text}
    response = requests.post(RASA_URL, json=rasa_data)

    print(f"📤 Requête envoyée à Rasa : {rasa_data}")
    print(f"🔍 Code réponse HTTP : {response.status_code}")

    # Vérifier si Rasa a répondu
    if response.status_code == 200:
        rasa_response = response.json()
        print(f"📥 Réponse brute de Rasa : {rasa_response}")

        if rasa_response:
            response_text = rasa_response[0].get('text', "Pas de réponse de Rasa")
        else:
            response_text = "Rasa n'a pas répondu"
    else:
        response_text = f"Erreur Rasa : {response.status_code}"

    print(f"✅ Réponse finale : {response_text}")
    
    # 🔹 Ajouter les en-têtes CORS pour éviter les erreurs
    response = jsonify({"message": response_text})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    if not os.path.exists('recordings'):
        os.makedirs('recordings')
    app.run(host='localhost', port=5000)
