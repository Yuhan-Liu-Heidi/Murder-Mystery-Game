from flask import Flask, jsonify
import numpy as np
import database as db


app = Flask(__name__)


error_messages = {0: "该用户不存在",
                  1: "该用户已存在",
                  2: "密码不正确",
                  3: "本轮搜证未开始",
                  5: "这不是您的角色，请不要作弊哦~",
                  6: "该角色不存在",
                  7: "您不可以搜索自己的线索",
                  8: "您的AP不足",
                  9: "该地点已无剩余线索",
                  10: "该线索已被深入"}


# Part I: User sign-up and log-in
def new_user(i, p):
    """ Create new user with ID and password

    :param i: string containing user ID
    :param p: string containing password
    :return: boolean result of creating user
    """
    if i not in db.user.keys():
        db.create_user(i, p)
        return True
    else:
        return False


def verify_user(i, p):
    """ User log-in with ID and password

    :param i: string containing user ID
    :param p: string containing password
    :return: True when logged-in, string when not logged in
    """
    try:
        u_id = [x for x in db.user.keys() if x == i][0]
    except IndexError:
        return error_messages[0]
    try:
        assert p == db.user[u_id]["pw"]
    except AssertionError:
        return error_messages[2]
    return True


# Part II: User choose character
def new_ch(i, ch_name):
    """ User choose character

    If the character has been chosen, return False; if the user has chose
    another character before, return character name; otherwise, link the chosen
    character to the user and return True

    :param i: string containing user ID
    :param ch_name: string containing chosen character
    :return:
    """
    if db.track['chars'][ch_name]:
        return False
    elif db.user[i]["char"] is not None:
        return db.user[i]["char"]
    else:
        db.add_char(i, ch_name)
        return True


def verify_ch(i):
    """ Verify if user has chosen character

    :param i: string containing user ID
    :return: string containing character or False if user has not chosen
    """
    u_id = [x for x in db.user.keys() if x == i][0]
    if db.user[u_id]["char"] is not None:
        return db.user[u_id]["char"]
    else:
        return False


# Part III: Play page
def start_rnd(n_rnd, u_id):
    """ Verify if all users are ready for a round of clue searching

    :param n_rnd: int containing round number
    :param u_id: string containing user ID
    :return: boolean of the result, True for all ready
    """
    db.track_round(u_id, n_rnd)  # set user True for this round
    if db.track["round"] >= n_rnd:
        return True
    else:
        n_start = sum([db.user[x]["round"][n_rnd] for x in db.user])
        if n_start < db.game["player_num"]:
            return False
        else:
            db.track["round"] = n_rnd  # 给db
            rnd = "round{}".format(n_rnd)
            for user in db.user:  # 加ap 给db
                db.user[user]["ap"] += db.game['round_ap'] * 2
            for place in db.game["locations"]:
                for clue in db.game["clues"][rnd][place]:
                    db.track["clues"][place].append(clue)  # 给db
                print(db.track["clues"])
            return True


def search_clue(u_id, place):
    """ Search clues

    When users search a place, verify (1) if this round of clue searching has
    began, (2) if they is allowed to search this place, (3) if they have enough
    AP, and (4) if there are clues left in this place.
    Return first a boolean representing if the search is successful and then a
    clue or an error message.

    :param u_id: string containing user ID
    :param place: string containing place searched
    :return: boolean containing result and string containing clue or error
    """
    u_ch = db.user[u_id]["char"]
    u_ap = db.user[u_id]["ap"]
    if u_ch in place:
        return False, error_messages[7]
    elif u_ap <= 0:
        return False, error_messages[8]
    else:
        r_num = db.track["round"]
        if r_num == 0:
            return False, error_messages[3]
        else:
            if len(db.track["clues"][place]) is not 0:
                clue = db.track["clues"][place][0]
                db.track["clues"][place].remove(clue)  # 给db
                if len(clue.split("//")) > 1:
                    db.track["hidden"].append(clue.split("//")[1])  # 给db
                db.user[u_id]["ap"] -= 2  # 给db
                return True, clue
            else:
                return False, error_messages[9]


