import os
from datetime import datetime, UTC
from functools import wraps
from pathlib import Path

from flask import Flask, abort, flash, make_response, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "app.db"

PRODUCT_PAGES = [
    {
        "slug": "sticker",
        "name": "不干胶",
        "endpoint": "quote",
        "template": "index.html",
    },
    {
        "slug": "insert-flag",
        "name": "牙签插旗",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "牙签插旗报价",
        "description": "按领淘插旗页面字段整理成本地牙签插旗报价页，先用本地 demo 规则快速出价。",
        "badge": "牙签插旗",
        "type_label": "品种",
        "types": ["铜板纸不干胶"],
        "default_type": "铜板纸不干胶",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "5*7",
        "extra_fields": [
            {
                "key": "toothpickSize",
                "label": "牙签尺寸(CM/厘米)",
                "output_label": "牙签尺寸",
                "kind": "select",
                "options": ["6.5 CM", "8 CM", "10 CM"],
                "default": "6.5 CM",
                "position": "after_size",
            },
        ],
        "quantity_label": "数量(张)",
        "quantity_options": [500, 1000, 2000],
        "default_quantity": 500,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "cut", "label": "裁切工艺", "multi": False, "options": ["模切"], "default_options": ["模切"]},
            {"key": "lamination", "label": "覆膜工艺", "multi": False, "options": ["覆亮膜"], "default_options": ["覆亮膜"]},
            {"key": "accessory", "label": "配件", "multi": True, "options": ["粘牙签", "配牙签"], "default_options": ["配牙签"]},
        ],
        "pricing": {
            "base_price": {"铜板纸不干胶": 68},
            "area_steps": [{"max": 30, "fee": 0}, {"max": 60, "fee": 12}, {"max": 100, "fee": 24}, {"max": 999999, "fee": 45}],
            "quantity_fee": {500: 0, 1000: 32, 2000: 70},
            "craft_fee": {"模切": 8, "覆亮膜": 12, "粘牙签": 18, "配牙签": 10},
        },
        "result_lines": ["牙签插旗当前为本地 demo 报价，真实生产价后续可接领淘基线。", "默认按单面印刷和配牙签场景整理。"],
        "preview_label": "牙签插旗效果预览",
        "preview_badge": "TOOTHPICK FLAG",
        "preview_note": "Food Flag Card",
    },
    {
        "slug": "special-paper-card",
        "name": "特种纸卡片",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "特种纸卡片报价",
        "description": "由领淘特种纸名片页面改名而来，用于本地特种纸卡片报价演示。",
        "badge": "特种纸卡片",
        "type_label": "材料",
        "types": ["刚古纸", "莱妮纸", "冰白纸", "珠光纸", "荷兰白卡"],
        "default_type": "刚古纸",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "9*5.4",
        "quantity_label": "数量(张)",
        "quantity_options": [200, 500, 1000],
        "default_quantity": 200,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "craft", "label": "工艺", "multi": True, "options": ["打孔", "异形模切", "圆角", "打点线", "压痕", "配流苏", "穿流苏", "单面烫金", "双面烫金"], "default_options": []},
            {"key": "commonCraft", "label": "常见工艺", "multi": True, "options": ["打码"], "default_options": []},
        ],
        "pricing": {
            "base_price": {"刚古纸": 36, "莱妮纸": 38, "冰白纸": 42, "珠光纸": 46, "荷兰白卡": 40},
            "area_steps": [{"max": 50, "fee": 0}, {"max": 80, "fee": 8}, {"max": 120, "fee": 16}, {"max": 999999, "fee": 30}],
            "quantity_fee": {200: 0, 500: 18, 1000: 36},
            "craft_fee": {
                "打孔": 5,
                "异形模切": 18,
                "圆角": 6,
                "打点线": 8,
                "压痕": 8,
                "配流苏": 12,
                "穿流苏": 12,
                "打码": 10,
                "单面烫金": 28,
                "双面烫金": 48,
            },
        },
        "result_lines": ["特种纸卡片当前为本地 demo 报价，工艺费用按展示规则叠加。", "涉及异形模切、烫金等复杂工艺时，正式下单前建议人工复核。"],
        "preview_label": "特种纸卡片效果预览",
        "preview_badge": "SPECIAL PAPER CARD",
        "preview_note": "Textured Card",
    },
    {
        "slug": "insert-card",
        "name": "插卡",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "插卡报价",
        "description": "按领淘插卡页面整理成本地报价页，保留品种、尺寸、数量、款数和工艺字段。",
        "badge": "插卡",
        "type_label": "品种",
        "types": ["白卡纸插卡"],
        "default_type": "白卡纸插卡",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "9*5.4",
        "quantity_label": "数量(个)",
        "quantity_options": [200, 500, 1000],
        "default_quantity": 200,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "craft", "label": "工艺", "multi": False, "options": ["模切"], "default_options": []},
        ],
        "pricing": {
            "base_price": {"白卡纸插卡": 28},
            "area_steps": [{"max": 50, "fee": 0}, {"max": 80, "fee": 8}, {"max": 120, "fee": 16}, {"max": 999999, "fee": 28}],
            "quantity_fee": {200: 0, 500: 16, 1000: 34},
            "craft_fee": {"模切": 10},
        },
        "result_lines": ["插卡当前为本地 demo 报价，真实价格后续可按领淘样本补齐。", "默认按常规纸卡单面印刷场景整理。"],
        "preview_label": "插卡效果预览",
        "preview_badge": "INSERT CARD",
        "preview_note": "Package Insert",
    },
    {
        "slug": "keychain",
        "name": "钥匙扣",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "钥匙扣报价",
        "description": "按领淘钥匙扣页面整理成本地报价页，保留材质、厚度、尺寸、数量、款数和配件字段。",
        "badge": "钥匙扣",
        "type_label": "材质",
        "types": ["亚克力", "PVC", "金属"],
        "default_type": "亚克力",
        "extra_fields": [
            {
                "key": "thickness",
                "label": "厚度",
                "output_label": "厚度",
                "kind": "select",
                "options": ["3.6mm"],
                "default": "3.6mm",
            },
        ],
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "5*5",
        "quantity_label": "数量(个)",
        "quantity_options": [100, 500, 1000],
        "default_quantity": 100,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "commonCraft", "label": "常见工艺", "multi": False, "options": ["打孔"], "default_options": ["打孔"]},
            {"key": "accessory", "label": "配件", "multi": True, "options": ["标准款", "经济款", "龙虾款", "时尚款", "珠链款", "D扣款", "星星款", "彩绳款", "彩圈铃铛款", "门扣款"], "default_options": ["标准款"]},
        ],
        "pricing": {
            "base_price": {"亚克力": 58, "PVC": 48, "金属": 88},
            "area_steps": [{"max": 20, "fee": 0}, {"max": 40, "fee": 12}, {"max": 80, "fee": 24}, {"max": 999999, "fee": 45}],
            "quantity_fee": {100: 0, 500: 35, 1000: 70},
            "craft_fee": {"打孔": 0, "标准款": 0, "经济款": 0, "龙虾款": 0, "时尚款": 0, "珠链款": 0, "D扣款": 0, "星星款": 0, "彩绳款": 0, "彩圈铃铛款": 0, "门扣款": 0},
        },
        "result_lines": ["钥匙扣当前为本地 demo 报价，材质和配件按展示规则叠加。", "如果后续要精准对价，需要补领淘对应工艺基线。"],
        "preview_label": "钥匙扣效果预览",
        "preview_badge": "KEYCHAIN",
        "preview_note": "Accessory Quote",
    },
    {
        "slug": "banner",
        "name": "条幅",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "条幅报价",
        "description": "输入基础尺寸、数量和款数，快速生成条幅报价说明。",
        "badge": "宣传物料",
        "types": ["普通条幅", "加厚条幅", "刀刮布条幅"],
        "default_type": "普通条幅",
        "size_label": "尺寸(M/米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "2*0.8",
        "quantity_label": "数量(条)",
        "quantity_options": [1, 5, 10],
        "default_quantity": 5,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "edge", "label": "工艺", "multi": False, "options": ["缝筒", "打扣", "四角吊耳", "净裁"], "default_options": ["缝筒"]},
        ],
        "pricing": {
            "base_price": {"普通条幅": 18, "加厚条幅": 24, "刀刮布条幅": 36},
            "area_steps": [{"max": 2, "fee": 0}, {"max": 5, "fee": 12}, {"max": 10, "fee": 28}, {"max": 999999, "fee": 55}],
            "quantity_fee": {1: 0, 5: 25, 10: 60},
            "craft_fee": {"缝筒": 0, "打扣": 0, "四角吊耳": 0, "净裁": 0},
        },
        "result_lines": ["默认含排版，常规地区可发物流或快递。", "加急订单请先和客服确认截单时间。"],
        "preview_label": "条幅效果预览",
        "preview_badge": "BANNER QUOTE",
        "preview_note": "Promotional Display",
    },
    {
        "slug": "card",
        "name": "卡片",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "卡片报价",
        "description": "用于名片、吊卡、小卡片场景，提供基础报价演示。",
        "badge": "纸类印刷",
        "types": ["铜版卡片", "白卡卡片", "哑粉卡片"],
        "default_type": "铜版卡片",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "9*5.4",
        "quantity_label": "数量(张)",
        "quantity_options": [500, 1000, 2000],
        "default_quantity": 1000,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "print", "label": "印刷方式", "multi": False, "options": ["单面印刷", "双面印刷", "专色印刷"]},
            {"key": "extra", "label": "附加工艺", "multi": True, "options": ["圆角", "覆哑膜", "烫金"]},
        ],
        "pricing": {
            "base_price": {"铜版卡片": 26, "白卡卡片": 22, "哑粉卡片": 30},
            "area_steps": [{"max": 50, "fee": 0}, {"max": 80, "fee": 6}, {"max": 120, "fee": 12}, {"max": 999999, "fee": 22}],
            "quantity_fee": {500: 12, 1000: 22, 2000: 40},
            "craft_fee": {"单面印刷": 0, "双面印刷": 10, "专色印刷": 18, "圆角": 6, "覆哑膜": 8, "烫金": 15},
        },
        "result_lines": ["默认含基础排版，文字较多建议转曲后上传。", "异形模切卡片需要按刀版另行确认。"],
        "preview_label": "卡片效果预览",
        "preview_badge": "CARD PRINT",
        "preview_note": "Paper Marketing",
    },
    {
        "slug": "pvc",
        "name": "PVC",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "PVC报价",
        "description": "适用于 PVC 卡、PVC 标识类产品，先给一版可直接演示的报价页。",
        "badge": "耐用材质",
        "types": ["PVC卡片", "PVC吊牌", "PVC标牌"],
        "default_type": "PVC卡片",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "8.5*5.4",
        "quantity_label": "数量(个)",
        "quantity_options": [100, 300, 500],
        "default_quantity": 300,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "surface", "label": "表面处理", "multi": False, "options": ["亮面", "哑面", "磨砂"]},
            {"key": "extra", "label": "附加工艺", "multi": True, "options": ["打孔", "平码", "喷码"]},
        ],
        "pricing": {
            "base_price": {"PVC卡片": 58, "PVC吊牌": 66, "PVC标牌": 72},
            "area_steps": [{"max": 50, "fee": 0}, {"max": 100, "fee": 10}, {"max": 180, "fee": 18}, {"max": 999999, "fee": 32}],
            "quantity_fee": {100: 16, 300: 34, 500: 52},
            "craft_fee": {"亮面": 0, "哑面": 4, "磨砂": 8, "打孔": 5, "平码": 8, "喷码": 12},
        },
        "result_lines": ["PVC 类默认按单面报价，双面内容可在备注里补充。", "如涉及芯片卡或磁条卡，需要单独核价。"],
        "preview_label": "PVC效果预览",
        "preview_badge": "PVC PRODUCT",
        "preview_note": "Durable Display",
    },
    {
        "slug": "uv-transfer",
        "name": "金属标-UV转印贴",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "金属标-UV转印贴报价",
        "description": "适合做金属质感标识和转印贴场景，先用简版规则接待客户。",
        "badge": "工艺贴标",
        "types": ["普通UV转印贴", "金属拉丝UV贴", "立体滴胶UV贴"],
        "default_type": "普通UV转印贴",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "6*3",
        "quantity_label": "数量(枚)",
        "quantity_options": [100, 300, 500],
        "default_quantity": 300,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "finish", "label": "表面效果", "multi": False, "options": ["亮光", "哑光", "拉丝"]},
            {"key": "extra", "label": "附加工艺", "multi": True, "options": ["背胶加强", "定位膜", "加急"]},
        ],
        "pricing": {
            "base_price": {"普通UV转印贴": 66, "金属拉丝UV贴": 88, "立体滴胶UV贴": 108},
            "area_steps": [{"max": 20, "fee": 0}, {"max": 40, "fee": 9}, {"max": 80, "fee": 18}, {"max": 999999, "fee": 30}],
            "quantity_fee": {100: 18, 300: 36, 500: 58},
            "craft_fee": {"亮光": 0, "哑光": 4, "拉丝": 10, "背胶加强": 6, "定位膜": 10, "加急": 22},
        },
        "result_lines": ["默认按单图单位置计算，多位置贴标建议拆单确认。", "曲面贴附效果与材质有关，正式生产前建议先打样。"],
        "preview_label": "UV转印贴预览",
        "preview_badge": "UV TRANSFER",
        "preview_note": "Metallic Sticker",
    },
    {
        "slug": "fridge-magnet",
        "name": "冰箱贴",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "冰箱贴报价",
        "description": "适合文创、伴手礼、品牌周边的基础报价演示。",
        "badge": "文创周边",
        "types": ["软磁冰箱贴", "滴胶冰箱贴", "异形冰箱贴"],
        "default_type": "软磁冰箱贴",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "7*7",
        "quantity_label": "数量(个)",
        "quantity_options": [100, 300, 500],
        "default_quantity": 300,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "shape", "label": "形状方案", "multi": False, "options": ["方形", "圆形", "异形模切"]},
            {"key": "extra", "label": "附加项", "multi": True, "options": ["亮膜", "滴胶", "独立包装"]},
        ],
        "pricing": {
            "base_price": {"软磁冰箱贴": 42, "滴胶冰箱贴": 58, "异形冰箱贴": 65},
            "area_steps": [{"max": 36, "fee": 0}, {"max": 64, "fee": 8}, {"max": 100, "fee": 16}, {"max": 999999, "fee": 28}],
            "quantity_fee": {100: 14, 300: 28, 500: 46},
            "craft_fee": {"方形": 0, "圆形": 4, "异形模切": 10, "亮膜": 4, "滴胶": 12, "独立包装": 6},
        },
        "result_lines": ["文创类产品默认按普通磁吸强度报价。", "如果需要高磁或礼盒包装，需要单独确认。"],
        "preview_label": "冰箱贴效果预览",
        "preview_badge": "MAGNET QUOTE",
        "preview_note": "Creative Gift",
    },
    {
        "slug": "coaster",
        "name": "杯垫",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "杯垫报价",
        "description": "先放一版杯垫报价 demo，方便前台切换展示。",
        "badge": "桌面用品",
        "types": ["纸质杯垫", "PVC杯垫", "软木杯垫"],
        "default_type": "纸质杯垫",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "9*9",
        "quantity_label": "数量(个)",
        "quantity_options": [100, 300, 500],
        "default_quantity": 300,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "shape", "label": "外形方案", "multi": False, "options": ["方形", "圆形", "异形"]},
            {"key": "extra", "label": "附加工艺", "multi": True, "options": ["吸水层", "覆膜", "加厚"]},
        ],
        "pricing": {
            "base_price": {"纸质杯垫": 28, "PVC杯垫": 45, "软木杯垫": 52},
            "area_steps": [{"max": 64, "fee": 0}, {"max": 100, "fee": 8}, {"max": 144, "fee": 15}, {"max": 999999, "fee": 26}],
            "quantity_fee": {100: 12, 300: 24, 500: 40},
            "craft_fee": {"方形": 0, "圆形": 4, "异形": 8, "吸水层": 10, "覆膜": 4, "加厚": 9},
        },
        "result_lines": ["餐饮渠道常做 300 起，更多数量可以再往下压。", "如需成套包装，建议在备注里标明包装数量。"],
        "preview_label": "杯垫效果预览",
        "preview_badge": "COASTER DEMO",
        "preview_note": "Tabletop Product",
    },
    {
        "slug": "class-flag",
        "name": "班旗",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "班旗报价",
        "description": "适合学校活动、社团活动等场景，先做成基础可演示页。",
        "badge": "校园活动",
        "types": ["班旗旗面", "班旗整套", "运动会班旗"],
        "default_type": "班旗整套",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 高 * 宽</span>",
        "default_size": "96*144",
        "quantity_label": "数量(套)",
        "quantity_options": [1, 3, 5],
        "default_quantity": 3,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "material", "label": "旗面材质", "multi": False, "options": ["经编布", "贡缎布", "牛津布"]},
            {"key": "extra", "label": "附加项", "multi": True, "options": ["配旗杆", "流苏", "加急"]},
        ],
        "pricing": {
            "base_price": {"班旗旗面": 36, "班旗整套": 68, "运动会班旗": 82},
            "area_steps": [{"max": 8000, "fee": 0}, {"max": 15000, "fee": 15}, {"max": 25000, "fee": 28}, {"max": 999999, "fee": 48}],
            "quantity_fee": {1: 0, 3: 18, 5: 38},
            "craft_fee": {"经编布": 0, "贡缎布": 8, "牛津布": 12, "配旗杆": 18, "流苏": 10, "加急": 20},
        },
        "result_lines": ["学校活动类一般建议至少提前 2-3 天确认稿件。", "若需双面不同内容，需要按双面印刷另算。"],
        "preview_label": "班旗效果预览",
        "preview_badge": "CLASS FLAG",
        "preview_note": "Campus Event",
    },
]

