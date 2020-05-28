# -*- coding: utf-8 -*-

import os
# To generate uuid
import uuid

from collections import OrderedDict 

from flask import Flask, session, redirect, url_for, render_template, request
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room, send

from datetime import datetime

app = Flask(__name__) 
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True 
app.config["SESSION_TYPE"] = "filesystem"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #?? Is it right?
Session(app)

# A dictionary of all channels with messages.
# each channel stores no more than 100 messages.
channels = {} 
# Mapping channel id to its name
channels_ids = {}

@app.route("/")
def index():
    # Takes recently logged in user to the index page
    if "username" in session:
        username = session["username"]
        return render_template("index.html", username=username, channels_ids=channels_ids)

    # Asks new user to login
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    session["username"] = username

    return redirect(url_for("index"))

@app.route("/change_username", methods=["GET"])
def change_username():
    return render_template("login.html")

@app.route("/create_channel", methods=["POST"])
def create_channel():
    # Get channel name from user's input
    channel_name = str(request.form.get("channel_name"))

    # Check if this channel name already exists
    if channel_name in channels_ids.values():
        return render_template("error.html", message="This channel name already exists")

    # Generate a random channel id
    channel_id = uuid.uuid4()
    channel_id = str(channel_id)

    # Map channel id to its name
    channels_ids[channel_id] = channel_name

    # Initiate an ordered dictionary of messages for this channel
    message_dict = OrderedDict()
    channels[channel_id] = message_dict
    
    return redirect(url_for("channel", channel_id=channel_id))

@app.route("/channel/<channel_id>")
def channel(channel_id):
    try:
        # Get dictionary of messages for this channel
        messages = channels[channel_id]

        # Save current channel to user sessions 
        session["current_channel"] = channel_id

        channel_name = channels_ids[channel_id]
    except KeyError:
        return render_template("error.html", message="something went wrong")

    return render_template("channel.html", channel_name=channel_name, messages=messages)

@socketio.on("joined")
def on_join():
    # Join socket room to send and recieve messages only inside this channel 
    username = session["username"]
    room = session["current_channel"]
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on("leave")
def on_leave():
    # Leave the socket room 
    username = session["username"]
    room = session["current_channel"]
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on("send message")
def send_message(data):
    # Get the name of current room
    room = session["current_channel"]
    channel_id = room

    # Generate a message id
    message_id  = uuid.uuid4()
    message_id = str(message_id)

    # Compile a message
    message_text = data["message"]

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = {"message_text": message_text, "username": session["username"], "time": time}

    # Check is there already 100 messages in this channel
    # and delete if necessary 

    while len(channels[channel_id]) >= 100:
        # Delete the first message (FIFO)
        channels[channel_id].popitem(0)

    # Add message id and message to ordered dictionary    

    channels[channel_id][message_id] = message

    emit("announce message", {"message": message, "message_id": message_id}, room=room, broadcast=True)   

@socketio.on("delete message")
def delete_message(data):
    # Check if this message is from the logged user 
    channel_id = session["current_channel"]
    message_id = data["message_id"]

    if channels[channel_id][message_id]["username"] != session["username"]:
        # Emit an event with notification that user can't delete this message
        # only to this user
        room = request.sid
        emit("user cant delete message", room=room)
    else:
        # Delete the message
        channels[channel_id].pop(message_id)

        room = channel_id

        emit("deleted message", {"message_id": message_id}, room=room, broadcast=True)
