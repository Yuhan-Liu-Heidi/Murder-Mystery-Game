from flask import Flask, jsonify
import numpy as np
import database as db
import math


app = Flask(__name__)


error_messages = {0: "该用户已存在",
                  1: "该用户不存在",
                  2: "密码不正确",
                  3: "这不是您的角色，请不要作弊哦~",
                  4: "该角色不存在",
                  5: "本轮搜证未开始",
                  6: "error",
                  7: "no ap",
                  8: "no clue",
                  9: "该线索已被深入"}


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
        return error_messages[1]
    try:
        assert p == db.user[u_id]["pw"]
    except AssertionError:
        return error_messages[2]
    return True


# Part II: User choose character
def ch_page():
    """ load characters and descriptions from dictionary

    :return: list containing characters and their descriptions
    """
    ch_names = []
    for ch in db.game['descriptions'].keys():
        ch_names.append([ch, db.game['descriptions'][ch]])
    return ch_names


def ch_chosen():
    """ Return chosen status of characters in format {"ch1": True}

    :return: dict containing boolean representing chosen status
    """
    result = {}
    for i, is_chose in enumerate(db.track['chars'].values()):
        result["ch{}".format(i+1)] = is_chose
    return result


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
def locations():
    """ Return location names in format {"l1": "crime scene"}

    :return: dict containing names of the locations
    """
    location = {}
    for i, place in enumerate(db.game['location map'].values()):
        location["l{}".format(i+1)] = place
    return location


def start_rnd(n_rnd, u_id):
    """ Verify if all users are ready for a round of clue searching

    :param n_rnd: int containing round number
    :param u_id: string containing user ID
    :return: '1' if the round has started, '0' if not
    """
    def calc_rnd_ap():
        total_ap = 0
        for p in db.game["clues"][rnd]:
            for c in db.game["clues"][rnd][p]:
                total_ap += len(c.split("//")) + 1
        ap = math.ceil(total_ap / len(db.game["chars"]))
        return ap
    db.track_round(u_id, n_rnd)  # set user True for this round
    if db.track["round"] >= n_rnd:
        return '1'
    else:
        n_start = sum([db.user[x]["round"][n_rnd] for x in db.user])
        if n_start < db.game["player_num"]:
            return '0'
        else:
            db.track["round"] = n_rnd  # 给db：记录游戏轮数
            rnd = "round{}".format(n_rnd)
            for user in db.user:  # 给db：玩家AP增加
                db.user[user]["ap"] += calc_rnd_ap()
            for place in db.game["locations"]:
                for clue in db.game["clues"][rnd][place]:
                    db.track["clues"][place].append(clue)  # 给db：更新可搜线索池
            return '1'


def search_clue(u_id, place):
    """ Search clues

    When users search a place, verify (1) if this round of clue searching has
    began, (2) if they is allowed to search this place, (3) if they have enough
    AP, and (4) if there are clues left in this place.
    Return first a clue or an error message and then boolean representing if
    the clue has a hidden part.

    :param u_id: string containing user ID
    :param place: string containing place searched
    :return: string containing clue or error and boolean representing if the
    clue has hidden
    """
    u_ch = db.user[u_id]["char"]
    u_ap = db.user[u_id]["ap"]
    r_num = db.track["round"]
    place_name = db.game['location map'][place]
    has_hidden = False
    if r_num == 0:
        clue = error_messages[5]
    elif u_ch in place_name:
        clue = error_messages[6]
    elif u_ap <= 0:
        clue = error_messages[7]
    else:
        if len(db.track["clues"][place]) == 0:
            clue = error_messages[8]
        else:
            c = db.track["clues"][place][0]
            db.track["clues"][place].remove(c)  # 给db：去掉已搜证据
            if len(c.split("//")) > 1:
                has_hidden = True
                clue, _ = c.split('//')
                clue_save = c.replace(clue, clue+'->'+u_id)
                db.track['searched_clues'][place].append(clue_save)
                # 给db：记录证据归属
            else:
                db.track['searched_clues'][place].append(c+'->'+u_id)
                # 给db：记录证据归属
                clue = c
            db.user[u_id]['ap'] -= 2  # 给db：减ap
    return clue, has_hidden


