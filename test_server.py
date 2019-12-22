import pytest


@pytest.mark.parametrize("ID, p, expected", [("Heidi", "0326", None),
                                             ("Heidi", "326", "密码不正确"),
                                             ("Heid", "0326", "用户名不正确")])
def test_verify_user(ID, p, expected):
    from server import verify_user, new_user, user_dict
    new_user("Heidi", "0326")
    result = verify_user(ID, p)
    assert result == expected