LEGACY_PRODUCT_PAGES = [
    {
        "slug": "sticker",
        "name": "不干胶",
        "endpoint": "quote",
        "template": "index.html",
    },
    {
        "slug": "banner",
        "name": "条幅",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "条幅报价",
        "description": "输入基础尺寸、数量和款数，快速生成条幅报价说明。",
        "badge": "宣传物料",
        "types": ["普通条幅", "加厚条幅", "刀刮布条幅"],
        "default_type": "普通条幅",
        "size_label": "尺寸(M/米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "2*0.8",
        "quantity_label": "数量(条)",
        "quantity_options": [1, 5, 10],
        "default_quantity": 5,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "edge", "label": "边缘工艺", "multi": False, "options": ["普通裁切", "锁边打扣", "穿杆口"]},
            {"key": "extra", "label": "附加工艺", "multi": True, "options": ["单面喷绘", "双面喷绘", "加急"]},
        ],
        "pricing": {
            "base_price": {"普通条幅": 18, "加厚条幅": 24, "刀刮布条幅": 36},
            "area_steps": [{"max": 2, "fee": 0}, {"max": 5, "fee": 12}, {"max": 10, "fee": 28}, {"max": 999999, "fee": 55}],
            "quantity_fee": {1: 0, 5: 25, 10: 60},
            "craft_fee": {"普通裁切": 0, "锁边打扣": 8, "穿杆口": 12, "单面喷绘": 0, "双面喷绘": 26, "加急": 20},
        },
        "result_lines": ["默认含排版，常规地区可发物流或快递。", "加急订单请先和客服确认截单时间。"],
        "preview_label": "条幅效果预览",
        "preview_badge": "BANNER QUOTE",
        "preview_note": "Promotional Display",
    },
    {
        "slug": "insert-flag",
        "name": "插旗",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "插旗报价",
        "description": "适合活动布置和引流展示，先用 demo 规则给客户快速回价。",
        "badge": "活动布置",
        "types": ["刀旗", "沙滩旗", "注水旗"],
        "default_type": "刀旗",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 高 * 宽</span>",
        "default_size": "180*60",
        "quantity_label": "数量(套)",
        "quantity_options": [1, 3, 5],
        "default_quantity": 3,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "pole", "label": "旗杆方案", "multi": False, "options": ["普通旗杆", "加厚旗杆", "铝合金旗杆"]},
            {"key": "extra", "label": "附加项", "multi": True, "options": ["含底座", "含收纳袋", "加急"]},
        ],
        "pricing": {
            "base_price": {"刀旗": 48, "沙滩旗": 72, "注水旗": 95},
            "area_steps": [{"max": 8000, "fee": 0}, {"max": 15000, "fee": 18}, {"max": 25000, "fee": 35}, {"max": 999999, "fee": 58}],
            "quantity_fee": {1: 0, 3: 28, 5: 55},
            "craft_fee": {"普通旗杆": 0, "加厚旗杆": 12, "铝合金旗杆": 24, "含底座": 18, "含收纳袋": 6, "加急": 20},
        },
        "result_lines": ["默认按整套报价，印刷和支架一起算。", "如需单独补旗面，可按备注重新核价。"],
        "preview_label": "插旗效果预览",
        "preview_badge": "FLAG DISPLAY",
        "preview_note": "Event Promotion",
    },
    {
        "slug": "card",
        "name": "卡片",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "卡片报价",
        "description": "用于名片、吊卡、小卡片场景，提供基础报价演示。",
        "badge": "纸类印刷",
        "types": ["铜版卡片", "白卡卡片", "哑粉卡片"],
        "default_type": "铜版卡片",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "9*5.4",
        "quantity_label": "数量(张)",
        "quantity_options": [500, 1000, 2000],
        "default_quantity": 1000,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "print", "label": "印刷方式", "multi": False, "options": ["单面印刷", "双面印刷", "专色印刷"]},
            {"key": "extra", "label": "附加工艺", "multi": True, "options": ["圆角", "覆哑膜", "烫金"]},
        ],
        "pricing": {
            "base_price": {"铜版卡片": 26, "白卡卡片": 22, "哑粉卡片": 30},
            "area_steps": [{"max": 50, "fee": 0}, {"max": 80, "fee": 6}, {"max": 120, "fee": 12}, {"max": 999999, "fee": 22}],
            "quantity_fee": {500: 12, 1000: 22, 2000: 40},
            "craft_fee": {"单面印刷": 0, "双面印刷": 10, "专色印刷": 18, "圆角": 6, "覆哑膜": 8, "烫金": 15},
        },
        "result_lines": ["默认含基础排版，文字较多建议转曲后上传。", "异形模切卡片需要按刀版另行确认。"],
        "preview_label": "卡片效果预览",
        "preview_badge": "CARD PRINT",
        "preview_note": "Paper Marketing",
    },
    {
        "slug": "pvc",
        "name": "PVC",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "PVC报价",
        "description": "适用于 PVC 卡、PVC 标识类产品，先给一版可直接演示的报价页。",
        "badge": "耐用材质",
        "types": ["PVC卡片", "PVC吊牌", "PVC标牌"],
        "default_type": "PVC卡片",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "8.5*5.4",
        "quantity_label": "数量(个)",
        "quantity_options": [100, 300, 500],
        "default_quantity": 300,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "surface", "label": "表面处理", "multi": False, "options": ["亮面", "哑面", "磨砂"]},
            {"key": "extra", "label": "附加工艺", "multi": True, "options": ["打孔", "平码", "喷码"]},
        ],
        "pricing": {
            "base_price": {"PVC卡片": 58, "PVC吊牌": 66, "PVC标牌": 72},
            "area_steps": [{"max": 50, "fee": 0}, {"max": 100, "fee": 10}, {"max": 180, "fee": 18}, {"max": 999999, "fee": 32}],
            "quantity_fee": {100: 16, 300: 34, 500: 52},
            "craft_fee": {"亮面": 0, "哑面": 4, "磨砂": 8, "打孔": 5, "平码": 8, "喷码": 12},
        },
        "result_lines": ["PVC 类默认按单面报价，双面内容可在备注里补充。", "如涉及芯片卡或磁条卡，需要单独核价。"],
        "preview_label": "PVC效果预览",
        "preview_badge": "PVC PRODUCT",
        "preview_note": "Durable Display",
    },
    {
        "slug": "uv-transfer",
        "name": "金属标-UV转印贴",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "金属标-UV转印贴报价",
        "description": "适合做金属质感标识和转印贴场景，先用简版规则接待客户。",
        "badge": "工艺贴标",
        "types": ["普通UV转印贴", "金属拉丝UV贴", "立体滴胶UV贴"],
        "default_type": "普通UV转印贴",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "6*3",
        "quantity_label": "数量(枚)",
        "quantity_options": [100, 300, 500],
        "default_quantity": 300,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "finish", "label": "表面效果", "multi": False, "options": ["亮光", "哑光", "拉丝"]},
            {"key": "extra", "label": "附加工艺", "multi": True, "options": ["背胶加强", "定位膜", "加急"]},
        ],
        "pricing": {
            "base_price": {"普通UV转印贴": 66, "金属拉丝UV贴": 88, "立体滴胶UV贴": 108},
            "area_steps": [{"max": 20, "fee": 0}, {"max": 40, "fee": 9}, {"max": 80, "fee": 18}, {"max": 999999, "fee": 30}],
            "quantity_fee": {100: 18, 300: 36, 500: 58},
            "craft_fee": {"亮光": 0, "哑光": 4, "拉丝": 10, "背胶加强": 6, "定位膜": 10, "加急": 22},
        },
        "result_lines": ["默认按单图单位置计算，多位置贴标建议拆单确认。", "曲面贴附效果与材质有关，正式生产前建议先打样。"],
        "preview_label": "UV转印贴预览",
        "preview_badge": "UV TRANSFER",
        "preview_note": "Metallic Sticker",
    },
    {
        "slug": "fridge-magnet",
        "name": "冰箱贴",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "冰箱贴报价",
        "description": "适合文创、伴手礼、品牌周边的基础报价演示。",
        "badge": "文创周边",
        "types": ["软磁冰箱贴", "滴胶冰箱贴", "异形冰箱贴"],
        "default_type": "软磁冰箱贴",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "7*7",
        "quantity_label": "数量(个)",
        "quantity_options": [100, 300, 500],
        "default_quantity": 300,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "shape", "label": "形状方案", "multi": False, "options": ["方形", "圆形", "异形模切"]},
            {"key": "extra", "label": "附加项", "multi": True, "options": ["亮膜", "滴胶", "独立包装"]},
        ],
        "pricing": {
            "base_price": {"软磁冰箱贴": 42, "滴胶冰箱贴": 58, "异形冰箱贴": 65},
            "area_steps": [{"max": 36, "fee": 0}, {"max": 64, "fee": 8}, {"max": 100, "fee": 16}, {"max": 999999, "fee": 28}],
            "quantity_fee": {100: 14, 300: 28, 500: 46},
            "craft_fee": {"方形": 0, "圆形": 4, "异形模切": 10, "亮膜": 4, "滴胶": 12, "独立包装": 6},
        },
        "result_lines": ["文创类产品默认按普通磁吸强度报价。", "如果需要高磁或礼盒包装，需要单独确认。"],
        "preview_label": "冰箱贴效果预览",
        "preview_badge": "MAGNET QUOTE",
        "preview_note": "Creative Gift",
    },
    {
        "slug": "coaster",
        "name": "杯垫",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "杯垫报价",
        "description": "先放一版杯垫报价 demo，方便前台切换展示。",
        "badge": "桌面用品",
        "types": ["纸质杯垫", "PVC杯垫", "软木杯垫"],
        "default_type": "纸质杯垫",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 长 * 宽</span>",
        "default_size": "9*9",
        "quantity_label": "数量(个)",
        "quantity_options": [100, 300, 500],
        "default_quantity": 300,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "shape", "label": "外形方案", "multi": False, "options": ["方形", "圆形", "异形"]},
            {"key": "extra", "label": "附加工艺", "multi": True, "options": ["吸水层", "覆膜", "加厚"]},
        ],
        "pricing": {
            "base_price": {"纸质杯垫": 28, "PVC杯垫": 45, "软木杯垫": 52},
            "area_steps": [{"max": 64, "fee": 0}, {"max": 100, "fee": 8}, {"max": 144, "fee": 15}, {"max": 999999, "fee": 26}],
            "quantity_fee": {100: 12, 300: 24, 500: 40},
            "craft_fee": {"方形": 0, "圆形": 4, "异形": 8, "吸水层": 10, "覆膜": 4, "加厚": 9},
        },
        "result_lines": ["餐饮渠道常做 300 起，更多数量可以再往下压。", "如需成套包装，建议在备注里标明包装数量。"],
        "preview_label": "杯垫效果预览",
        "preview_badge": "COASTER DEMO",
        "preview_note": "Tabletop Product",
    },
    {
        "slug": "class-flag",
        "name": "班旗",
        "endpoint": "product_quote",
        "template": "product_quote.html",
        "heading": "班旗报价",
        "description": "适合学校活动、社团活动等场景，先做成基础可演示页。",
        "badge": "校园活动",
        "types": ["班旗旗面", "班旗整套", "运动会班旗"],
        "default_type": "班旗整套",
        "size_label": "尺寸(CM/厘米) <span class=\"warn\">输入格式: 高 * 宽</span>",
        "default_size": "96*144",
        "quantity_label": "数量(套)",
        "quantity_options": [1, 3, 5],
        "default_quantity": 3,
        "style_label": "款数",
        "default_style_count": 1,
        "craft_groups": [
            {"key": "material", "label": "旗面材质", "multi": False, "options": ["经编布", "贡缎布", "牛津布"]},
            {"key": "extra", "label": "附加项", "multi": True, "options": ["配旗杆", "流苏", "加急"]},
        ],
        "pricing": {
            "base_price": {"班旗旗面": 36, "班旗整套": 68, "运动会班旗": 82},
            "area_steps": [{"max": 8000, "fee": 0}, {"max": 15000, "fee": 15}, {"max": 25000, "fee": 28}, {"max": 999999, "fee": 48}],
            "quantity_fee": {1: 0, 3: 18, 5: 38},
            "craft_fee": {"经编布": 0, "贡缎布": 8, "牛津布": 12, "配旗杆": 18, "流苏": 10, "加急": 20},
        },
        "result_lines": ["学校活动类一般建议至少提前 2-3 天确认稿件。", "若需双面不同内容，需要按双面印刷另算。"],
        "preview_label": "班旗效果预览",
        "preview_badge": "CLASS FLAG",
        "preview_note": "Campus Event",
    },
]

