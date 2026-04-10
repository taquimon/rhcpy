# from cgi import print_form
import datetime
import sqlite3

from flask import flash
from flask import Flask
from flask import g
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from flask_login import login_user
from flask_login import LoginManager
from flask_login import logout_user
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.secret_key = "your_temporary_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect("rhc_database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", [user_id])
        user_data = cur.fetchone()
        if user_data:
            return User(user_data["id"], user_data["username"], user_data["password"])
    return None


@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        with sqlite3.connect("rhc_database.db") as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username = ?", [username])
            user_data = cur.fetchone()
            if user_data and check_password_hash(user_data["password"], password):
                user = User(
                    user_data["id"],
                    user_data["username"],
                    user_data["password"],
                )
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Invalid username or password")
                return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route("/<usr>", methods=["POST", "GET"])
def user(usr):
    return f"<h1>{usr}</h1>"


@app.route("/club", methods=["POST"])
@login_required
def club():
    club_name = ""
    if request.method == "POST":
        default_value = "0"

        club_name = request.form.get("club", default_value)
    print("Club: ", club_name)
    # players = read_json_file(club_name=club_name)
    players = get_players_from_db(club_name=club_name)
    print(players)
    for player in players:
        print("player: ", player)
        fecha_nac = (
            player["fechanacimiento"].replace("/", "-")
            if player["fechanacimiento"].find("/")
            else player["fechanacimiento"]
        )
        print(fecha_nac)
        age = calculate_age(fecha_nac)
        player["fechanacimiento"] = fecha_nac
        player["edad"] = age
        if age >= 50:
            player["bg"] = "bg-primary"
        else:
            player["bg"] = "bg-warning"

        name_pdf = (
            player["name"].replace(" ", "_").lower()
            + "_"
            + player["last"].replace(" ", "_").lower()
        )
        new_name_pdf = name_pdf.replace("ñ", "n")
        url_pdf = "static/resources/" + club_name.lower() + "/" + new_name_pdf + ".pdf"
        player["imagen"] = url_pdf
    print(players)
    # return render_template("player.html", players=players, club=club_name)
    return players


def calculate_age(birthdate):
    day, month, year = map(int, birthdate.split("-"))
    today = datetime.date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))

    return age


DATABASE = "rhc_database.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def create_table():
    conn = sqlite3.connect("rhc_database.db")
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
    conn.execute(
        "CREATE TABLE player(register TEXT,"
        "name TEXT, last TEXT, ci TEXT,"
        "fechanacimiento TEXT, parentesco TEXT, notas TEXT, club TEXT)",
    )
    print("Table created successfully")
    conn.close()


def create_users_table():
    conn = sqlite3.connect("rhc_database.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)",
    )
    print("Users table created successfully")
    conn.close()


@app.route("/new_player", methods=["GET", "POST"])
@login_required
def new_player():
    if request.method == "POST":
        try:
            name = request.form["name"]
            last = request.form["last"]
            ci = request.form["ci"]
            birthday = request.form["fechanacimiento"]
            parentesco = request.form["parentesco"]
            notes = request.form["notas"]
            club = request.form["club"]
            print(club)
            print(parentesco)
            with sqlite3.connect("rhc_database.db") as users:
                cursor = users.cursor()
                cursor.execute(
                    "INSERT INTO player \
                (name,last,ci,fechanacimiento,parentesco,notas,club) VALUES (?,?,?,?,?,?,?)",
                    (name, last, ci, birthday, parentesco, notes, club),
                )
                users.commit()
                message = "Jugador agregado correctamente"

        except Exception:
            users.rollback()
            message = "No se pudo agtegar el usuario"
        finally:
            users.close()
            return render_template("new_player.html", message=message)

    else:
        return render_template("new_player.html")


@app.route("/list_player", methods=["GET", "POST"])
@login_required
def list_player():
    with sqlite3.connect("rhc_database.db") as con:
        # con.row_factory = sqlite3.Row
        con.row_factory = dict_factory

        cur = con.cursor()
        cur.execute("SELECT rowid, * FROM player order by name")

        rows = cur.fetchall()

    for row in rows:
        fecha_nac = (
            row["fechanacimiento"].replace("/", "-")
            if row["fechanacimiento"].find("/")
            else row["fechanacimiento"]
        )
        row["edad"] = calculate_age(fecha_nac)
        row["bg"] = "bg-primary" if row["edad"] >= 50 else "bg-warning"

    print(rows)

    return render_template("list_player.html", players=rows)


