#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from message import Message
import random

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


INTENT_REPONSE__1 = "Noona-nk:Reponse_1"
INTENT_BONJOUR__ = "Noona-nk:Bonjour_"
# INTENT_STOP_QUIZ = "alrouen:stopQuiz"
# INTENT_DOES_NOT_KNOW = "alrouen:iDoNotKnow"

INTENT_FILTER_GET_ANSWER = [
    INTENT_REPONSE__1
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
        "No_answer" : "tu ne reponds pas... tout va bien?"
        # 'stopGame': 
        #     "Ok, on arrête là. Ton score est de {} point. A bientôt.",
        #     "Ok, ton score est de {} point. Merci d'avoir jouer."
        
    }
}

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


# def action_wrapper(hermes, intentMessage, conf):
#     liste_reponses = ["Salut! ça va?","Hello, tout va bien?", "Hey! Comment va-tu aujoud'hui","Hi, comment te sens-tu aujourd'hui"]
    

    index_reponse = random.randint(0,len(liste_reponses))
    
    result_sentence = liste_reponses[index_reponse]
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)



    # def start(self):
    #     with Hermes(MQTT_ADDR) as h:
    #         h.subscribe_intent(INTENT_START_MULTIPLICATIONTABLE_QUIZ, self.user_request_quiz) \
    #             .subscribe_intent(INTENT_STOP_QUIZ, self.user_quits) \
    #             .subscribe_intent(INTENT_DOES_NOT_KNOW, self.user_does_not_know) \
    #             .subscribe_intent(INTENT_GIVE_ANSWER, self.user_gives_answer) \
    #             .start()



# if __name__ == "__main__":
#     with Hermes("localhost:1883") as h:
#         h.subscribe_intent("Noona-nk:Bonjour_", subscribe_intent_callback) \
#          .start()
         

class Serena:
    def __init__(self):
        # self.__current_table = 0
        # self.__current_multiplier = 0
        # self.__score = 0
        # self.__multipliers = []
        self.__message = Message(SKILL_MESSAGES, 'fr')


  ###     def new_multiplication(self):
    #     self.__current_multiplier = self.new_multiplier()
    #     return self.__message.get('newMultiplication').format(self.__current_table, self.__current_multiplier)

    def user_request_assistant(self, hermes, intent_message):
        print("L'utilisateur lance l'assistant")


        sentence = self.__message.get('Demande').format(self.__current_table)
        hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_ANSWER)

            # else:
            #     hermes.publish_end_session(intent_message.session_id, self.__message.get('invalidTable'))
                

    def user_reponse_1(self, hermes, intent_message):
        # if self.__current_table == 0:
        #     hermes.publish_continue_session(intent_message.session_id, self.__message.get('noTable'), [INTENT_START_MULTIPLICATIONTABLE_QUIZ])

        # if intent_message.slots.answer:
        answer = intent_message
        # result = self.__current_multiplier * self.__current_table

        # self.__multipliers.remove(self.__current_multiplier)

        if answer == "fatigue":
            # self.__score = self.__score + 1

            # if len(self.__multipliers) > 0:
            hermes.publish_end_session(intent_message.session_id, self.__message.get('Fatigué'))
            hermes.publish_start_session_action('default', self.new_multiplication(), INTENT_FILTER_GET_ANSWER, True, '')
            # else:
            #     hermes.publish_end_session(intent_message.session_id, self.__message.get('tableFinished').format(self.__score))


        elif answer == "Bien":
            answer = intent_message
            hermes.publish_end_session(intent_message.session_id, self.__message.get('Bonne_santé'))
            hermes.publish_start_session_action('default', self.new_multiplication(), INTENT_FILTER_GET_ANSWER, True, '')

        else:
            hermes.publish_continue_session(intent_message.session_id, self.__message.get('No_answer'), [INTENT_START_MULTIPLICATIONTABLE_QUIZ])
            
                
                    # hermes.publish_end_session(intent_message.session_id, self.__message.get('wrongAnswer'))
                    # hermes.publish_start_session_action('default', self.new_multiplication(), INTENT_FILTER_GET_ANSWER, True, '')
                    


    def start(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intent(INTENT_BONJOUR__, self.user_request_assistant) \
                .subscribe_intent(INTENT_REPONSE__1, self.user_reponse_1) \
                .start()


if __name__ == "__main__":
    game = Serena()
    game.start()

