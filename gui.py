from flask import Flask, render_template, redirect, url_for, request, jsonify
import server
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
            signed_up = server.new_user(request.form["username"],
                                        request.form["psw"])
            if not signed_up:
                error_msg = server.error_messages[1]
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
        if type(ch_name) == str:
            return redirect(url_for("play", u_name=u_name, ch_name=ch_name))
        else:
            return render_template("choose_ch.html")


# Part III: Play page
@app.route("/<u_name>/play/<ch_name>", methods=["GET", "POST"])
def play(u_name, ch_name):
    from database import user, game, vote
    if request.method == "GET":
        ch = user[u_name]["char"]
        if ch_name == ch:
            message = {"u_name": u_name, "ch_name": ch_name}
            return render_template("play.html", msg_info=message)
        else:
            if ch_name in game['chars']:
                return server.error_messages[5]
            else:
                return server.error_messages[6]
    else:
        try:
            vote_name = request.form["vote"]
        except Exception:
            vote_name = None
        vote[vote_name].append(ch_name)
        user[u_name]["round"]["voted"] = True
        return redirect(url_for("ending"))


@app.route("/ap_num/", methods=["POST"])
def ap_num():
    from database import user
    name = request.form["name"]  # ?
    u_ap = user[name]["ap"]
    return jsonify(ap=u_ap)


@app.route("/clue_num/")
def clue_num():
    result = server.update_clue_num()
    return result


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
    print("in function find_clue: {}, {}".format(result, clue))
    if result:
        if len(clue) == 1:
            return jsonify(clue=clue, hidden=False)
        else:
            return jsonify(clue=clue, hidden=True)
    else:
        return


@app.route("/hidden_clue/")
def hidden_clue():
    name = str(request.args.get("name_find_clue")).lower()
    clue = str(request.args.get("clue_for_hidden")).lower()
    # somehow get the hidden clue as "深入线索1"
    # is_hidden=True -> This hidden clue is still hidden
    # is_hidden=False -> This hidden clue has been token
    is_hidden = True
    if is_hidden:
        return jsonify(hidden_clue="深入线索1")
    else:
        return jsonify(hidden_clue=False)


@app.route("/update_revealed_clues/")
def update_revealed_clues():
    return jsonify(p01=[["证据1", "深入证据1"], ["证据2"]],
                   p02=[["证据3", False], ["证据4", False]], p03=[])


@app.route("/release_clue/")
def release_clue():
    clue = str(request.args.get("clue_to_release")).lower()
    # is_release=True -> This clue has been released
    # is_release=False -> This clue has not been released
    is_release = True
    if is_release is False:
        return jsonify(status="success")
    else:
        return jsonify(status="failure")


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
        return jsonify(revealed=True,
                       vote_murder=voted_murderer,
                       true_murder=true_murderer,
                       result=result)
    else:
        return jsonify(revealed=False, vote_murder=None, true_murder=None,
                       result=None)


if __name__ == "__main__":
    app.run(debug=True)
