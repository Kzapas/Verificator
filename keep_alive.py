from flask import *
from threading import Thread
import firebase_admin
from firebase_admin import db
import string
import random
import urllib.parse

app = Flask(__name__)

with open("settings.json", 'r', encoding='utf-8') as _settings_data:
    settings = json.load(_settings_data)

server_name = f"{settings['server_name']}"

@app.route('/success', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        discord_handle = str(request.form.get("dhandle"))
        discord_handle = urllib.parse.quote(discord_handle)
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        print("Your name is " + first_name + " " + last_name)
        db.reference("/users").set({
        	discord_handle:
        	{
        		"fname": first_name,
            "lname": last_name
        	}
        })
    return render_template("success.html")


@app.route('/', methods=["GET", "POST"])
def gdg():
    return render_template("index.html", value=server_name)


def run():
    app.run(host='0.0.0.0', port=8080)

def startbot():
    t = Thread(target=run)
    t.start()
