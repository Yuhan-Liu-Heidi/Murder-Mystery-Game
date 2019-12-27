# test database
import pytest


@pytest.mark.parametrize("user_id, pw, expected", [
    ('heidi',
     '1234',
     {'heidi': {'pw': '1234',
                'char': {'name': None, 'story': None},
                'ap': 4,
                'clue': {},
                'round': {1: False, 2: False}
                }}),
    ('lucy',
     '2345',
     {'heidi': {'pw': '1234',
                'char': {'name': None, 'story': None},
                'ap': 4,
                'clue': {},
                'round': {1: False, 2: False}
                },
      'lucy': {'pw': '2345',
               'char': {'name': None, 'story': None},
               'ap': 4,
               'clue': {},
               'round': {1: False, 2: False}
               }})
])
def test_create_user(user_id, pw, expected):
    from database import create_user
    user_dict = create_user(user_id, pw)
    assert user_dict == expected
