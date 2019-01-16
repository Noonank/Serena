#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from message import Message
import random

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

INTENT_BONJOUR_ = "Noona-nk:Bonjour_"
INTENT_REPONSE_1 = "Noona-nk:Reponse_1"
INTENT_STOP_DIALOG = "Noona-nk:stopDialog"
INTENT_JE_NE_SAIS_PAS = "Noona-nk:JeNeSaisPas"

INTENT_FILTER_GET_ANSWER = [
    INTENT_REPONSE_1,
    INTENT_STOP_DIALOG,
    INTENT_JE_NE_SAIS_PAS
]

SKILL_MESSAGES = {
    'fr': {
        "Demande" : [
            "Salut! ça va?",
            "Hello, tout va bien?", 
            "Hey! Comment va-tu aujoud'hui",
            "Bonjour, comment te sens-tu aujourd'hui"
        ],
        "Fatigué": "Ah bon?, As-tu mal dormis?",
        "Bonne_santé": "Très bien, n'oublie pas de bien t'hydrater",
        "Sommeil": "Tu devrais dormir plus.",
        "Assistantgenial": "Avec plaisir, je suis à ton service",
        "Faim?": "As-tu faim?",
        "Faim_oui": "Va manger quelque chose mais attention evite de grignoter entre les repas.",
        "RAV": "Je ne peux rien faire pour toi, j'appel ton medecin.",
        "No_answer" : "tu ne reponds pas... tout va bien?",
        "stopGame" : "On s'arrete la, prend soin de toi"        
    }
}


class Serena:
    def __init__(self):
        self.__current_answer = ""
        # self.__current_table = 0
        # self.__current_multiplier = 0
        # self.__score = 0
        # self.__multipliers = []
        self.__message = Message(SKILL_MESSAGES, 'fr')

    def user_request_assistant(self, hermes, intent_message):
        print("L'utilisateur lance l'assistant")
        if intent_message.slots.bonjour:
            sentence = self.__message.get('Demande')
            print(sentence)
            hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_ANSWER)

                
    def user_reponse_1(self, hermes, intent_message):
        if intent_message.slots.reponse:
            reponse = intent_message.slots.reponse
            if answer == "oui":
                hermes.publish_end_session(intent_message.session_id, self.__message.get('Bonne_santé'))
                # hermes.publish_start_session_action('default', self.new_multiplication(), INTENT_FILTER_GET_ANSWER, True, '')

            elif answer == "non":
                hermes.publish_end_session(intent_message.session_id, self.__message.get('Fatigué'))
                # hermes.publish_start_session_action('default', self.new_multiplication(), INTENT_FILTER_GET_ANSWER, True, '')


    def user_ne_repond_pas(self, hermes, intent_message):
        if self.__current_answer == "":
            hermes.publish_end_session(intent_message.session_id, self.__message.get('No_answer'))
            # hermes.publish_start_session_action('default', self.new_multiplication(), INTENT_FILTER_GET_ANSWER, True, '')

    def user_stop_dialog(self, hermes, intent_message):
        if self.__current_table == 0:
            hermes.publish_end_session(intent_message.session_id, "")
            
        hermes.publish_end_session(intent_message.session_id, self.__message.get('stopGame').format(self.__score))


    def start(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intent(INTENT_BONJOUR_, self.user_request_assistant) \
                .subscribe_intent(INTENT_STOP_DIALOG, self.user_stop_dialog) \
                .subscribe_intent(INTENT_JE_NE_REPOND_PAS, self.user_ne_repond_pas) \
                .subscribe_intent(INTENT_REPONSE_1, self.user_reponse_1) \
                .start()
                

if __name__ == "__main__":
    game = Serena()
    game.start()
