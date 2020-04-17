# assuming ap is the same for round1 and round2
"""
Clue storing:
 - All clues come in the format of 'clue' or 'clue//clue_hidden'
 - After a user searched a clue, save 'clue/userID' or
   'clue/userID//clue_hidden' to track['searched_clues']
 - After a user publicized a clue, change 'clue/userID' part
   to 'clue/publicized'
 - In game json, if a clue does not have hidden, don't put 'clue//'
"""


import json
global user, game
# Please initiate the following dict at the beginning
user = {}
vote = {"良小花": [], "良星星": [], "米亚伦": [], None: []}
track = {'chars': {'良小花': False, '良星星': False, '米亚伦': False},
         'searched_clues': {'p01': [], 'p02': [], 'p03': [], 'p04': [],
                            'p05': []},
         'clues': {'p01': [], 'p02': [], 'p03': [], 'p04': [], 'p05': []},
         'round': 0}


def rd_game():
    global game
    file_path = "sample_game.json"
    in_file = open(file_path, "r")
    game = json.load(in_file)
    in_file.close()
    return game


game = rd_game()
game["murderer"] = "良小花"
game["location map"] = {"p01": '良小花', "p02": '良星星', "p03": '米亚伦',
                        "p04": '公共区域', "p05": '现场'}
game["descriptions"] = {"良小花": "女，当红小花，演技派。",
                        "良星星": "女，生日寿星。",
                        "米亚伦": "女，同班同学。"}


def create_user(user_id, pw):
    global user, game
    user[user_id] = {'pw': pw,
                     'char': None,
                     'ap': 0,
                     'clue': {},
                     'round': {1: False, 2: False, "voted": False}
                     }
    print('User account created for {}.'.format(user_id))
    return user


# def user_exist(user_id):
#     global user
#     if user_id in user:
#         return True
#     else:
#         return False


def add_char(user_id, char):
    global user
    user[user_id]['char'] = char
    track['chars'][char] = True
    print('User {} has chosen character {}'.format(user_id, char))
    return user, track


def clue_update(user_id, place):
    global user
    # check if user picked their own place
    if user[user_id]['char'] in place:
        return False
    else:  # update user ap, clue
        add_clue()
        sbtr_ap()
    return


def add_clue():
    global user
    pass


def sbtr_ap():
    global user
    pass


def publicize(place, clue):
    from create_game import track
    pass


def add_ap():
    global user, game
    for x in user:
        if x['round'][1] and x['round'][2]:
            x['ap'] = x['ap'] + game['round_ap']
    return


def track_round(user_id, rd):
    global user
    if user[user_id]['round'][rd]:
        return 'User has already clicked {}轮搜证'.format(rd)
    else:
        user[user_id]['round'][rd] = True
    print('User {} has clicked {}轮搜证.'.format(user_id, rd))
    return


# make separate python file
def create_game():
    global game
    game = {'chars': {'A': True, 'B': True, 'C': True},  # input
            'clues': {'p1': [['clue1 at p1 w/ hidden',  # input
                              'hidden of clue1 at p1'],
                             ['clue2 at p1 w/o hidden']],
                      'p2': [['1/1 clue at p2 ele1'],
                             ['1/1 clue at p2 ele2']]},
            'stories': {'A': 'A story (image path)',
                        'B': 'B story',
                        'C': 'C story'},
            'player_num': 3,
            'murderer': '良小花'}
    return


if __name__ == "__main__":
    rd_game()
    # create_game()
