# coding=utf8
import werobot
from environments import *
from User import *
from chatbot import *

robot = werobot.WeRoBot(enable_session=False,
                        token=WECHAT_TOKEN,
                        APP_ID=WECHAT_APP_ID,
                        APP_SECRET=WECHAT_APP_SECRET)

RobotService("")  # preload the QA


@robot.text
def answerQuestion(message):
    source = message.source
    target = message.target
    question = message.content

    user = User(source)
    robot = RobotService(target)

    answer = robot.handle_question_from_user(user.user_id, question)
    # 微信公众号规定，采用UTF-8编码方式，文本消息内容最多2047个字节
    if len(answer) > 680:
         return answer[0:680]
    else:
        return answer

@robot.subscribe
def subscribe(message):
    return "小主您好！我是小谱，很高兴能伴您左右，为您答疑解惑，一起战胜疾病！我也在不断学习成长中，目前只擅长《16病区放化疗宣教手冊》和就医流程相关的知识哦。有什么不懂的就随时问我吧。\n为了更精准的为您解疑答惑，请告诉小谱您想咨询的是放射治疗（放疗）还是化学药物治疗（化疗）？\n请选择: 1 放疗  2 化疗"