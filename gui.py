from flask import Flask, render_template, redirect, url_for, request, jsonify
import server


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        return redirect(url_for("login"))
    else:
        return render_template("welcome.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = None
    if request.method == "POST":
        if request.form["action"] == "signup":
            signed_up = server.new_user(request.form["username"],
                                        request.form["psw"])
            if not signed_up:
                error_msg = "The user has existed"
            else:
                message = "You've signed up"
                return render_template("login.html", msg1=message)
        elif request.form["action"] == "login":

            logged_in = server.verify_user(request.form["username"],
                                           request.form["psw"])
            if type(logged_in) == str:
                error_msg = logged_in
            elif logged_in:
                return redirect(url_for("choose_ch",
                                        uname=request.form["username"]))
    return render_template("login.html", error=error_msg)


@app.route("/<uname>/choose_ch", methods=["GET", "POST"])
def choose_ch(uname):
    import database
    if request.method == "GET":
        chname = server.verify_ch(uname)
        if chname is str:
            return redirect(url_for("play", uname=uname, chname=chname))
    if request.method == "POST":
        chname = request.form["choose_ch"]
        database.assign_character(uname, chname)
        return redirect(url_for("play", uname=uname, chname=chname))
    else:
        return render_template("choose_ch.html")


@app.route("/<uname>/play/<chname>", methods=["GET", "POST"])
def play(uname, chname):
    # from database import game
    if request.method == "GET":
        message = {"uname": uname, "chname": chname}
        return render_template("play.html", msg1=message)


def search_clue(n_rnd):
    pass


if __name__ == "__main__":
    app.run(debug=True)
