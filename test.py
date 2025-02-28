import requests
import json
import base64 as b64
import wave

def send_post_request(path):
    url = "http://127.0.0.1:5000/google"

    with wave.open(path, 'rb') as audiofile:
        speech_data = b64.b64encode(audiofile.readframes(audiofile.getnframes())).decode()

        # Correction : encoder correctement les paramètres audio
        params_dict = {
            "nchannels": audiofile.getnchannels(),
            "sampwidth": audiofile.getsampwidth(),
            "framerate": audiofile.getframerate(),
            "nframes": audiofile.getnframes(),
            "comptype": audiofile.getcomptype(),
            "compname": audiofile.getcompname(),
        }
        params = b64.b64encode(json.dumps(params_dict).encode()).decode()

    data = {
        "result": {
            "resultType": "Partial",
            "alts": [{"transcript": "useless", "confidence": 1}]
        },
        "data": speech_data, 
        "params": params
    }

    # Debug : vérifier les données envoyées
    print("Sending data:", json.dumps(data, indent=2))

    req = requests.post(url, json=data)
    print("Response:", req.text)

if __name__ == "__main__":
    send_post_request("son.wav")
