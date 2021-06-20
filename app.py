from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_socketio import SocketIO, join_room, leave_room


app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/chat')
def chat():
    # Get the arguments from the request
    username= request.args.get('username') 
    room = request.args.get('room')

    if username and room:
        return render_template("chat.html", username=username, room=room)
    else:
        return redirect(url_for("home"))

#Join room
@socketio.on("join_room")
def handle_join_room_event(data):
    #app.logger.info <=> print, but add the date, and the logs can be stored
    app.logger.info("{} has joined the room {}".format(data["username"], data["room"]))
    join_room(data["room"])
    socketio.emit("join_room_announcement", data, room=data["room"])

#Leave room 
@socketio.on("leave_room")
def handle_leave_room_event(data):
        app.logger.info("{} has left the room {}".format(data["username"], data["room"]))
        leave_room(data["room"])
        socketio.emit("leave_room_announcement", data, room=data["room"])
        
#Send message
@socketio.on("send_message")
def handle_send_message(data):
        app.logger.info("{} has send a message to the room {}: {}".format(data["username"], data["room"], data["message"]))
        socketio.emit("receive_message", data, room=data["room"])




if __name__ == "__main__":
    socketio.run(app, debug=True)