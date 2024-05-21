import datetime
    
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

@app.route("/<usr>", methods=['POST', 'GET'])
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route("/club", methods=['POST'])
def club():
    club_name = ''    
    if request.method == "POST":
        default_value = '0'
        
        club_name = request.form.get('club', default_value)
    print("Club: ", club_name)
    players = read_json_file(club_name=club_name)    
    print(players)
    for player in players:
        age = calculate_age(player['fechanacimiento'])
        player["edad"] = age
        if age >=50:
            player["bg"] = "bg-primary"
        else:
            player["bg"] = "bg-warning"
        
    print(players)
    return render_template("player.html", players=players, club=club_name)
    
def calculate_age(birthdate):

    
    day,month,year = map(int, birthdate.split("-"))
    today = datetime.date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    
    return age

if __name__ == "__main__":
    app.run(debug=True)