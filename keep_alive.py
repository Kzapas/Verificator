from flask import *
from threading import Thread
import firebase_admin
from firebase_admin import db
import string
import random
import urllib.parse

app = Flask(__name__)

@app.route('/success', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        discord_handle = str(request.form.get("dhandle"))
        discord_handle = urllib.parse.quote(discord_handle)
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        db.reference("/users").push({
        	discord_handle:
        	{
        		"firstname": first_name,
            "lastname": last_name,
            "email": email,
            "phone":phone
        	}
        })
    return render_template("success.html")


@app.route('/', methods=["GET", "POST"])
def gdg():
    return "Cannot GET"


def run():
    app.run(host='0.0.0.0', port=8080)

def startbot():
    t = Thread(target=run)
    t.start()
