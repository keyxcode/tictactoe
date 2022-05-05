from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

#======================================================================
@app.route("/")
def index():

    # Initialize gameboard, turn and undo manager
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["undo"] = []

    return render_template("game.html", game=session["board"], turn=session["turn"], undo=session["undo"])


#======================================================================
@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    
    # Play a move
    session["board"][row][col] = session["turn"]

    # Store the last move in undo manager
    session["undo"].append([row, col])

    # If someone wins -> Winning Logic
    for i in range(3):
        for j in range(3):
            if session["board"][i][0] == session["board"][i][1] == session["board"][i][2] != None or \
               session["board"][0][j] == session["board"][1][j] == session["board"][2][j] != None or \
               session["board"][0][0] == session["board"][1][1] == session["board"][2][2] != None or\
               session["board"][2][0] == session["board"][1][1] == session["board"][0][2] != None:
               return render_template("winner.html", game=session["board"], turn=session["turn"])

    # If it's a draw -> Draw Logic
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

    # If no one wins yet -> Switch turn
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
             
    return redirect("/")


#======================================================================
@app.route("/reset")
def reset():

    # Reset the game board
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    
    # Reset turn
    session["turn"] = "X"

    # Reset undo manager
    session["undo"] = []
    
    return redirect("/")


#======================================================================
@app.route("/undo")
def undo():

    # Undo a move
    if len(session["undo"]) > 0:
        lastMove = len(session["undo"]) - 1
        row = session["undo"][lastMove][0]
        col = session["undo"][lastMove][1]

        session["board"][row][col] = None

        # Remove the last move in the undo manager
        session["undo"].pop()

        # Revert play turn
        if session["turn"] == "X":
            session["turn"] = "O"
        else:
            session["turn"] = "X"
    
    return redirect("/")
