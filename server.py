from flask import Flask, jsonify
from testdata import user, game


app = Flask(__name__)


error_messages = {0: "该用户不存在",
                  1: "该用户已存在",
                  2: "密码不正确",
                  3: "本轮搜证未开始",
                  5: "这不是您的角色，请不要作弊哦~",
                  6: "该角色不存在"}


def new_user(i, p):
    from database import user
    import database
    if i not in user.keys():
        database.create_user(i, p)
        return True
    else:
        return False


# @app.route()
def verify_user(i, p):
    from database import user
    try:
        u_id = [x for x in user.keys() if x == i][0]
    except IndexError:
        return error_messages[0]
    try:
        assert p == user[u_id]["pw"]
    except AssertionError:
        return error_messages[2]
    return True


def new_ch(i, ch_name):
    from database import user, add_char, track
    if track['chars'][ch_name]:
        return False
    elif user[i]["char"] is not None:
        return user[i]["char"]
    else:
        add_char(i, ch_name)
        return True


def verify_ch(i):
    from database import user
    u_id = [x for x in user.keys() if x == i][0]
    if user[u_id]["char"] is not None:
        return user[u_id]["char"]
    else:
        return False


def user_ready(u_id, n_rnd):
    user[u_id]["round"][n_rnd] = True
    return


def start_rnd(n_rnd, u_id):
    from database import user, game, track_round
    track_round(u_id, n_rnd)
    n_start = sum([user[x]["round"][n_rnd] for x in user])
    if n_start < game["player_num"]:
        return False
    else:
        return True


def search_clue(u_id, n_rnd, place):
    from database import user, game
    if start_rnd(n_rnd):
        pass
    else:
        return error_messages[3]


def verify_vote(n_rnd):
    from database import game, track
    n_voted = sum([user[x]["round"][n_rnd] for x in user])
    if n_voted < game["player_num"]:
        return False
    else:
        return True


def calc_vote():
    return jsonify(ch1=["111", []],
                   ch2=["222", ["111", "444", "555", "999", "000"]],
                   ch3=["333", ["666"]], ch4=["444", ["222"]], ch5=["555", []],
                   ch6=["666", ["333"]], ch7=["777", ["888"]],
                   ch8=["888", ["777"]], ch9=["999", []], ch10=["000", []])


def verify_murderer(voted):
    from database import game
    true_murderer = game["murderer"]
    if voted == true_murderer:
        return [True, true_murderer]
    else:
        return [False, true_murderer]


# @app.route("")
if __name__ == "__main__":
    # app.run()
    pass
