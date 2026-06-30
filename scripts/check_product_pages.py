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
        "craft_labels": ["裁切工艺", "覆膜工艺", "配件"],
    },
    "special-paper-card": {
        "heading": "特种纸卡片报价",
        "quantity_label": "数量(张)",
        "craft_labels": ["基础工艺", "常见工艺"],
    },
    "insert-card": {
        "heading": "插卡报价",
        "quantity_label": "数量(个)",
        "craft_labels": ["工艺"],
    },
    "keychain": {
        "heading": "钥匙扣报价",
        "quantity_label": "数量(个)",
        "craft_labels": ["常见工艺", "配件"],
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
        craft_labels = [group["label"] for group in page["craft_groups"]]
        assert_equal(craft_labels, hints["craft_labels"], f"{slug} 工艺字段不正确")

    print("product pages ok")


if __name__ == "__main__":
    main()
