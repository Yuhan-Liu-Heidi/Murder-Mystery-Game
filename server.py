from flask import Flask, jsonify, request
import requests


app = Flask(__name__)
user_dict = {"Heidi": {"ID": "Heidi", "p": "0326"}}
story_dict = {"stories": [], "clues": []}
error_messages = {1: "用户名不正确",
                  2: "密码不正确"}


# @app.route()
def verify_user(ID, p):
    try:
        u_id = [x for x in user_dict.keys() if x == ID][0]
    except IndexError:
        return error_messages[1]
    try:
        assert p == user_dict[u_id]["p"]
    except AssertionError:
        return error_messages[2]
    return  # jump to page:


# @app.route("/new_game", methods=["POST"])
def new_game():
    pass


# @app.route("")
if __name__ == "__main__":
    # app.run()
    pass
