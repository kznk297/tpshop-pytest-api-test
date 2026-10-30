import re

import pytest


@pytest.mark.parametrize(
    "data, expected_msg",
    [
        ({"goods_id": 114, "goods_num": 0, "item_id": 127}, "购买商品数量不能为0"),
        ({"goods_id": 114, "goods_num": 201, "item_id": 127}, "购买商品数量大于200"),
        ({"goods_num": 1, "item_id": 127}, "请选择要购买的商品"),
        ({"goods_id": 114, "goods_num": 1}, "必须传递商品规格"),
    ],
)
def test_add_cart_fail(auth_session, data, expected_msg):
    """加购异常场景：参数校验"""
    r = auth_session.post(
        "http://127.0.0.1/index.php?m=Home&c=Cart&a=add",
        data=data,
        timeout=10,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == 0
    assert expected_msg in body["msg"]

def test_add_cart(auth_session):
    """加购：正常商品，加入成功"""
    r = auth_session.post(
        "http://127.0.0.1/index.php?m=Home&c=Cart&a=add",
        data={
            "goods_id": 114,
            "goods_num": 1,
            "item_id": 127,
        },
        timeout=10,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == 1
    assert "加入购物车成功" in body["msg"]



def test_order_flow(auth_session):
    """完整链路：加购 -> 查购物车 -> 取地址 -> 提交订单"""
    base = "http://127.0.0.1"

    # 1. 加入购物车
    r = auth_session.post(
        f"{base}/index.php?m=Home&c=Cart&a=add",
        data={"goods_id": 114, "goods_num": 1, "item_id": 127},
        timeout=10,
    )
    assert r.json()["status"] == 1

    # 2. 查询购物车
    r = auth_session.get(
        f"{base}/index.php?m=Home&c=Cart&a=header_cart_list",
        timeout=10,
    )
    assert r.status_code == 200
    assert "cart_quantity" in r.text

    # 3. 获取收货地址，并从中提取 address_id
    r = auth_session.get(
        f"{base}/index.php?m=Home&c=Cart&a=ajaxAddress",
        timeout=10,
    )
    assert "收货人信息" in r.text

    match = re.search(
        r'class="addressItem[^"]*"\s+data-address-id="(\d+)"',
        r.text,
    )
    assert match, "页面里没有找到收货地址"
    address_id = match.group(1)

    # 4. 用提取到的 address_id 提交订单
    r = auth_session.post(
        f"{base}/index.php?m=Home&c=Cart&a=cart3",
        data={"address_id": address_id, "act": "submit_order"},
        timeout=20,
    )
    body = r.json()
    assert body["status"] == 1
    assert body["result"], "没有拿到订单号"

    print("订单号:", body["result"])

    
