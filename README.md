# Chat application

This messaging app uses Socket.IO to communicate between clients and server. Users are signing in with their name. After that, they can create channels to communicate in or join existing ones. Inside a channel, users can do real-time messaging. They can also delete their messages, but not the messages of others.  

# Installation
You need to have Python 3.6 or higher and pip3 installed.

1. Download repository 

```bash
git clone https://github.com/lit-lucy/chat.git
```

2. In a terminal window, navigate into directory where file was cloned.

3. Run

```bash
pip3 install -r requirements.txt
```

4. Create and activate a virtual environment

```bash
python3 -m venv venv

. venv/bin/activate
```

5. Set up Flask application and run it.

```bash
export FLASK_APP=application.py

flask run
```

6. Navigate to URL provided by Flask. 
