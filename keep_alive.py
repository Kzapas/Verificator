from flask import *
from threading import Thread
import firebase_admin
from firebase_admin import db
import string
import random

app = Flask(__name__)


@app.route('/success', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))
        print("Your name is " + first_name + " " + last_name + ". Your code is: " + code)
        db.reference("/users").set({
        	code:
        	{
        		"fname": first_name,
            "lname": last_name
        	}
        })
    return render_template("success.html", value=code)


@app.route('/', methods=["GET", "POST"])
def gdg():
    return render_template("index.html")


def run():
    app.run(host='0.0.0.0', port=8080)

def startbot():
    t = Thread(target=run)
    t.start()
