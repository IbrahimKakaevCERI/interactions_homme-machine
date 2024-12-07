from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import datetime

class ActionGiveDirections(Action):
    def name(self) -> str:
        return "action_give_directions"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot('location')

        # Exemple simplifié : ajout des directions pour les services
        if location == "cardiologie":
            response = "Le service de cardiologie se trouve au 2ème étage, à gauche de l'ascenseur."
        elif location == "radiologie" or location == "radios":
            response = "Le service de radiologie est au rez-de-chaussée, à côté de l'accueil principal."
        elif location == "urgence":
            response = "La salle d'urgence est au 1er étage, juste à côté de l'entrée principale."
        else:
            response = f"Je ne connais pas l'emplacement du service {location}. Veuillez vous renseigner à l'accueil."
            
        dispatcher.utter_message(text=response)

        return []

# Action pour rappeler un rendez-vous
class ActionCheckAppointment(Action):

    def name(self) -> Text:
        return "action_check_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        appointment_date = tracker.get_slot('appointment_date')

        if appointment_date:
            response = f"Vous avez un rendez-vous prévu le {appointment_date}."
        else:
            response = "Je ne trouve pas de rendez-vous à venir. Voulez-vous vérifier une autre date?"

        dispatcher.utter_message(text=response)

        return []

# Action pour fournir les horaires de visite
class ActionProvideVisitingHours(Action):

    def name(self) -> Text:
        return "action_provide_visiting_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = "Les horaires de visite sont de 10h à 18h tous les jours."
        dispatcher.utter_message(text=response)

        return []

# Action pour donner les consignes d'hygiène
class ActionProvideHygieneRules(Action):

    def name(self) -> Text:
        return "action_provide_hygiene_rules"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = "Merci de respecter les règles d'hygiène : port du masque obligatoire et désinfection des mains à l'entrée."
        dispatcher.utter_message(text=response)

        return []

# Action pour raconter une blague
class ActionTellJoke(Action):

    def name(self) -> Text:
        return "action_tell_joke"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        joke = "Pourquoi les ordinateurs détestent les hôpitaux ? Parce qu'ils attrapent des virus !"
        dispatcher.utter_message(text=joke)

        return []

# Action pour checker les rdv
class ActionCheckRendezvous(Action):
    def name(self) -> str:
        return "action_check_rendezvous"

    def run(self, dispatcher, tracker, domain):
        user_name = tracker.get_slot('user_name')  # On suppose que le nom de l'utilisateur est dans un slot

        # Récupérer le rendez-vous de l'utilisateur depuis la base de données
        rendezvous = self.get_rendezvous(user_name)

        if rendezvous:
            date, time = rendezvous
            response = f"Vous avez un rendez-vous prévu pour le {date} à {time}."
        else:
            response = "Vous n'avez pas de rendez-vous prévu aujourd'hui."

        dispatcher.utter_message(text=response)
        return []

    def get_rendezvous(self, user_name):
        # Connexion à la base de données SQLite et récupération du rendez-vous
        conn = sqlite3.connect('rasa.db')
        c = conn.cursor()
        c.execute('''SELECT date, time FROM rendezvous WHERE user_name = ?''', (user_name,))
        result = c.fetchone()
        conn.close()
        return result

