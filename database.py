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
vote = {"李永基": [], "宋晁徽": [], "孟余生": [], "麦权承": [], None: []}
track = {'chars': {'李永基': False, '宋晁徽': False, '孟余生': False, '麦权承': False},
         'searched_clues': {'p01': [], 'p02': [], 'p03': [], 'p04': [],
                            'p05': []},
         'clues': {'p01': [], 'p02': [], 'p03': [], 'p04': [], 'p05': []},
         'round': 0}


def rd_game():
    global game
    with open('sample_game.json', encoding='utf-8') as fr:
        result = json.load(fr)
    return result


game = rd_game()
game["murderer"] = "宋晁徽"
game["location map"] = {"p01": '李永基', "p02": '宋晁徽', "p03": '孟余生',
                        "p04": '麦权承', "p05": '押解车'}
game["descriptions"] = {"李永基": "男，30岁，南瞻部岛警视厅前厅长",
                        "宋晁徽": "男，52岁，现检察院检察长",
                        "孟余生": "男，47岁，秋门集团旗下南湾赌场老板",
                        "麦权承": "男，22岁，捡子的好朋友。"}


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
