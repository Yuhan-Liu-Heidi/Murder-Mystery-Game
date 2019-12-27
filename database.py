# assume ap is the same for round1 and round2

global user, game
user = {}


def create_user(user_id, pw):
    global user, game
    user[user_id] = {'pw': pw,
                     'char': {'name': None, 'story': None},
                     'ap': game['round_ap'],
                     'clue': {},
                     'round': {1: False, 2: False}
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
    from create_game import track
    global user
    user[user_id]['char'] = char
    track['chars'][char] = True
    print('User {} has chosen character {}'.format(user_id, char))
    return


def clue_update(user_id, place):
    global user
    # check if user picked their own place
    if user[user_id]['char'] in place:
        return False
    else:  # update user ap, clue
        add_clue()
        sbtr_ap()
    print()
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
                             ['1/1 clue at p2 ele2']]
                      },
            'stories': {'A': 'A story (image path)',
                        'B': 'B story',
                        'C': 'C story'},
            'player_num': 3  # input
            }
    return
