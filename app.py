from flask import Flask, redirect, url_for, render_template, request

from helpers.rhc_helper import read_json_file

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route("/player/<club>")
def club(club):
    players = read_json_file(club_name=club)
    print(players[0])
    return render_template("player.html", players=players)
    

if __name__ == "__main__":
    app.run(debug=True)