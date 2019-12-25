from flask import Flask
from testdata import user, game


app = Flask(__name__)


error_messages = {0: "该用户不存在",
                  1: "该用户已存在",
                  2: "密码不正确",
                  3: "本轮搜证未开始",
                  4: "您已选好角色"}


def new_user(i, p):
    from database import user
    if i not in user.keys():
        database.create_us
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


def assign_character(i, ch_name):
    from database import user, game
    try:
        u_id = [x for x in user.keys() if x == i][0]
    except IndexError:
        return error_messages[0]
    database.assign_ch()
    return True


def user_ready(u_id, n_round):
    user[u_id]["round"][n_round] = True
    return


def start_round(n_round):
    n_start = sum([user[x]["round"][n_round] for x in user])
    if n_start < game["player_num"]:
        return False
    else:
        return True


def search_clue(n_round):
    if start_round(n_round):
        pass
    else:
        return error_messages[3]


# @app.route("")
if __name__ == "__main__":
    # app.run()
    pass
