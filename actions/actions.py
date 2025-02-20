from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3

class ActionGetHoraireVisite(Action):
    def name(self) -> str:
        return "action_get_horaire_visite"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        patient_name = tracker.get_slot("patient_name")
        if not patient_name:
            dispatcher.utter_message(text="Je n'ai pas pu récupérer le nom du patient. Veuillez réessayer.")
            return []

        horaires = self.get_horaire_visite_from_db(patient_name)

        if horaires:
            message = "Voici les horaires de visite pour le patient :\n"
            for horaire in horaires:
                message += f"Date : {horaire[0]}, de {horaire[1]} à {horaire[2]}\n"
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Désolé, je n'ai trouvé aucun horaire de visite pour ce patient.")

        return []

    def get_horaire_visite_from_db(self, patient_name):
        try:
            conn = sqlite3.connect('bdd/database.db')
            c = conn.cursor()
            c.execute('''
            SELECT date, start_time, end_time FROM horaires_visite WHERE patient_name = ?
            ''', (patient_name,))
            result = c.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"Erreur lors de la récupération des horaires de visite : {e}")
            return None

class ActionGetRendezvous(Action):
    def name(self) -> str:
        return "action_get_rendezvous"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        user_name = tracker.get_slot("user_name")
        if not user_name:
            dispatcher.utter_message(text="Je n'ai pas pu récupérer votre nom. Veuillez réessayer.")
            return []

        rendezvous = self.get_rendezvous_from_db(user_name)

        if rendezvous:
            dispatcher.utter_message(text=f"Votre rendez-vous est le {rendezvous[0]} à {rendezvous[1]} pour un service de {rendezvous[2]} avec {rendezvous[3]}.")
        else:
            dispatcher.utter_message(text="Désolé, je n'ai trouvé aucun rendez-vous pour vous.")

        return []

    def get_rendezvous_from_db(self, user_name):
        try:
            conn = sqlite3.connect('bdd/database.db')
            c = conn.cursor()
            c.execute('''
            SELECT date, time, service, doctor FROM rendezvous WHERE user_name = ?
            ''', (user_name,))
            result = c.fetchone()
            conn.close()
            return result
        except Exception as e:
            print(f"Erreur lors de la récupération des rendez-vous : {e}")
            return None