def search_hidden_clue(u_id, clue):
    """ Search hidden clues

    :param u_id: string containing user ID
    :param clue: string containing the clue searched for hidden
    :return: string containing clue or error
    """
    u_ch = db.user[u_id]["char"]
    u_ap = db.user[u_id]["ap"]
    place = ""
    if u_ap <= 0:
        return False, error_messages[7]
    else:
        has_found = False
        for p in db.track['searched_clues'].keys():
            for c in db.track['searched_clues'][p]:
                if clue in c.split("//")[0].split('->')[0]:
                    place = p
                    has_found = True
                    c_full = c
                    break
            if has_found:
                break
        place_name = db.game['location map'][place]
        if u_ch in place_name:
            return error_messages[6]
        else:
            hidden = c_full.split('//')[1]
            if len(hidden.split('->')) == 1:
                c_save = c_full + '->' + u_id
                db.track['searched_clues'][place].remove(c_full)  # 给db
                db.track['searched_clues'][place].append(c_save)  # 给db
                db.user[u_id]["ap"] -= 1  # 给db
                return hidden
            else:
                return error_messages[9]


def verify_release(clue, place):
    """ Verify if a clue has been revealed

    :param clue: string containing the clue
    :param place: string containing the place of the clue
    :return: boolean representing if the clue has been revealed
    """
    def has_publicized(c):
        c_splt = c.split('->')
        if c_splt[1] == 'publicized':
            return "failure"
        else:
            return "success"
    for srchd_c in db.track['searched_clues'][place]:
        if clue in srchd_c:
            srchd_splt = srchd_c.split('//')
            has_hidden = bool(len(srchd_splt)-1)
            if has_hidden:
                if clue in srchd_splt[0]:
                    result = has_publicized(srchd_splt[0])
                    c_save = srchd_splt[0].split('->')[0] + '->publicized//'\
                        + srchd_splt[1]
                else:
                    result = has_publicized(srchd_splt[1])
                    c_save = srchd_splt[0].split('->')[0] + '->publicized//'\
                        + srchd_splt[1].split('->')[0] + '->publicized//'
            else:
                result = has_publicized(srchd_splt[0])
                c_save = srchd_c.split('->')[0] + '->publicized//'
            db.track['searched_clues'][place].remove(srchd_c)  # 给db：更新公开
            db.track['searched_clues'][place].append(c_save)
            return result


def user_voted(u_name):
    """ Verify if the user has voted

    :param u_name: string containing user ID
    :return: Boolean representing if the user has voted
    """
    return db.user[u_name]["round"]["voted"]


def update_clue_num():
    """ Update counts of clues searched/total in format {"p01": [#, #]}

    :return: dict containing clue num of each place
    """
    # found clue num | rnd1 clue num | rnd2 clue num
    result = {}
    rnd = db.track["round"]
    if rnd == 0:
        return
    else:
        index = 0
        for i, place in enumerate(db.game["locations"]):
            key = "p{}".format(str(i+1).zfill(2))
            if rnd == 1:
                num_c = len(db.game["clues"]["round1"][place])
            else:
                num_c = len(db.game["clues"]["round1"][place]) + \
                    len(db.game["clues"]["round2"][place])
            num_found_c = num_c - len(db.track["clues"][place])
            result[key] = [num_found_c, num_c]
            index += 1
        return result


def update_round(u_id):
    """ Update round of the game in format {"round1": [#, #]}

    :return: dict containing the round info
    """
    # check = [round1, round2], round*=[has_user_clk_rnd, has_rnd_bgn]
    is_rnd1 = db.track['round'] > 0
    is_rnd2 = db.track['round'] > 1
    u_rnd1 = db.user[u_id]['round'][1]
    u_rnd2 = db.user[u_id]['round'][2]
    check = {"round1": [u_rnd1, is_rnd1], "round2": [u_rnd2, is_rnd2]}
    return check


