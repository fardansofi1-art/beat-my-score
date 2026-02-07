from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DB="game.db"

def db():
    return sqlite3.connect(DB)

def init():
    con=db()
    cur=con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        score INTEGER DEFAULT 0
    )
    """)

    con.commit()
    con.close()

init()

@app.route("/")
def home():
    con=db()
    cur=con.cursor()

    cur.execute("SELECT name,score FROM players ORDER BY score DESC")
    leaderboard=cur.fetchall()

    con.close()

    return render_template("index.html", leaderboard=leaderboard)

@app.route("/submit",methods=["POST"])
def submit():
    name=request.form["name"]
    score=int(request.form["score"])

    con=db()
    cur=con.cursor()

    cur.execute("INSERT OR IGNORE INTO players(name) VALUES(?)",(name,))
    cur.execute("UPDATE players SET score=? WHERE name=?",(score,name))

    con.commit()
    con.close()

    return "ok"

@app.route("/reset_player",methods=["POST"])
def reset_player():
    name=request.form["name"]

    con=db()
    cur=con.cursor()
    cur.execute("UPDATE players SET score=0 WHERE name=?",(name,))
    con.commit()
    con.close()

    return "ok"

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