@app.route("/search_ci")
@login_required
def search_ci():
    ci = request.args.get("ci", 0, type=str)
    with sqlite3.connect("rhc_database.db") as con:
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM player WHERE ci = ?", [ci])
        ci_found = cur.fetchall()

        if ci_found == []:
            ci_result = "CI no encontrado"
        else:
            name = ci_found[0]["name"]
            last = ci_found[0]["last"]
            ci_result = (
                f"CI: <b>{ci}</b> ya esta registrado a nombre de: <b>{name} {last}</b>"
            )

    return jsonify(result=ci_result)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def get_players_from_db(club_name=None):
    with sqlite3.connect("rhc_database.db") as con:
        con.row_factory = dict_factory

        cur = con.cursor()
        cur.execute(
            "SELECT * FROM player WHERE club = ? and gestion in ('2025') ORDER BY last",
            [club_name],
        )
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/player_card/<int:player_id>")
@login_required
def player_card(player_id):
    with sqlite3.connect("rhc_database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT * FROM player WHERE rowid = ?", [player_id])
        player = cur.fetchone()

    if not player:
        flash("Player not found")
        return redirect(url_for("list_player"))

    # Calculate age
    fecha_nac = (
        player["fechanacimiento"].replace("/", "-")
        if player["fechanacimiento"].find("/") != -1
        else player["fechanacimiento"]
    )
    player["fechanacimiento"] = fecha_nac
    player["edad"] = calculate_age(fecha_nac)

    # Generate PDF URL if exists
    name_pdf = (
        player["name"].replace(" ", "_").lower()
        + "_"
        + player["last"].replace(" ", "_").lower()
    )
    new_name_pdf = name_pdf.replace("ñ", "n")
    url_pdf = "static/resources/" + player["club"].lower() + "/" + new_name_pdf + ".pdf"
    player["imagen"] = url_pdf

    return render_template("player_card.html", player=player)


@app.route("/cards_by_club", methods=["GET", "POST"])
@login_required
def cards_by_club():
    """Display player cards grouped by club"""
    clubs_data = {}
    selected_club = None

    if request.method == "POST":
        selected_club = request.form.get("club", None)

    with sqlite3.connect("rhc_database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()

        # Get all unique clubs
        cur.execute(
            "SELECT DISTINCT club FROM player WHERE club IS NOT NULL ORDER BY club",
        )
        clubs = [row["club"] for row in cur.fetchall()]

        # If a specific club is selected, get players for that club
        if selected_club:
            cur.execute(
                "SELECT rowid, * FROM player WHERE club = ? ORDER BY last",
                [selected_club],
            )
            players = cur.fetchall()

            for idx, player in enumerate(players, 1):
                fecha_nac = (
                    player["fechanacimiento"].replace("/", "-")
                    if "/" in player["fechanacimiento"]
                    else player["fechanacimiento"]
                )
                player["fechanacimiento"] = fecha_nac
                player["edad"] = calculate_age(fecha_nac)

                # Generate registration number if not present
                if not player["register"]:
                    player["register"] = generate_registro(selected_club, idx)

                # Generate PDF URL if exists
                name_pdf = (
                    player["name"].replace(" ", "_").lower()
                    + "_"
                    + player["last"].replace(" ", "_").lower()
                )
                new_name_pdf = name_pdf.replace("ñ", "n")
                url_pdf = (
                    "static/resources/"
                    + player["club"].lower()
                    + "/"
                    + new_name_pdf
                    + ".pdf"
                )
                player["imagen"] = url_pdf

            clubs_data[selected_club] = players
        else:
            # Get all players grouped by club
            for club in clubs:
                cur.execute(
                    "SELECT rowid, * FROM player WHERE club = ? ORDER BY last",
                    [club],
                )
                players = cur.fetchall()

                for idx, player in enumerate(players, 1):
                    fecha_nac = (
                        player["fechanacimiento"].replace("/", "-")
                        if "/" in player["fechanacimiento"]
                        else player["fechanacimiento"]
                    )
                    player["fechanacimiento"] = fecha_nac
                    player["edad"] = calculate_age(fecha_nac)

                    # Generate registration number if not present
                    if not player["register"]:
                        player["register"] = generate_registro(club, idx)

                    # Generate PDF URL if exists
                    name_pdf = (
                        player["name"].replace(" ", "_").lower()
                        + "_"
                        + player["last"].replace(" ", "_").lower()
                    )
                    new_name_pdf = name_pdf.replace("ñ", "n")
                    url_pdf = (
                        "static/resources/"
                        + player["club"].lower()
                        + "/"
                        + new_name_pdf
                        + ".pdf"
                    )
                    player["imagen"] = url_pdf

                clubs_data[club] = players

    return render_template(
        "cards_by_club.html",
        clubs_data=clubs_data,
        clubs=clubs,
        selected_club=selected_club,
    )


def generate_registro(club_name, player_index):
    """Generate registration number based on club name (first 3 chars) and index"""
    if not club_name:
        return None
    club_prefix = club_name[:3].upper()
    return f"{club_prefix}-{player_index:03d}"


if __name__ == "__main__":
    create_users_table()
    # Create default user if not exists
    with sqlite3.connect("rhc_database.db") as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cur.fetchone():
            hashed_password = generate_password_hash("admin123")
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ("admin", hashed_password),
            )
            con.commit()
            print("Default user 'admin' created with password 'admin123'")
    app.run(debug=True)
