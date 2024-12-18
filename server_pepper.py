from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# L'adresse de votre serveur Rasa
RASA_URL = 'http://localhost:5005/webhooks/rest/webhook'

# L'adresse de Pepper
PEPPER_IP = '192.168.13.63'  # Remplacez par l'IP de votre Pepper
PEPPER_PORT = 9559

@app.route('/send_message', methods=['POST'])
def send_message():
    # Recevoir le message de Rasa
    data = request.json
    message = data.get('message', '')

    # Envoyer le message à Rasa via REST
    rasa_response = requests.post(RASA_URL, json={"sender": "pepper", "message": message})
    
    if rasa_response.status_code == 200:
        rasa_data = rasa_response.json()
        response_text = rasa_data[0].get('text', 'Désolé, je n\'ai pas compris.')

        # Envoyer le message à Pepper via HTTP (ou via un serveur de commandes)
        pepper_response = send_to_pepper(response_text)
        return jsonify({"response": pepper_response})
    else:
        return jsonify({"error": "Erreur lors de la communication avec Rasa"}), 500

def send_to_pepper(message):
    # Utilisez une méthode pour envoyer à Pepper, par exemple avec une requête HTTP
    # Si Pepper expose un service HTTP, vous pouvez envoyer ici le message.
    # Exemple de ce que vous pourriez faire :
    url = f'http://{PEPPER_IP}:{PEPPER_PORT}/say'  # Remplacez par l'endpoint réel de Pepper
    response = requests.post(url, json={"message": message})

    if response.status_code == 200:
        return "Message envoyé à Pepper avec succès"
    else:
        return "Échec de l'envoi à Pepper"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


