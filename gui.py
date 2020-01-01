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


@app.route("/ch_names/")
def ch_names():
    return jsonify(ch_names=["良小花", "良星星", "米亚伦"])


@app.route("/is_chosen/")
def ch_chosen():
    from database import track
    return jsonify(ch1=track['chars']['良小花'],
                   ch2=track['chars']['良星星'],
                   ch3=track['chars']['米亚伦'],
                   ch4=True, ch5=True,
                   ch6=True, ch7=True, ch8=True, ch9=True, ch10=True)


@app.route("/<u_name>/choose_ch", methods=["GET", "POST"])
def choose_ch(u_name):
    if request.method == "POST":
        ch_name = request.form["choose_ch"]
        ch_added = server.new_ch(u_name, ch_name)
        if ch_added:
            return redirect(url_for("play", u_name=u_name, ch_name=ch_name))
        elif not ch_added:
            message = "此角色已被选择"
            return render_template("choose_ch.html", message=message)
        else:
            return redirect(url_for("play", u_name=u_name, ch_name=ch_added))
    else:
        ch_name = server.verify_ch(u_name)
        print(ch_name)
        if type(ch_name) == str:
            return redirect(url_for("play", u_name=u_name, ch_name=ch_name))
        else:
            return render_template("choose_ch.html")


@app.route("/<u_name>/play/<ch_name>", methods=["GET", "POST"])
def play(u_name, ch_name):
    from database import user, game
    from server import error_messages
    message = None
    if request.method == "GET":
        ch = user[u_name]["char"]
        if ch_name == ch:
            message = {"u_name": u_name, "ch_name": ch_name}
            return render_template("play.html", msg_info=message)
        else:
            if ch_name in game['chars']:
                return error_messages[5]
            else:
                return error_messages[6]


@app.route("/start_round1/")
def start_round1():
    from server import start_rnd
    from database import user
    name1 = request.args.get("name_ready_for_1")
    u_id = str(name1).lower()
    # Receive the names that are ready.
    check = start_rnd(1, u_id)
    print(check)
    if check:
        return jsonify(result="1")
    else:
        return jsonify(result="0")


@app.route("/vote_result/")
def vote_result():
    from server import calc_vote
    result = calc_vote()
    return result


@app.route("/final_result/")
def final_result():
    from server import verify_vote, calc_vote, verify_murderer
    vote_complete = verify_vote(1)
    if vote_complete:
        voted_murderer = calc_vote()
        [result, true_murderer] = verify_murderer(voted_murderer)
        return jsonify(revealed=True,
                       vote_murder=voted_murderer,
                       true_murder=true_murderer,
                       result=result)
    else:
        return jsonify(revealed=False, vote_murder=None, true_murder=None,
                       result=None)


@app.route("/ending/")
def ending():
    return render_template("ending.html")


if __name__ == "__main__":
    app.run(debug=True)