PRODUCTS_BY_SLUG = {item["slug"]: item for item in PRODUCT_PAGES}

db = SQLAlchemy()
login_manager = LoginManager()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    last_login_at = db.Column(db.DateTime, nullable=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "请先登录后再继续。"

    def asset_url(filename: str) -> str:
        static_file = Path(app.static_folder) / filename
        version = int(static_file.stat().st_mtime) if static_file.exists() else 0
        return url_for("static", filename=filename, v=version)

    app.jinja_env.globals["asset_url"] = asset_url

    @app.context_processor
    def inject_now() -> dict[str, datetime]:
        return {"now": datetime.now(UTC), "product_pages": PRODUCT_PAGES}

    register_routes(app)

    with app.app_context():
        init_database()

    return app


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return db.session.get(User, int(user_id))


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):
        if current_user.role != "admin":
            abort(403)
        return view(*args, **kwargs)

    return wrapped_view


def init_database() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    db.create_all()

    seed_users = [
        ("admin", "Admin@123456", "admin"),
        ("user1", "User@123456", "user"),
    ]

    for username, password, role in seed_users:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            continue

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()


def validate_username(username: str) -> str | None:
    if len(username) < 3:
        return "用户名至少需要 3 个字符。"
    if len(username) > 32:
        return "用户名不能超过 32 个字符。"
    if not username.replace("_", "").replace("-", "").isalnum():
        return "用户名只允许字母、数字、下划线和短横线。"
    return None


