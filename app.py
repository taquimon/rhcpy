# from cgi import print_form
import datetime
from email import message
import json
import re
import sqlite3
from flask import g
    
from flask import Flask, redirect, url_for, render_template, request, jsonify

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
    # players = read_json_file(club_name=club_name)
    players = get_players_from_db(club_name=club_name)
    print(players)
    for player in players:
        print("player: ", player)
        fecha_nac = player['fechanacimiento'].replace('/','-') if player['fechanacimiento'].find('/') else player['fechanacimiento']
        print(fecha_nac)
        age = calculate_age(fecha_nac)
        player["fechanacimiento"] = fecha_nac
        player["edad"] = age
        if age >=50:
            player["bg"] = "bg-primary"
        else:
            player["bg"] = "bg-warning"
        
        name_pdf = player['name'].replace(" ", "_").lower() + "_" + player['last'].replace(" ", "_").lower()
        new_name_pdf = name_pdf.replace("ñ", "n")
        url_pdf = "static/resources/" + club_name.lower() + "/" + new_name_pdf + ".pdf"
        player["imagen"] = url_pdf
    print(players)
    #return render_template("player.html", players=players, club=club_name)
    return players
    
def calculate_age(birthdate):

    
    day,month,year = map(int, birthdate.split("-"))
    today = datetime.date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    
    return age




DATABASE = "rhc_database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def create_table():
    conn = sqlite3.connect('rhc_database.db')
    print("Opened database successfully")
    # "registro": "BOT-172",
    #     "name": "Efrain",
    #     "last": "Bustamante Molina",
    #     "ci": "3042703",
    #     "fechanacimiento": "10-04-1966",
    #     "parentesco": "HUANUNEÑO",
    #     "ci_image": "",
    #     "notas": "",
    #     "club": "Botafogo"
    conn.execute("CREATE TABLE player(register TEXT," \
                "name TEXT, last TEXT, ci TEXT," \
                "fechanacimiento TEXT, parentesco TEXT, notas TEXT, club TEXT)")
    print("Table created successfully")
    conn.close()


@app.route('/new_player', methods=['GET', 'POST']) 
def new_player(): 
    if request.method == 'POST': 
        try:
            name = request.form['name'] 
            last = request.form['last'] 
            ci = request.form['ci'] 
            birthday = request.form['fechanacimiento'] 
            parentesco = request.form['parentesco'] 
            notes = request.form['notas']
            club =  request.form['club']
            print(club)
            print(parentesco)
            with sqlite3.connect("rhc_database.db") as users: 
                cursor = users.cursor() 
                cursor.execute("INSERT INTO player \
                (name,last,ci,fechanacimiento,parentesco,notas,club) VALUES (?,?,?,?,?,?,?)", 
                (name, last, ci, birthday, parentesco, notes, club))
                users.commit()
                message = "Jugador agregado correctamente"
            
        except Exception:
            users.rollback()
            message = "No se pudo agtegar el usuario"
        finally:
            users.close()
            return render_template("new_player.html", message=message)
            
    else: 
        return render_template('new_player.html') 


@app.route('/list_player', methods=['GET', 'POST'])
def list_player():
    
    with sqlite3.connect("rhc_database.db") as con:
        #con.row_factory = sqlite3.Row
        con.row_factory = dict_factory

        cur = con.cursor()
        cur.execute("SELECT * FROM player order by name")

        rows = cur.fetchall()
    
    for row in rows:
        fecha_nac = row['fechanacimiento'].replace('/','-') if row['fechanacimiento'].find('/') else row['fechanacimiento']
        row['edad'] = calculate_age(fecha_nac)
        row['bg'] = "bg-primary" if row['edad'] >= 50 else "bg-warning"
        
    print(rows)
    
    return render_template("list_player.html", players=rows)


@app.route('/search_ci')
def search_ci():
    ci = request.args.get('ci', 0 , type=str)    
    with sqlite3.connect("rhc_database.db") as con:
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM player WHERE ci = ?", [ci])
        ci_found = cur.fetchall()
                
        if ci_found == []:
            ci_result = "CI no encontrado"
        else:
            name = ci_found[0]['name']
            last = ci_found[0]['last']
            ci_result = f"CI: <b>{ci}</b> ya esta registrado a nombre de: <b>{name} {last}</b>"

    return jsonify(result=ci_result)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_players_from_db(club_name=None):

    with sqlite3.connect("rhc_database.db") as con:
        con.row_factory = dict_factory

        cur = con.cursor()
        cur.execute("SELECT * FROM player WHERE club = ? and gestion = '2024' ORDER BY last", [club_name])
        club_found = cur.fetchall()


    return club_found

def get_players_from_db_all(club_name=None):

    with sqlite3.connect("rhc_database.db") as con:
        con.row_factory = dict_factory

        cur = con.cursor()
        cur.execute("SELECT * FROM player WHERE club = ? order by last", [club_name])
        club_found = cur.fetchall()


    return club_found


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

if __name__ == "__main__":
    app.run(debug=True)