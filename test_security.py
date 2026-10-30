import pytest


@pytest.mark.xfail(
    strict=True,
    reason="已知缺陷：提交订单未校验 address_id 归属（IDOR）",
)
def test_order_with_other_users_address(auth_session):
    """使用他人收货地址下单，预期应被拒绝"""
    base = "http://127.0.0.1"

    r = auth_session.post(
        f"{base}/index.php?m=Home&c=Cart&a=add",
        data={"goods_id": 114, "goods_num": 1, "item_id": 127},
        timeout=10,
    )
    assert r.json()["status"] == 1

    r = auth_session.post(
        f"{base}/index.php?m=Home&c=Cart&a=cart3",
        data={"address_id": 4, "act": "submit_order"},
        timeout=20,
    )
    body = r.json()
    assert body["status"] == 0, f"越权下单成功，订单号={body.get('result')}"