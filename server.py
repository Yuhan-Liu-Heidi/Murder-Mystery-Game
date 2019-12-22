from flask import Flask


app = Flask(__name__)
global user_dict, story_dict
user_dict = {}
story_dict = {"chars": {"黑底": True, "米亚": True},
              "stories": {"黑底": 121, "米亚": 111},
              "clues": {"黑底": 121, "米亚": 111}}
error_messages = {0: "用户名不正确",
                  1: "密码不正确",
                  2: "该用户已存在",
                  3: "该用户不存在"}


def new_user(i, p):
    global user_dict
    if i not in user_dict.keys():
        user_dict[i] = {"pw": p, "char": None, "ap": 16, "clue": None}
        return  # jump to page:
    else:
        return error_messages[2]


# @app.route()
def verify_user(i, p):
    global user_dict
    try:
        u_id = [x for x in user_dict.keys() if x == i][0]
    except IndexError:
        return error_messages[0]
    try:
        assert p == user_dict[u_id]["pw"]
    except AssertionError:
        return error_messages[1]
    return  # jump to page:


# @app.route("/new_game", methods=["POST"])
def new_game():
    pass


def assign_character(i, ch):
    global user_dict
    try:
        u_id = [x for x in user_dict.keys() if x == i][0]
    except IndexError:
        return error_messages[3]
    user_dict[u_id]["CH"] = ch
    return  # jump to page:


# @app.route("")
if __name__ == "__main__":
    # app.run()
    # new_user("Heidi", "0326")
    # print(user_dict)
    # assign_character("Heidi", "黑底")
    # print(user_dict)
    pass
