from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import datetime

# Action pour donner des directions dans l'hôpital
class ActionGiveDirections(Action):

    def name(self) -> Text:
        return "action_give_directions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot('location')
        
        # Exemple simplifié : ajout des directions pour les services
        if location == "cardiologie":
            response = "Le service de cardiologie se trouve au 2ème étage, à gauche de l'ascenseur."
        elif location == "radiologie":
            response = "Le service de radiologie est au rez-de-chaussée, à côté de l'accueil principal."
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
