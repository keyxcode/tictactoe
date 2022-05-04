from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)


@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    return render_template("game.html", game=session["board"], turn=session["turn"])


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    
    # Play a move
    session["board"][row][col] = session["turn"]

    # Winning Logic
    for i in range(3):
        for j in range(3):
            if session["board"][i][0] == session["board"][i][1] == session["board"][i][2] != None or \
               session["board"][0][j] == session["board"][1][j] == session["board"][2][j] != None or \
               session["board"][0][0] == session["board"][1][1] == session["board"][2][2] != None or\
               session["board"][2][0] == session["board"][1][1] == session["board"][0][2] != None:
               return render_template("winner.html", game=session["board"], turn=session["turn"])

    # Draw Logic
    draw = True
    for i in range(3):
        for j in range(3):
            if session["board"][i][j] == None:
                draw = False
                break
            else:
                continue
    if draw == True:
        return render_template("winner.html", game=session["board"])

    # Switch turn
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
             
    return redirect("/")


@app.route("/reset")
def reset():

    # Reset the game board
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    
    # Reset turn
    session["turn"] = "X"
    
    return redirect("/")
