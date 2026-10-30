import requests
import pytest

URL = "http://127.0.0.1/index.php?s=/Home/User/do_login"


def test_login_success():
    """正向用例：账号密码正确，登录成功"""
    s = requests.Session()
    r = s.post(
        URL,
        data={
            "username": "15915407513@163.com",
            "password": "123456",
            "verify_code": "0000",
        },
        timeout=10,
    )
    assert r.status_code == 200
    assert r.json()["status"] == 1


@pytest.mark.parametrize(
    "username, password, expected_status",
    [
        ("15915407513@163.com", "wrong123", -2),  # 密码错误
        ("", "123456", 0),                        # 账号为空
    ],
)
def test_login_fail(username, password, expected_status):
    """反向用例：登录失败"""
    r = requests.post(
        URL,
        data={
            "username": username,
            "password": password,
            "verify_code": "0000",
        },
        timeout=10,
    )
    assert r.status_code == 200
    assert r.json()["status"] == expected_status