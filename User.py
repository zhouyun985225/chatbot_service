# -*- coding: utf-8 -*-  
from chatbot import *

class User():
    def __init__(self, user_id):
        self.user_id = user_id
    
    def send_message_to_robot(self, message, robot):
        return robot.handle_question_from_user(self.user_id, message)
        
        