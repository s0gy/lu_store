import ast
from pathlib import Path


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"

EXPECTED_PAGES = [
    ("sticker", "不干胶", "quote"),
    ("insert-flag", "牙签插旗", "product_quote"),
    ("special-paper-card", "特种纸卡片", "product_quote"),
    ("insert-card", "插卡", "product_quote"),
    ("keychain", "钥匙扣", "product_quote"),
    ("banner", "条幅", "product_quote"),
    ("card", "卡片", "product_quote"),
    ("pvc", "PVC", "product_quote"),
    ("uv-transfer", "金属标-UV转印贴", "product_quote"),
    ("fridge-magnet", "冰箱贴", "product_quote"),
    ("coaster", "杯垫", "product_quote"),
    ("class-flag", "班旗", "product_quote"),
]

EXPECTED_FIELD_HINTS = {
    "insert-flag": {
        "heading": "牙签插旗报价",
        "quantity_label": "数量(张)",
        "craft_groups": [
            ("裁切工艺", ["模切", "裁切"], ["模切"]),
            ("覆膜工艺", ["覆哑膜", "覆亮膜", "不覆膜"], []),
            ("配件", ["配牙签", "粘牙签", "配刮刮膜", "粘刮刮膜"], ["配牙签"]),
        ],
    },
    "special-paper-card": {
        "heading": "特种纸卡片报价",
        "quantity_label": "数量(张)",
        "craft_groups": [
            ("工艺", ["打孔", "异形模切", "圆角", "打点线", "压痕", "配流苏", "穿流苏", "单面烫金", "双面烫金"], []),
            ("常见工艺", ["打码"], []),
        ],
    },
    "insert-card": {
        "heading": "插卡报价",
        "quantity_label": "数量(个)",
        "craft_groups": [
            ("工艺", ["模切"], []),
        ],
    },
    "keychain": {
        "heading": "钥匙扣报价",
        "quantity_label": "数量(个)",
        "craft_groups": [
            ("常见工艺", ["打孔"], ["打孔"]),
            ("配件", ["配件"], []),
        ],
    },
    "banner": {
        "heading": "条幅报价",
        "quantity_label": "数量(条)",
        "craft_groups": [
            ("边缘工艺", ["普通裁切", "锁边打扣", "穿杆口"], []),
            ("附加工艺", ["单面喷绘", "双面喷绘", "加急"], []),
        ],
    },
    "card": {
        "heading": "卡片报价",
        "quantity_label": "数量(张)",
        "craft_groups": [
            ("印刷方式", ["单面印刷", "双面印刷", "专色印刷"], []),
            ("附加工艺", ["圆角", "覆哑膜", "烫金"], []),
        ],
    },
    "pvc": {
        "heading": "PVC报价",
        "quantity_label": "数量(个)",
        "craft_groups": [
            ("表面处理", ["亮面", "哑面", "磨砂"], []),
            ("附加工艺", ["打孔", "平码", "喷码"], []),
        ],
    },
    "uv-transfer": {
        "heading": "金属标-UV转印贴报价",
        "quantity_label": "数量(枚)",
        "craft_groups": [
            ("表面效果", ["亮光", "哑光", "拉丝"], []),
            ("附加工艺", ["背胶加强", "定位膜", "加急"], []),
        ],
    },
    "fridge-magnet": {
        "heading": "冰箱贴报价",
        "quantity_label": "数量(个)",
        "craft_groups": [
            ("形状方案", ["方形", "圆形", "异形模切"], []),
            ("附加项", ["亮膜", "滴胶", "独立包装"], []),
        ],
    },
    "coaster": {
        "heading": "杯垫报价",
        "quantity_label": "数量(个)",
        "craft_groups": [
            ("外形方案", ["方形", "圆形", "异形"], []),
            ("附加工艺", ["吸水层", "覆膜", "加厚"], []),
        ],
    },
    "class-flag": {
        "heading": "班旗报价",
        "quantity_label": "数量(套)",
        "craft_groups": [
            ("旗面材质", ["经编布", "贡缎布", "牛津布"], []),
            ("附加项", ["配旗杆", "流苏", "加急"], []),
        ],
    },
}


def load_product_pages():
    tree = ast.parse(APP_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "PRODUCT_PAGES":
                    return ast.literal_eval(node.value)
    raise AssertionError("未找到 PRODUCT_PAGES 配置")


def assert_equal(actual, expected, message):
    if actual != expected:
        raise AssertionError(f"{message}\n实际: {actual!r}\n期望: {expected!r}")


def main():
    pages = load_product_pages()
    summary = [(item["slug"], item["name"], item["endpoint"]) for item in pages]
    assert_equal(summary, EXPECTED_PAGES, "产品页清单不符合目标页面清单")

    slugs = {item["slug"] for item in pages}
    assert_equal(len(slugs), len(pages), "产品页 slug 出现重复")
    names = [item["name"] for item in pages]
    assert_equal("插旗" in names, False, "旧插旗页面不应恢复，保留当前牙签插旗")

    by_slug = {item["slug"]: item for item in pages}
    for slug, hints in EXPECTED_FIELD_HINTS.items():
        page = by_slug[slug]
        assert_equal(page["heading"], hints["heading"], f"{slug} 标题不正确")
        assert_equal(page["quantity_label"], hints["quantity_label"], f"{slug} 数量字段不正确")
        craft_groups = [
            (group["label"], group["options"], group.get("default_options", []))
            for group in page["craft_groups"]
        ]
        assert_equal(craft_groups, hints["craft_groups"], f"{slug} 工艺字段不正确")

    print("product pages ok")


if __name__ == "__main__":
    main()