def validate_password(password: str) -> str | None:
    if len(password) < 8:
        return "密码至少需要 8 个字符。"
    return None


def register_routes(app: Flask) -> None:
    @app.route("/")
    def home():
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        return redirect(url_for("quote"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("quote"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = User.query.filter_by(username=username).first()

            if not user or not user.check_password(password):
                flash("用户名或密码错误。", "error")
                return render_template("login.html"), 401

            if not user.is_active:
                flash("当前账户已被停用，请联系管理员。", "error")
                return render_template("login.html"), 403

            user.last_login_at = datetime.now(UTC)
            db.session.commit()
            login_user(user)
            flash("登录成功。", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("quote"))

        return render_template("login.html")

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        flash("已退出登录。", "success")
        return redirect(url_for("login"))

    @app.route("/quote")
    @login_required
    def quote():
        response = make_response(render_template("index.html", active_product="sticker"))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.route("/quote/<product_slug>")
    @login_required
    def product_quote(product_slug: str):
        product = PRODUCTS_BY_SLUG.get(product_slug)
        if product is None or product["slug"] == "sticker":
            abort(404)

        response = make_response(render_template(product["template"], product=product, active_product=product_slug))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.route("/records")
    @login_required
    def records():
        return redirect(url_for("quote"))

    @app.route("/account")
    @login_required
    def account():
        return render_template("account.html")

    @app.route("/account/password", methods=["POST"])
    @login_required
    def account_change_password():
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not current_user.check_password(current_password):
            flash("当前密码不正确。", "error")
            return redirect(url_for("account"))

        password_error = validate_password(new_password)
        if password_error:
            flash(password_error, "error")
            return redirect(url_for("account"))

        if new_password != confirm_password:
            flash("两次输入的新密码不一致。", "error")
            return redirect(url_for("account"))

        current_user.set_password(new_password)
        db.session.commit()
        flash("密码已更新。", "success")
        return redirect(url_for("account"))

    @app.route("/admin")
    @admin_required
    def admin_dashboard():
        stats = {
            "total_users": User.query.count(),
            "admin_users": User.query.filter_by(role="admin").count(),
            "normal_users": User.query.filter_by(role="user").count(),
            "active_users": User.query.filter_by(is_active=True).count(),
        }
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        return render_template("admin_dashboard.html", stats=stats, recent_users=recent_users)

    @app.route("/admin/users")
    @admin_required
    def admin_users():
        users = User.query.order_by(User.role.asc(), User.created_at.asc()).all()
        return render_template("admin_users.html", users=users)

    @app.route("/admin/users/create", methods=["POST"])
    @admin_required
    def admin_users_create():
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "user").strip()

        username_error = validate_username(username)
        if username_error:
            flash(username_error, "error")
            return redirect(url_for("admin_users"))

        password_error = validate_password(password)
        if password_error:
            flash(password_error, "error")
            return redirect(url_for("admin_users"))

        if role not in {"admin", "user"}:
            flash("角色参数不合法。", "error")
            return redirect(url_for("admin_users"))

        if User.query.filter_by(username=username).first():
            flash("用户名已存在，请更换。", "error")
            return redirect(url_for("admin_users"))

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash(f"账户 {username} 已创建。", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/users/<int:user_id>/toggle-active", methods=["POST"])
    @admin_required
    def admin_users_toggle_active(user_id: int):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)

        if user.id == current_user.id:
            flash("不能停用当前登录的管理员账户。", "error")
            return redirect(url_for("admin_users"))

        user.is_active = not user.is_active
        db.session.commit()
        status_text = "启用" if user.is_active else "停用"
        flash(f"账户 {user.username} 已{status_text}。", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/users/<int:user_id>/reset-password", methods=["POST"])
    @admin_required
    def admin_users_reset_password(user_id: int):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)

        new_password = request.form.get("new_password", "")
        password_error = validate_password(new_password)
        if password_error:
            flash(f"{user.username} 重置失败：{password_error}", "error")
            return redirect(url_for("admin_users"))

        user.set_password(new_password)
        db.session.commit()
        flash(f"账户 {user.username} 密码已重置。", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/users/<int:user_id>/rename", methods=["POST"])
    @admin_required
    def admin_users_rename(user_id: int):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)

        new_username = request.form.get("username", "").strip()
        username_error = validate_username(new_username)
        if username_error:
            flash(f"{user.username} 修改失败：{username_error}", "error")
            return redirect(url_for("admin_users"))

        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != user.id:
            flash("新用户名已存在，请更换。", "error")
            return redirect(url_for("admin_users"))

        old_username = user.username
        user.username = new_username
        db.session.commit()
        flash(f"账户 {old_username} 已改名为 {new_username}。", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/users/<int:user_id>/change-role", methods=["POST"])
    @admin_required
    def admin_users_change_role(user_id: int):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)

        new_role = request.form.get("role", "").strip()
        if new_role not in {"admin", "user"}:
            flash("角色参数不合法。", "error")
            return redirect(url_for("admin_users"))

        if user.id == current_user.id and new_role != "admin":
            flash("不能把当前登录的管理员账户降级为普通用户。", "error")
            return redirect(url_for("admin_users"))

        old_role = user.role
        user.role = new_role
        db.session.commit()
        flash(f"账户 {user.username} 角色已从 {old_role} 改为 {new_role}。", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
    @admin_required
    def admin_users_delete(user_id: int):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)

        if user.id == current_user.id:
            flash("不能删除当前登录的管理员账户。", "error")
            return redirect(url_for("admin_users"))

        if user.role == "admin":
            admin_count = User.query.filter_by(role="admin").count()
            if admin_count <= 1:
                flash("不能删除系统中的最后一个管理员账户。", "error")
                return redirect(url_for("admin_users"))

        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f"账户 {username} 已删除。", "success")
        return redirect(url_for("admin_users"))

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("403.html"), 403


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
