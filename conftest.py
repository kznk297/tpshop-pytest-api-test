import os

import pytest
import requests

import pymysql


@pytest.fixture
def db():
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "123456"),
        database=os.getenv("DB_NAME", "tpshop"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
    yield conn
    conn.close()

BASE_URL = os.getenv("TPSHOP_BASE_URL", "http://127.0.0.1")
USERNAME = os.getenv("TPSHOP_USERNAME", "15915407513@163.com")
PASSWORD = os.getenv("TPSHOP_PASSWORD", "123456")


@pytest.fixture
def auth_session():
    """每次用例登录一次，返回已登录的 Session"""
    sess = requests.Session()
    r = sess.post(
        f"{BASE_URL}/index.php?s=/Home/User/do_login",
        data={
            "username": USERNAME,
            "password": PASSWORD,
            "verify_code": "0000",
        },
        timeout=10,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == 1, body


    sess.user_id = body["result"]["user_id"]

    yield sess

