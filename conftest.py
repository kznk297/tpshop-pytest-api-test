import pytest
import requests

BASE_URL = "http://127.0.0.1"


@pytest.fixture
def auth_session():
    """登录一次，返回已登录的 Session，供用例复用"""
    s = requests.Session()
    r = s.post(
        f"{BASE_URL}/index.php?s=/Home/User/do_login",
        data={
            "username": "15915407513@163.com",
            "password": "123456",
            "verify_code": "0000",
        },
        timeout=10,
    )
    assert r.status_code == 200
    assert r.json()["status"] == 1
    return s