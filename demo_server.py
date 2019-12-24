from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        return redirect(url_for("login"))
    else:
        return render_template("welcome.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    message = None
    # Hard coding!!!!!
    user_existing = False
    if request.method == "POST":
        if request.form["action"] == "signup":
            if user_existing is True:
                error = "The user has existed"
            else:
                message = "You've signed up"
                return render_template("login.html", msg1=message)
        elif request.form["action"] == "login":
            if request.form["username"] != "lily" or request.form["psw"] != "123":
                error = "Invalid login please try again"
            else:
                return redirect(url_for("choose_ch", uname=request.form["username"]))
    return render_template("login.html", error=error)


@app.route("/<uname>/choose_ch", methods=["GET", "POST"])
def choose_ch(uname):
    if request.method == "POST":
        # check if user has chosen one ch or if it matches to the chosen one
        chname = request.form["choose_ch"]
        return redirect(url_for("play", uname=uname, chname=chname))
    else:
        return render_template("choose_ch.html")


@app.route("/<uname>/play/<chname>", methods=["GET", "POST"])
def play(uname, chname):
    if request.method == "GET":
        message = {"uname": uname, "chname": chname}
        return render_template("play.html", msg1=message)


if __name__ == "__main__":
    app.run(debug=True)
