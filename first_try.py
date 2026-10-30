import requests

s = requests.Session()
r = s.post(
  "http://127.0.0.1/index.php?s=/Home/User/do_login",
    data={
        "username": "15915407513@163.com",
        "password": "123456",
        "verify_code": "0000",
    },
    timeout=10,
)

print("状态码:", r.status_code)
print("返回:", r.text[:500])