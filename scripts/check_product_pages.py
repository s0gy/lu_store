import ast
from pathlib import Path


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"

EXPECTED_PAGES = [
    ("sticker", "不干胶", "quote"),
    ("insert-flag", "牙签插旗", "product_quote"),
    ("special-paper-card", "特种纸卡片", "product_quote"),
    ("insert-card", "插卡", "product_quote"),
    ("keychain", "钥匙扣", "product_quote"),
]

REMOVED_SLUGS = {
    "banner",
    "card",
    "pvc",
    "uv-transfer",
    "fridge-magnet",
    "coaster",
    "class-flag",
}

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
    assert_equal(summary, EXPECTED_PAGES, "产品页清单不符合目标五页")

    slugs = {item["slug"] for item in pages}
    leftovers = sorted(slugs & REMOVED_SLUGS)
    assert_equal(leftovers, [], "旧 demo 产品页仍然出现在 PRODUCT_PAGES 中")

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
