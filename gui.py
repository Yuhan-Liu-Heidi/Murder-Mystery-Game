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
    from server import error_messages
    error_msg = None
    if request.method == "POST":
        if request.form["action"] == "signup":
            signed_up = server.new_user(request.form["username"],
                                        request.form["psw"])
            if not signed_up:
                error_msg = error_messages[1]
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
                                        u_name=request.form["username"]))
    return render_template("login.html", error=error_msg)


@app.route("/<u_name>/choose_ch", methods=["GET", "POST"])
def choose_ch(u_name):
    import database
    if request.method == "POST":
        ch_name = request.form["choose_ch"]
        database.add_char(u_name, ch_name)
        return redirect(url_for("play", u_name=u_name, ch_name=ch_name))
    else:
        ch_name = server.verify_ch(u_name)
        if ch_name is str:
            return redirect(url_for("play", u_name=u_name, ch_name=ch_name))
        else:
            return render_template("choose_ch.html")


@app.route("/<u_name>/play/<ch_name>", methods=["GET", "POST"])
def play(u_name, ch_name):
    from database import user, game
    from server import error_messages
    message = None
    if request.method == "GET":
        ch = user[u_name]["char"]["name"]
        if ch_name == ch:
            message = {"u_name": u_name, "ch_name": ch_name}
            return render_template("play.html", msg_info=message)
        else:
            if ch_name in game['chars']:
                return error_messages[5]
            else:
                return error_messages[6]


if __name__ == "__main__":
    app.run(debug=True)
