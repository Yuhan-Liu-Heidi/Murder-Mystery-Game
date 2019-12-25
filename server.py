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


def verify_ch(i):
    from database import user
    u_id = [x for x in user.keys() if x == i][0]
    if user[u_id]["char"]["name"] is not None:
        return user[u_id]["char"]["name"]
    else:
        return False


def user_ready(u_id, n_rnd):
    user[u_id]["round"][n_rnd] = True
    return


def start_rnd(n_rnd):
    from database import user
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


# @app.route("")
if __name__ == "__main__":
    # app.run()
    pass
