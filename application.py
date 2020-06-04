# -*- coding: utf-8 -*-

# Import module 
from channel import *

import os

from flask import Flask, session, redirect, url_for, render_template, request
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__) 
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

 
@app.route("/")
def index():
    # Takes recently logged in user to the index page
    if "username" in session:
        username = session["username"]
        return render_template("index.html", username=username, channels=channels)

    # Asks new user to login
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    session["username"] = username

    return redirect(url_for("index"))

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()

    return render_template("login.html")

@app.route("/create_channel", methods=["POST"])
def create_channel():
    # Get channel name from user's input
    channel_name = request.form.get("channel_name")

    # Check if this channel name already exists
    if is_channel_exist(channel_name):
        return render_template("error.html", message="This channel name already exists")

    # Add channel
    channel_id = add_channel(channel_name)
    
    return redirect(url_for("channel", channel_id=channel_id))

@app.route("/channel/<channel_id>")
def channel(channel_id):
    # Check if channel_id exists
    if channel_id not in channels:
        return render_template("error.html", message="Channel doesn't exist")

    # Get all information for this channel (id, name, messages)
    channel = channels[channel_id]

    # Save current channel to user sessions 
    session["current_channel"] = channel_id

    return render_template("channel.html", channel=channel)

@socketio.on("joined")
def on_join():
    # Join socket room to send and recieve messages only inside this channel 
    username = session["username"]
    room = session["current_channel"]
    join_room(room)

    send(username + " has entered the room.", room=room)

@socketio.on("leave")
def on_leave():
    # Leave the socket room 
    username = session["username"]
    room = session["current_channel"]
    leave_room(room)

    send(username + " has left the room.", room=room)

@socketio.on("send message")
def send_message(data):
    # Get the name of current room
    room = session["current_channel"]
    channel_id = room

    # Get a text of message
    message_text = data["message"]
    username = session["username"]

    message = add_message(message_text, username, channel_id)

    emit("announce message", {"message": message}, room=room, broadcast=True)   

@socketio.on("delete message")
def delete_message(data):
    # Check if this message is from the logged user 
    channel_id = session["current_channel"]
    message_id = data["message_id"]

    if channels[channel_id]["messages"][message_id]["username"] != session["username"]:
        # Emit an event with notification that user can't delete this message
        # only to this user
        room = request.sid
        emit("user cant delete message", room=room)
    else:
        # Delete the message
        delete(channel_id, message_id)

        room = channel_id

        emit("deleted message", {"message_id": message_id}, room=room, broadcast=True)

