# coding=utf8
import werobot
from environments import *
from User import *
from chatbot import *

robot = werobot.WeRoBot(enable_session=False,
                        token=WECHAT_TOKEN,
                        APP_ID=WECHAT_APP_ID,
                        APP_SECRET=WECHAT_APP_SECRET)


client = robot.client

@robot.text
def answerQuestion(message):
    source = message.source
    target = message.target
    question = message.content

    user = User(source)
    robot = RobotService(target)

    answer = user.send_message_to_robot(question, robot)
    return answer