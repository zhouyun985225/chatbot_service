# coding=utf8
import werobot
from environments import *
from User import *
from chatbot import *

robot = werobot.WeRoBot(enable_session=False,
                        token=WECHAT_TOKEN,
                        APP_ID=WECHAT_APP_ID,
                        APP_SECRET=WECHAT_APP_SECRET)


RobotService("") #preload the QA

@robot.text
def answerQuestion(message):
    source = message.source
    target = message.target
    question = message.content

    user = User(source)
    robot = RobotService(target)

    answer = robot.handle_question_from_user(user.user_id, question)
    return answer


