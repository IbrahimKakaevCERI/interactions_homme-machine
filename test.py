from naoqi import ALProxy

# Connexion à l'API NAOqi de Pepper
tts = ALProxy("ALTextToSpeech", "192.168.13.63", 9559)

# Tester la parole de Pepper
tts.say("Bonjour, je suis Pepper !")
