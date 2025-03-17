import urllib2
import json
import random
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        # serveur rasa : rasa run -m models --enable-api --cors “*” --debug
        self.url = 'http://192.168.1.70:5005/webhooks/rest/webhook/'
        self.text = "Bonjour je suis à votre disposition." #None
        self.newCall = True


    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        if (self.newCall):
            #response = self.rasa_call(self.url, '/restart') #TODO: Rasa can be restarted
            self.onRasaResponse(self.text)
            self.newCall = False
        self.onStopped()

    def onInput_RasaRequest(self, text=None):
        self.text = text
        if (self.text.startswith('au revoir')):
            self.onBye("Au revoir, merci")
        else:
            response = self.rasa_call(self.url, self.text)
            r = json.loads(response.body)
            if (r):
                r = r[0]['text'].encode("UTF-8")
                if (r.startswith('au revoir')):
                    self.onBye("Au revoir, merci")
                else:
                    self.onRasaResponse(r)
            else:
                self.onRasaResponse("Je reste coi")
        self.onStopped()


    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped

    def rasa_call(self, url, text):
        # url : l'url à contacter, avec le '/' final (nromalement de la forme http://<IP>:8082/)
        # text : ce que la personne demande à rasa
        data = '{"sender":"nao", "message":"' + text + '"}'

        req = urllib2.Request(url, data=data)
        f = urllib2.urlopen(req)
        class Response:
            pass
        response = Response()
        response.code = f.getcode()
        response.body = f.read()
        return response