
from flask import Flask, render_template, redirect
import json
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

USERS_FILE = "users.json"
LOG_FILE = "logs.txt"


# LOAD USERS
def load_users():
    with open(USERS_FILE, "r") as file:
        return json.load(file)


# SAVE USERS
def save_users(data):
    with open(USERS_FILE, "w") as file:
        json.dump(data, file, indent=4)


# WRITE LOGS
def write_log(username, action):
    timestamp = datetime.now(
    ZoneInfo("Asia/Kolkata")
).strftime("%d-%m-%Y %I:%M:%S %p")

    with open(LOG_FILE, "a") as file:
        file.write(f"{timestamp} | {username.upper()} | {action}\n")


# HOME PAGE
@app.route("/")
def home():
    users = load_users()
    return render_template("index.html", users=users)


# TRACK USER
@app.route("/view/<username>")
def track(username):
    users = load_users()

    if username in users:
        users[username]["status"] = True
        users[username]["timestamp"] = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M:%S %p")

        save_users(users)

        write_log(username, "STATUS TRUE")

    return redirect("/thankyou")


# RESET ALL STATUS
@app.route("/reset-all")
def reset_all():
    users = load_users()

    for user in users:
        users[user]["status"] = False

    save_users(users)

    write_log("SYSTEM", "ALL STATUS RESET")

    return redirect("/")
@app.route("/view/<username>")
def view_document(username):

    users = load_users()

    if username in users:

        users[username]["status"] = True

        users[username]["timestamp"] = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).strftime("%d-%m-%Y %I:%M:%S %p")

        save_users(users)

        write_log(username, "LINK OPENED")

    return render_template("thankyou.html")

# CLEAR LOGS
@app.route("/clear-logs")
def clear_logs():

    # CLEAR LOG FILE
    open(LOG_FILE, "w").close()

    # RESET ALL USERS
    users = load_users()

    for user in users:
        users[user]["status"] = False
        users[user]["timestamp"] = "--"

    save_users(users)

    return redirect("/")


# LOGS PAGE
@app.route("/logs")
def logs():

    grouped_logs = {}

    try:
        with open(LOG_FILE, "r") as file:
            lines = file.readlines()

        # latest logs first
        lines.reverse()

        for line in lines:
            parts = line.strip().split(" | ")

            if len(parts) == 3:
                timestamp, username, action = parts

                if username not in grouped_logs:
                    grouped_logs[username] = []

                grouped_logs[username].append({
                    "timestamp": timestamp,
                    "action": action
                })

    except FileNotFoundError:
        pass

    return render_template("logs.html", grouped_logs=grouped_logs)


# THANK YOU PAGE
@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


if __name__ == "__main__":
    app.run(debug=True)