import json
import time
from flask import Flask, Response, render_template

app = Flask(__name__)

messageList = [{"name" : "Aditya", "message" : "Me say Hi 😁"}]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/message/<name>/<message>')
def add_message(name, message):
    messageList.append({"name": name, "message" : message})
    print(messageList)
    return "message added", 200

@app.route("/stream")
def steam_chat():
    preMsg = None
    def response():
        while True:
            nonlocal preMsg
            currMsg = messageList[-1]
            if (currMsg != preMsg):
                preMsg = currMsg
                data = json.dumps(currMsg)
                yield f"data: {data}\nevent: message\n\n"
            time.sleep(0.5)
    return Response(response(), mimetype="text/event-stream")

@app.route('/broadcast')
def add_broadcast():
    return render_template("broadcaster.html") 

if (__name__ == "__main__"):
    app.run(debug=True, port=80)