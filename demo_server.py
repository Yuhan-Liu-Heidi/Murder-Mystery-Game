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
<<<<<<< HEAD:gui.py
            logged_in = server.verify_user(request.form["username"],
                                           request.form["psw"])
            if type(logged_in) == str:
                error_msg = logged_in
            elif logged_in:
                return redirect(url_for("choose_ch",
                                        uname=request.form["username"]))
    return render_template("login.html", error=error_msg)
=======
            if request.form["username"] != "lily" or \
                    request.form["psw"] != "123":
                error = "Invalid login please try again"
            else:
                return redirect(url_for("choose_ch",
                                        uname=request.form["username"]))
    return render_template("login.html", error=error)
>>>>>>> fa268e2f862cd1de28b07550c7794039ef601d1a:demo_server.py


@app.route("/<uname>/choose_ch", methods=["GET", "POST"])
def choose_ch(u_name):
    if request.method == "POST":
        ch_name = request.form["choose_ch"]
        chose_ch = server.assign_character(u_name, ch_name)
        if choose_ch:
            return redirect(url_for("play", uname=u_name, chname=ch_name))
        else:
            error_msg = chose_ch
            render_template("choose_ch.html", error=error_msg)
    else:
        return render_template("choose_ch.html")


@app.route("/<uname>/play/<chname>", methods=["GET", "POST"])
def play(uname, chname):
    if request.method == "GET":
        message = {"uname": uname, "chname": chname}
        return render_template("play.html", msg1=message)


if __name__ == "__main__":
    app.run(debug=True)