def update_clue_num():
    """ Update counts of clues searched/total

    :return: json containing the clue nums
    """
    # found clue num | rnd1 clue num | rnd2 clue num
    if db.track["round"] == 0:
        return
    else:
        num_clue = np.zeros([len(db.game["locations"]), 3])
        index = 0
        rnd = db.track["round"]
        for place in db.game["locations"]:
            num_clue[index][1] = len(db.game["clues"]["round1"][place])
            num_clue[index][2] = num_clue[index][1] + \
                                 len(db.game["clues"]["round2"][place])
            num_clue[index][0] = num_clue[index][rnd] - \
                                 len(db.track["clues"][place])
            index += 1
        return jsonify(p01=[num_clue[0][0], num_clue[0][rnd]],
                       p02=[num_clue[1][0], num_clue[1][rnd]],
                       p03=[num_clue[2][0], num_clue[2][rnd]],
                       p04=[num_clue[3][0], num_clue[3][rnd]],
                       p05=[num_clue[4][0], num_clue[4][rnd]])


def verify_release(clue, place):  # BUG: cant get place
    """ Verify if a clue has been revealed

    :param clue: string containing the clue
    :param place: string containing the place of the clue
    :return: boolean representing if the clue has been revealed
    """
    if clue in str(db.track["publicized_clue"][place]):
        return True
    else:
        db.track["publicized_clue"][place].append([clue])  # 给db
        return False


def search_hidden_clue(u_id, clue, n_rnd):
    """

    :param u_id:
    :param clue:
    :param n_rnd:
    :return:
    """
    u_ch = db.user[u_id]["char"]
    u_ap = db.user[u_id]["ap"]
    place = ""
    hidden = ""
    if u_ap <= 0:
        return False, error_messages[8]
    else:
        rnd = "round{}".format(n_rnd)
        for p in db.game["clues"][rnd].keys():
            for c in db.game["clues"][rnd][p]:
                print("Want to search hidden for {}".format(clue))
                print("Comparing w/ {}".format(c.split("//")[0]))
                if clue in c.split("//")[0]:
                    hidden = c.split("//")[1]
                    place = p
                    break
        if hidden == "" or place == "":
            return False
        if u_ch in place:
            return False, error_messages[7]
        else:
            if hidden in db.track["hidden"]:
                db.track["hidden"].remove(hidden)  # 给db
                db.user[u_id]["ap"] -= 2  # 给db
                return hidden
            else:
                return False, error_messages[10]


def verify_hidden_for_release():
    pass


# Part IV: Vote
def verify_vote():
    """ Verify if all users has voted

    :return: boolean containing the result
    """
    n_voted = sum([db.user[x]["round"]["voted"] for x in db.user])
    if n_voted < db.game["player_num"]:
        return False
    else:
        return True


def calc_vote():
    """ Count votes and return a list of most voted characters

    :return: list containing characters
    """
    v_max = 0
    for x in db.vote.keys():
        if len(db.vote[x]) > v_max:
            v_max = len(db.vote[x])
    return [x for x in db.vote.keys() if len(db.vote[x]) == v_max]


def disp_votes():
    """ Display voting results

    :return: json containing characters voted and people who voted them
    """
    ch_list = [x for x in db.vote.keys()]
    return jsonify(ch1=[ch_list[0], db.vote[ch_list[0]]],
                   ch2=[ch_list[1], db.vote[ch_list[1]]],
                   ch3=[ch_list[2], db.vote[ch_list[2]]],
                   ch4=["弃权", db.vote[ch_list[3]]])


def verify_murderer(voted):
    """ Verify if voted character is true murderer

    Check if the voted character is the true murderer, return result and the
    name of the true murderer. If there are more than one character got equal
    votes, does not reveal the true murderer and let users to decide once more.

    :param voted: string containing voted character
    :return: list containing result and true murderer
    """
    true_murderer = db.game["murderer"]
    if len(voted) == 1:
        if voted == true_murderer:
            return ["Success", true_murderer]
        else:
            return ["Failed", true_murderer]
    else:
        return ["平票", "???"]
