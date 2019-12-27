# test database
import pytest


@pytest.mark.parametrize("user_id, pw, expected", [
    ('heidi',
     '1234',
     {'heidi': {'pw': '1234',
                'char': None,
                'ap': 4,
                'clue': {},
                'round': {1: False, 2: False}
                }}),
    ('lucy',
     '2345',
     {'heidi': {'pw': '1234',
                'char': None,
                'ap': 4,
                'clue': {},
                'round': {1: False, 2: False}
                },
      'lucy': {'pw': '2345',
               'char': None,
               'ap': 4,
               'clue': {},
               'round': {1: False, 2: False}
               }})
])
def test_create_user(user_id, pw, expected):
    from database import create_user
    user_dict = create_user(user_id, pw)
    assert user_dict == expected


@pytest.mark.parametrize("user_id, char, expected_user, expected_track", [
    ('lucy',
     'A',
     {'heidi': {'pw': '1234',
                'char': None,
                'ap': 4,
                'clue': {},
                'round': {1: False, 2: False}
                },
      'lucy': {'pw': '2345',
               'char': 'A',
               'ap': 4,
               'clue': {},
               'round': {1: False, 2: False}
               }},
     {'A': True, 'B': False, 'C': False}),
    ('heidi',
     'B',
     {'heidi': {'pw': '1234',
                'char': 'B',
                'ap': 4,
                'clue': {},
                'round': {1: False, 2: False}
                },
      'lucy': {'pw': '2345',
               'char': 'A',
               'ap': 4,
               'clue': {},
               'round': {1: False, 2: False}
               }},
     {'A': True, 'B': True, 'C': False})
])
def test_add_char(user_id, char, expected_user, expected_track):
    from database import add_char
    user, track = add_char(user_id, char)
    assert user == expected_user and \
        track['chars'] == expected_track
