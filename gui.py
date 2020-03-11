from flask import Flask, render_template, redirect, url_for, request, jsonify
import server
import database as db
import logging


app = Flask(__name__)


# Part I: User sign-up and log-in
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
            u_id = request.form["username"]
            u_pw = request.form["psw"]
            signed_up = server.new_user(u_id, u_pw)
            if not signed_up:
                error_msg = server.error_messages[1]
            else:
                message = "You've signed up"
                app.logger.info("User created: {}".format(u_id))
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


# Part II: User choose character
@app.route("/ch_names/")
def ch_names():
    # temporarily hard coding
    return jsonify(ch_names=[["良小花", "女，当红小花，演技派。"],
                             ["良星星", "女，生日寿星。"],
                             # ["黄学", "男，学长。"],
                             # ["黑轮海", "女，同班同学。"],
                             # ["希嘻嘻", "女，lo裙小能手，学生会主席。"],
                             # ["嵩主角", "男，学校助教。"],
                             # ["大幂幂", "女，好姐妹。"],
                             # ["tc第二帅", "男，tc第二帅2。"],
                             # ["撒比尔", "男，小矮人。"],
                             ["米亚伦", "女，同班同学。"]])


@app.route("/is_chosen/")
def is_chosen():
    return jsonify(ch1=db.track['chars']['良小花'],  # Temp hard c
                   ch2=db.track['chars']['良星星'],
                   ch3=db.track['chars']['米亚伦'],
                   # ch4=True, ch5=True,
                   # ch6=True, ch7=True, ch8=True, ch9=True, ch10=True
                   )


@app.route("/<u_name>/choose_ch", methods=["GET", "POST"])
def choose_ch(u_name):
    if request.method == "POST":
        ch_name = request.form["choose_ch"]
        ch_added = server.new_ch(u_name, ch_name)
        if ch_added:
            app.logger.info("User {} has chosen {}".format(u_name, ch_name))
            return redirect(url_for("play", u_name=u_name, ch_name=ch_name))
        elif not ch_added:
            message = "此角色已被选择"
            return render_template("choose_ch.html", message=message)
        else:
            return redirect(url_for("play", u_name=u_name, ch_name=ch_added))
    else:
        ch_name = server.verify_ch(u_name)
        if type(ch_name) == str:
            return redirect(url_for("play", u_name=u_name, ch_name=ch_name))
        else:
            return render_template("choose_ch.html")


# Part III: Play page
@app.route("/<u_name>/play/<ch_name>", methods=["GET", "POST"])
def play(u_name, ch_name):
    if request.method == "GET":
        ch = db.user[u_name]["char"]
        if ch_name == ch:
            message = {"u_name": u_name, "ch_name": ch_name}
            return render_template("play.html", msg_info=message)
        else:
            if ch_name in db.game['chars']:
                return server.error_messages[5]
            else:
                return server.error_messages[6]
    else:
        vote_name = request.form["vote"]
        db.vote[vote_name].append(ch_name)  # 给db
        db.user[u_name]["round"]["voted"] = True  # 给db
        app.logger.info("User {} voted {}".format(u_name, vote_name))
        return redirect(url_for("ending"))


@app.route("/ap_num/", methods=["POST"])
def ap_num():
    name = request.form["name"]
    u_ap = db.user[name]["ap"]
    return jsonify(ap=u_ap)


@app.route("/clue_num/")
def clue_num():
    result = server.update_clue_num()
    return result


@app.route("/locations/")
def locations():
    return jsonify(l1="良小花", l2="良星星", l3="米亚伦", l4="公共区域", l5="现场")


@app.route("/start_round1/")
def start_round1():
    name1 = request.args.get("name_ready_for_1")
    u_id = str(name1).lower()
    check = server.start_rnd(1, u_id)
    if check:
        return jsonify(result="1")
    else:
        return jsonify(result="0")


@app.route("/start_round2/")
def start_round2():
    name1 = request.args.get("name_ready_for_2")
    u_id = str(name1).lower()
    check = server.start_rnd(2, u_id)
    if check:
        return jsonify(result="1")
    else:
        return jsonify(result="0")


@app.route("/find_clue/")
def find_clue():
    name = str(request.args.get("name_find_clue")).lower()
    place = str(request.args.get("name_place")).lower()
    [result, clue] = server.search_clue(name, place)
    if result:
        clue_release = clue.split('//')
        if len(clue_release) == 1:
            has_hidden = False
        else:
            has_hidden = True
        return jsonify(clue=clue_release[0], hidden=has_hidden)
    else:
        return


@app.route("/hidden_clue/")
def hidden_clue():
    name = str(request.args.get("name_find_clue")).lower()
    clue = str(request.args.get("clue_for_hidden")).lower()
    n_round = db.track["round"]
    hidden = server.search_hidden_clue(name, clue, n_round)
    if len(hidden) == 1:
        return jsonify(hidden_clue=hidden)
    else:
        return jsonify(hidden_clue=hidden[0])


@app.route("/update_revealed_clues/")
def update_revealed_clues():
    print(db.track["publicized_clue"])
    clues = {}
    for x in db.game["locations"]:
        clues[x] = server.update_released(x)
    print(clues)
    return jsonify(p01=clues["p01"],
                   p02=clues["p02"],
                   p03=clues["p03"],
                   p04=clues["p04"],
                   p05=clues["p05"])


@app.route("/release_clue/")
def release_clue():
    clue = str(request.args.get("clue_to_release")).lower()
    # place = str(request.args.get("name_place")).lower()
    place = 'p01'  # temp hard coding
    is_release = server.verify_release(clue, place)  # True: has been released
    print("In gui.py release_clue: released {}".format(clue))
    if is_release:
        return jsonify(status="failure")
    else:
        return jsonify(status="success")


# Part IV: Vote
@app.route("/ending/")
def ending():
    return render_template("ending.html")


@app.route("/vote_result/")
def vote_result():
    result = server.disp_votes()
    return result


@app.route("/final_result/")
def final_result():
    vote_complete = server.verify_vote()
    if vote_complete:
        voted_murderer = server.calc_vote()
        [result, true_murderer] = server.verify_murderer(voted_murderer)
        app.logger.info("Voting finished. Voted murderer: {}; Result: {}."
                        .format(voted_murderer, result))
        return jsonify(revealed=True,
                       vote_murder=voted_murderer,
                       true_murder=true_murderer,
                       result=result)
    else:
        return jsonify(revealed=False, vote_murder=None, true_murder=None,
                       result=None)


if __name__ == "__main__":
    logging.basicConfig(filename='MMG_server.log', level=logging.INFO,
                        filemode='w')
    app.run(debug=True)
