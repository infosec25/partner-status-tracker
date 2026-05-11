from flask import Flask, render_template, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "users.json"
LOG_FILE = "logs.txt"

# Default users
default_data = {
    "ASHISH": {
        "status": False,
        "last_click": "Never"
    },
    "VARUN": {
        "status": False,
        "last_click": "Never"
    },
    "RITESH": {
        "status": False,
        "last_click": "Never"
    },
    "UTKARSH": {
        "status": False,
        "last_click": "Never"
    }
}

# Create users.json if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        json.dump(default_data, file, indent=4)

# Create logs.txt if not exists
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()

# Read user data
def get_data():
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Save user data
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Save logs
def save_log(username, action):

    time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    log_entry = f"{time_now} | {username} | {action}\n"

    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

# Homepage
@app.route("/")
def home():

    users = get_data()

    return render_template("index.html", users=users)

# Track route
@app.route("/track/<username>")
def track(username):

    users = get_data()

    username = username.upper()

    if username in users:

        users[username]["status"] = True

        users[username]["last_click"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        save_data(users)

        save_log(username, "TRUE")

    return redirect("/")

# Reset route
@app.route("/reset/<username>")
def reset(username):

    users = get_data()

    username = username.upper()

    if username in users:

        users[username]["status"] = False

        save_data(users)

        save_log(username, "RESET")

    return redirect("/")

# Logs page
@app.route("/logs")
def logs():

    with open(LOG_FILE, "r") as file:
        log_data = file.readlines()

    log_data.reverse()

    return render_template("logs.html", logs=log_data)

if __name__ == "__main__":
    app.run(debug=True, port=8000)