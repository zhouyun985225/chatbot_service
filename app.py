from flask import Flask
import os
import socket
from wechat_service import robot
from flask import request
from environments import *
from werobot.contrib.flask import make_view
from chatbot import *
from User import *

app = Flask(__name__)
app.add_url_rule(rule='/robot/',  # WeRoBot 挂载地址
                 endpoint='werobot',  # Flask 的 endpoint
                 view_func=make_view(robot),
                 methods=['GET', 'POST'])


@app.route("/qa")
def qa():
    args = request.args
    user_id = args.get('userid')
    server_id = args.get('serverid')
    source = args.get('source')
    question = args.get('q')
    assert user_id != None and server_id != None and source != None and question != None, "Lack of parameters"
    user = User(user_id)
    robot = RobotService(server_id)
    answer = robot.handle_question_from_user(user.user_id, question)
    return answer


@app.route("/")
def hello():
    html = "<h3>Hello {name}!</h3>"
    return html.format(name=os.getenv("NAME", "world"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=CHATBOT_LISTENING_PORT)
