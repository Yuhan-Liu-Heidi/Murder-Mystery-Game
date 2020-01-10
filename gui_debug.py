from flask import Flask, render_template, redirect, url_for, request, jsonify
import logging

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
            if request.form["username"] != "lily" \
                    or request.form["psw"] != "123":
                error = "Invalid login please try again"
            else:
                return redirect(url_for("choose_ch",
                                        u_name=request.form["username"]))
    return render_template("login.html", error=error)


@app.route("/<u_name>/choose_ch", methods=["GET", "POST"])
def choose_ch(u_name):
    if request.method == "POST":
        # check if user has chosen one ch or if it matches to the chosen one
        ch_name = request.form["choose_ch"]
        # is_chosen=False -> This ch has not been chosen
        # is_chosen=True -> This ch has been chosen
        is_chosen = False
        if is_chosen is False:
            return redirect(url_for("play", u_name=u_name, ch_name=ch_name))
        else:
            message = "此角色已被选择"
            return render_template("choose_ch.html", message=message)
    else:
        return render_template("choose_ch.html")


@app.route("/<u_name>/play/<ch_name>/", methods=["GET", "POST"])
def play(u_name, ch_name):
    if request.method == "GET":
        message = {"u_name": u_name, "ch_name": ch_name}
        return render_template("play.html", msg_info=message)
    elif request.method == "POST":
        # is_voted=False -> u_name has not voted.
        # is_voted=True -> u_name has voted.
        is_voted = False
        if is_voted is False:
            vote_name = request.form["vote"]
            # u_name+vote_name->save to database, go to the ending page
            logging.info("* {} has been voted."
                         .format(vote_name))
            return redirect(url_for("ending"))
        else:
            # do nothing just go to the ending page
            return redirect(url_for("ending"))
    else:
        return render_template("play.html")


@app.route("/start_round1/")
def start_round1():
    name1 = request.args.get("name_ready_for_1")
    # Receive the names that are ready.
    # OK! Everyone is ready for round 1?
    check = "lily"
    if str(name1).lower() == check:
        return jsonify(result="1")
    else:
        return jsonify(result="0")


@app.route("/start_round2/")
def start_round2():
    name1 = request.args.get("name_ready_for_2")
    # Receive the names that are ready.
    # OK! Everyone is ready for round 1?
    check = "lily"
    if str(name1).lower() == check:
        return jsonify(result="1")
    else:
        return jsonify(result="0")


@app.route("/clue_num/")
def clue_num():
    # return: place=[已搜, 所有】
    return jsonify(p01=[3, 3], p02=[1, 4], p03=[0, 3])


@app.route("/ap_num/", methods=["POST"])
def ap_num():
    return jsonify(ap=10)


@app.route("/find_clue/")
def find_clue():
    name = str(request.args.get("name_find_clue")).lower()
    place = str(request.args.get("name_place")).lower()
    # somehow get the clue in someplace for someone
    # update numbers in place
    return jsonify(clue="线索1", hidden=True)


@app.route("/hidden_clue/")
def hidden_clue():
    name = str(request.args.get("name_find_clue")).lower()
    clue = str(request.args.get("clue_for_hidden")).lower()
    # somehow get the hidden clue as "深入线索1"
    # is_hidden=True -> This hidden clue is still hidden
    # is_hidden=False -> This hidden clue has been token
    is_hidden = True
    if is_hidden is True:
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


@app.route("/ch_names/")
def ch_names():
    return jsonify(ch_names=[["良小花", "女，当红小花，演技派。"],
                             ["良星星", "女，生日寿星。"],
                             ["米亚伦", "女，同班同学。"],
                             ["黑轮海", "女，同班同学。"],
                             ["希嘻嘻", "女，lo裙小能手，学生会主席。"],
                             ["嵩主角", "男，学校助教。"],
                             ["大幂幂", "女，好姐妹。"],
                             ["tc第二帅", "男，tc第二帅2。"],
                             ["撒比尔", "男，小矮人。"],
                             ["黄学", "男，学长。"]])


@app.route("/is_chosen/")
def is_chosen():
    # ch1=False -> This ch1 has not been chosen
    # ch1=True -> This ch1 has been chosen
    return jsonify(ch1=False, ch2=False, ch3=True, ch4=True, ch5=True,
                   ch6=True, ch7=True, ch8=True, ch9=True, ch10=True)


@app.route("/ending/")
def ending():
    return render_template("ending.html")


@app.route("/vote_result/")
def vote_result():
    # ch1=["333", ["666"]]
    # => ch1 name is "333" and he now has 1 vote from "666".
    return jsonify(ch1=["111", []],
                   ch2=["222", ["111", "444", "555", "999", "000"]],
                   ch3=["333", ["666"]], ch4=["444", ["222"]], ch5=["555", []],
                   ch6=["666", ["333"]], ch7=["777", ["888"]],
                   ch8=["888", ["777"]], ch9=["999", []], ch10=["000", []])


@app.route("/final_result/")
def final_result():
    # if the vote has not finished,
    # return jsonify(revealed=False, vote_murder=None,
    #                true_murder=None, result=None)
    # if everyone voted, then revealed=True and get the variables below.
    vote_murder = "222"
    true_murder = "111"
    result = "Success"
    return jsonify(revealed=True, vote_murder=vote_murder,
                   true_murder=true_murder, result=result)


@app.route("/locations/")
def locations():
    return jsonify(l1="良小花", l2="良星星", l3="米亚伦11111111111111111111", l4="公共区域", l5="现场")


def init_server():
    logging.basicConfig(filename='image_server.log',
                        level=logging.INFO,
                        filemode='w')
    return None


if __name__ == "__main__":
    init_server()
    app.run(debug=True)
