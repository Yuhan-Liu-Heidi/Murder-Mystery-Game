from flask import Flask, jsonify


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
    from database import user
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


def verify_vote():
    from database import game, user
    n_voted = sum([user[x]["round"]["voted"] for x in user])
    if n_voted < game["player_num"]:
        return False
    else:
        return True


def calc_vote():
    from database import vote
    v_max = 0
    for x in vote.keys():
        if len(vote[x]) > v_max:
            v_max = len(vote[x])
    return [x for x in vote.keys() if len(vote[x]) == v_max]


def disp_votes():
    from database import vote
    ch_list = [x for x in vote.keys()]
    return jsonify(ch1=[ch_list[0], vote[ch_list[0]]],
                   ch2=[ch_list[1], vote[ch_list[1]]],
                   ch3=[ch_list[2], vote[ch_list[2]]],
                   ch4=["弃权", vote[ch_list[3]]])


def verify_murderer(voted):
    from database import game
    # true_murderer = '良小花'
    true_murderer = game["murderer"]
    if len(voted) == 1:
        if voted == true_murderer:
            return ["Success", true_murderer]
        else:
            return ["Failed", true_murderer]
    else:
        return ["平票", "???"]


# @app.route("")
if __name__ == "__main__":
    # app.run()
    pass
