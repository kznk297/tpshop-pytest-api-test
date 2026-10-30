# TPshop 商城接口自动化测试

基于 TPshop 开源商城的 Python 接口自动化测试项目，覆盖登录、购物车、下单全链路，
并将实际发现的越权缺陷沉淀为回归用例。

## 技术栈

- Python 3.11
- pytest 9
- requests
- pytest-html

## 覆盖范围

| 模块 | 用例数 | 说明 |
| --- | --- | --- |
| 登录 | 3 | 正向登录、密码错误、账号为空 |
| 购物车 | 5 | 正常加购，以及数量 0/201、缺商品 ID、缺规格 |
| 下单链路 | 1 | 加购 → 查购物车 → 提取地址 → 提交订单 |
| 安全回归 | 1 | 他人收货地址越权下单（已知缺陷） |

当前结果：**9 passed, 1 xfailed**

## 项目结构

```text
tp-shop-api-test/
├── conftest.py        # 登录 fixture，提供已登录 Session
├── test_login.py      # 登录正反向用例
├── test_cart.py       # 加购异常与完整下单链路
├── test_security.py   # 越权缺陷回归用例
├── pytest.ini         # pytest 配置
└── requirements.txt   # 依赖
```

## 快速开始

1. 本地启动 TPshop，确保 `http://127.0.0.1` 可访问
2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 运行全部用例：

```bash
pytest -v
```

4. 生成 HTML 报告：

```bash
pytest -v --html=report.html --self-contained-html
```

## 已发现缺陷

**提交订单接口未校验收货地址归属（水平越权 / IDOR）**

- 登录账号传入他人的 `address_id`，仍可成功下单
- 已沉淀为 `test_security.py` 中的回归用例
- 当前使用 `xfail(strict=True)` 标记，后端修复后该用例会变为 XPASS，
  提醒维护者移除标记

## 说明

- 账号为本地测试环境账号，仅用于演示
- 所有用例针对本地 TPshop 实例运行
