from flask import Flask
import os
import socket
from chatbot import robot
from werobot.contrib.flask import make_view

app = Flask(__name__)
app.add_url_rule(rule='/robot/', # WeRoBot 挂载地址
                 endpoint='werobot', # Flask 的 endpoint
                 view_func=make_view(robot),
                 methods=['GET', 'POST'])

@app.route("/")
def hello():
    html = "<h3>Hello {name}!</h3>"
    return html.format(name=os.getenv("NAME", "world"))

if __name__ == "__main__":
    if os.getenv('ENVIRONMENT','development') == 'development':
        app.run(host='0.0.0.0', port=os.getenv("CHATBOT_LISTENING_PORT","80"))
    else:
        app.run(host='0.0.0.0', port=os.getenv("CHATBOT_LISTENING_PORT","8082"))
