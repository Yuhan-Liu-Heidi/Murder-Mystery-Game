from flask import Flask, jsonify


app = Flask(__name__)


error_messages = {0: "该用户不存在",
                  1: "该用户已存在",
                  2: "密码不正确",
                  3: "本轮搜证未开始",
                  5: "这不是您的角色，请不要作弊哦~",
                  6: "该角色不存在",
                  7: "您不可以搜索自己的线索",
                  8: "您的AP不足",
                  9: "该地点已无剩余线索"}


# Part I: User sign-up and log-in
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


# Part II: User choose character
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


# Part III: Play page
def user_ready(u_id, n_rnd):
    from database import user
    user[u_id]["round"][n_rnd] = True
    return


def start_rnd(n_rnd, u_id):
    from database import user, game, track_round, track
    track_round(u_id, n_rnd)
    n_start = sum([user[x]["round"][n_rnd] for x in user])
    if n_start < game["player_num"]:
        return False
    else:
        track["round"] = n_rnd
        return True


def search_clue(u_id, place):
    from database import user, game, track
    u_ch = user[u_id]["char"]
    u_ap = user[u_id]["ap"]
    if u_ch in place:
        return False, error_messages[7]
    elif u_ap <= 0:
        return False, error_messages[8]
    else:
        r_num = track["round"]
        if r_num == 0:
            return False, error_messages[3]
        elif r_num == 1:
            check = True  # Temp hard coding
            if check:
                clue = game["clues"]["round1"]["p01"][0]  # Temp hard coding
                user[u_id]["ap"] -= 2
                return True, clue
            else:
                return False, error_messages[9]
        else:
            check = True
            if check:
                clue = game["clues"]["round2"]["p01"][0]  # Temp hard coding
                return True, clue
            else:
                return False, error_messages[9]


def update_clue_num():
    from database import game, track
    n_rnd = track["round"]
    if n_rnd == 1:
        n_c_p1 = len(game["clues"]["round1"]["p01"])
        n_c_revealed_p1 = len(track["publicized_clue"]["p1"])  # Temp hard c
        n_c_p2 = len(game["clues"]["round1"]["p02"])
        n_c_revealed_p2 = len(track["publicized_clue"]["p2"])  # Temp hard c
        n_c_p3 = len(game["clues"]["round1"]["p03"])
        n_c_revealed_p3 = len(track["publicized_clue"]["p3"])  # Temp hard c
    elif n_rnd == 2:
        n_c_p1 = len(game["clues"]["round2"]["p01"])
        n_c_revealed_p1 = len(track["publicized_clue"]["p1"])  # Temp hard c
        n_c_p2 = len(game["clues"]["round2"]["p02"])
        n_c_revealed_p2 = len(track["publicized_clue"]["p2"])  # Temp hard c
        n_c_p3 = len(game["clues"]["round2"]["p03"])
        n_c_revealed_p3 = len(track["publicized_clue"]["p3"])  # Temp hard c
    else:
        return jsonify(p01=[0, 0], p02=[0, 0], p03=[0, 0])
    return jsonify(p01=[n_c_revealed_p1, n_c_p1],
                   p02=[n_c_revealed_p2, n_c_p2],
                   p03=[n_c_revealed_p3, n_c_p3])


# Part IV: Vote
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
    true_murderer = game["murderer"]
    if len(voted) == 1:
        if voted == true_murderer:
            return ["Success", true_murderer]
        else:
            return ["Failed", true_murderer]
    else:
        return ["平票", "???"]


if __name__ == "__main__":
    pass
