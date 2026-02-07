from flask import Flask, render_template, request
import os

app = Flask(__name__)

def get_scores():
    if not os.path.exists("scores.txt"):
        return []

    players = []

    with open("scores.txt") as f:
        for line in f:
            if "," in line:
                name, score = line.strip().split(",")
                players.append({"name": name, "score": int(score)})

    players.sort(key=lambda x: x["score"], reverse=True)

    # First is winner, rest losers
    for i, p in enumerate(players):
        if i == 0:
            p["status"] = "winner"
        else:
            p["status"] = "loser"

    return players[:10]

@app.route("/")
def home():
    leaderboard = get_scores()
    return render_template("index.html", leaderboard=leaderboard)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"].strip()
    score = request.form["score"]

    if name == "":
        name = "Anonymous"

    players = {}

    if os.path.exists("scores.txt"):
        with open("scores.txt") as f:
            for line in f:
                if "," in line:
                    n,s = line.strip().split(",")
                    players[n] = s   # overwrite old

    # overwrite this player's score
    players[name] = score

    # write back CLEAN file
    with open("scores.txt","w") as f:
        for n,s in players.items():
            f.write(f"{n},{s}\n")

    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)





