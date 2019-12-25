import json

user = {'01': {'pw': '111',
               'char': {'name': None, 'story': None},
               'ap': 4,
               'clue': {'p1': [['this is 1/2 clue at p1 ele1',
                                'this is 2/2 clue at p1 ele1'],
                               ['this is 1/1 clue at p1 ele2']],
                        'p2': [['this is 1/1 clue at p2 ele1'],
                               ['this is 1/1 clue at p2 ele2']]},
               'round': {'1': False, '2': False}
               },
        '02': {'pw': '222',
               'char': {'name': None, 'story': None},
               'ap': 4,
               'clue': {'p1': [['this is 1/2 clue at p1 ele1',
                                'this is 2/2 clue at p1 ele1'],
                               ['this is 1/1 clue at p1 ele2']],
                        'p2': [['this is 1/1 clue at p2 ele1'],
                               ['this is 1/1 clue at p2 ele2']]},
               'round': {'1': False, '2': False}
               },
        '03': {'pw': '333',
               'char': {'name': None, 'story': None},
               'ap': 4,
               'clue': {'p1': [['this is 1/2 clue at p1 ele1',
                                'this is 2/2 clue at p1 ele1'],
                               ['this is 1/1 clue at p1 ele2']],
                        'p2': [['this is 1/1 clue at p2 ele1'],
                               ['this is 1/1 clue at p2 ele2']]},
               'round': {'1': False, '2': False}
               }
        }

track = {'chars': {'A': False, 'B': False, 'C': False},
         'publicized_clue': {'p1': [['this is 1/2 clue at p1 ele1'],
                                    ['this is 1/1 clue at p1 ele2']],
                             'p2': [['this is 1/1 clue at p2 ele1']]},
         }

game = {'chars': ['A', 'B', 'C'],
        'clues': {'round1': {'p1': [['clue1 at p1 w/ hidden',
                                     'hidden of clue1 at p1'],
                             # w/ hidden, list with 2 elements
                                    ['clue2 at p1 w/o hidden']],
                             # w/o hidden, list with 1 element
                             'p2': [['clue1 at p2 w/o hidden'],
                                    ['clue2 at p2 w/o hidden']]
                             },
                  'round2': {'p1': [['clue1 at p1 w/ hidden',
                                     'hidden of clue1 at p1'],
                                    ['clue2 at p1 w/o hidden']],
                             'p2': [['clue1 at p2 w/o hidden'],
                                    ['clue2 at p2 w/o hidden']]
                             }
                  },
        'stories': {'A': 'A story',
                    'B': 'B story',
                    'C': 'C story'},
        'round_ap': 4,
        'player_num': 3
        }

out_file = open("sample_game.json", "w")
json.dump(game, out_file)
out_file.close()