def update_released():
    """ Update all released clues

    Format: {"p01": []}
    clue w/o hidden: ["clue_0", []]
    clue w/ hidden: ["clue_0", ["clue_1"]] if hidden released
                    ["clue_0", [False, is_searched]] if hidden not released

    :return: dict containing all released clues
    """
    rlsd_c = {}
    n_rnd = db.track["round"]
    if n_rnd == 0:
        return rlsd_c
    for i, place in enumerate(db.track['searched_clues'].keys()):
        key = "p{}".format(str(i+1).zfill(2))
        rlsd_c[key] = []
        for clue in db.track['searched_clues'][place]:
            c = clue.split("//")
            if len(c) == 1 or c[1] == '':
                if c[0].split('->')[1] == 'publicized':
                    rlsd_c[key].append([c[0].split('->')[0], []])
            else:
                if c[0].split('->')[1] == 'publicized':
                    if len(c[1].split('->')) == 1:
                        c_pub = c[0].split('->')[0]
                        rlsd_c[key].append([c_pub, [False, False]])
                    else:
                        if c[1].split('->')[1] == 'publicized':
                            c_pub = [c[0].split('->')[0], c[1].split('->')[0]]
                            rlsd_c[key].append([c_pub[0], [c_pub[1]]])
                        else:
                            c_pub = c[0].split('->')[0]
                            rlsd_c[key].append([c_pub, [False, True]])
    return rlsd_c


def update_own(u_id):
    """ Update own clue for a user

    Format: {"p01": []}
    clue w/o hidden: [["clue_0", False], []]
    clue w/ hidden: [["clue_0", False], [False]] if hidden not searched
                    [["clue_0", False], ["clue_1", False]] if hidden searched

    :param u_id: string containing user ID
    :return: dict containing clues the user searched and not publicized
    """
    own_c = {}
    n_rnd = db.track["round"]
    if n_rnd == 0:
        return own_c
    for i, place in enumerate(db.track['searched_clues'].keys()):
        key = "p{}".format(str(i+1).zfill(2))
        own_c[key] = []
        for clue in db.track['searched_clues'][place]:
            owner = clue.split('->')[-1]
            if u_id in owner:
                c = clue.split('//')
                if len(c) == 1 or c[1] == '':
                    own_c[key].append([[c[0].split('->')[0], False], []])
                else:
                    if u_id in c[1]:
                        c_pub_0 = [c[0].split('->')[0], False]
                        c_pub_1 = [c[1].split('->')[0], False]
                        own_c[key].append([c_pub_0, c_pub_1])
                    else:
                        c_pub_0 = [c[0].split('->')[0], False]
                        own_c[key].append([c_pub_0, [False]])
    return own_c


# Part IV: Vote
def vote(u_name, ch_name, vote_name):
    """ Verify if the user is allowed to vote and record the voting result

    :param u_name: string containing user ID
    :param ch_name: string containing character
    :param vote_name: string containing voted character name
    :return: Boolean representing vote status
    """
    n_rnd = db.track["round"]
    if n_rnd < 2:
        return False
    db.vote[vote_name].append(ch_name)  # 给db：记录投票结果
    db.user[u_name]["round"]["voted"] = True  # 给db：记录已投用户
    return True


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
    """ Display voting results in format {"ch1": []}

    :return: dict containing characters voted and people who voted them
    """
    result = {}
    for i, ch in enumerate(db.vote.keys()):
        key = "ch{}".format(i+1)
        result[key] = [ch, db.vote[ch]]
    return result


def verify_murderer(voted):
    """ Verify if voted character is true murderer

    Check if the voted character is the true murderer, return result and the
    name of the true murderer. If there are more than one character got equal
    votes, does not reveal the true murderer and let users to decide once more.
    Format:{"revealed": bool, "true_murder": str, "vote_murder": str,
            "result": "Success" or "Failed"}

    :param voted: string containing voted character
    :return: dict containing vote result
    """
    true_murderer = db.game["murderer"]
    result = {"revealed": True,
              "true_murder": true_murderer,
              "vote_murder": voted}
    if len(voted) == 1:
        if voted[0] == true_murderer:
            result["result"] = "Success"
            return result
        else:
            result["result"] = "Failed"
            return result
    else:
        result["true_murder"] = "???"
        result["result"] = "平票"
        return result
