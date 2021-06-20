from flask_login.utils import login_required, login_user, logout_user
from db import get_user
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_socketio import SocketIO, join_room, leave_room
from flask_login import LoginManager, current_user
from user import User
from dotenv import dotenv_values

config = dotenv_values(".env")

app = Flask(__name__)
app.secret_key=config["SECRET_KEY"]
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = "login" #used to redirect on login when @login_required
login_manager.init_app(app)



@app.route("/")
def home():
    return render_template("index.html")

@app.route('/chat')
@login_required
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

#LOGIN

#check if the user is present in the DB an return None if not
@login_manager.user_loader
def load_user(username):
    return get_user(username)

#login route
@app.route("/login", methods=["GET", "POST"])
def login():

    #if already logged in, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    message=''
    if request.method=="POST":
        username = request.form.get("username")
        password_input = request.form.get("password")
        user = get_user(username)
        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for("home"))
        else:
            message= 'Failed to login! please try again...'
    return render_template("login.html", message=message)

#LOGOUT

#logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    socketio.run(app, debug=True)