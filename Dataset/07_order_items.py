#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEP 7: Create olist_order_items_dataset_vn_new.csv
Requires:
- olist_orders_dataset_vn_new.csv
- olist_products_dataset_vn.csv
- olist_sellers_dataset_vn.csv
"""
from __future__ import annotations

# =========================
# Inlined common.py (no extra file needed)
# =========================

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

# ===== Default sizes (match your provided dataset sizes) =====
N_CUSTOMERS = 5000
N_ORDERS = 12000
N_ORDER_ITEMS = 36000
N_PAYMENTS = 6500
N_REVIEWS = 6500
N_SELLERS = 120
N_GEO = 625
N_PRODUCTS = 53


def make_rng(seed: int, salt: int) -> np.random.Generator:
    """
    Deterministic RNG per step.
    Using different salts keeps each script stable and reproducible.
    """
    return np.random.default_rng(seed + salt * 10_000)


def set_py_random(seed: int, salt: int) -> None:
    random.seed(seed + salt * 10_000 + 123)


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_csv(df: pd.DataFrame, path: Path, force: bool) -> None:
    """
    Write CSV with utf-8-sig (Excel-friendly). Refuse overwrite non-empty unless --force.
    """
    if path.exists() and (not force) and path.stat().st_size > 0:
        raise FileExistsError(f"File đã tồn tại và không rỗng: {path}. Dùng --force để ghi đè.")
    df.to_csv(path, index=False, encoding="utf-8-sig")


def make_id(prefix: str, i: int, width: int = 5) -> str:
    return f"{prefix}_{i:0{width}d}"


def random_datetimes(rng: np.random.Generator, start: datetime, end: datetime, n: int) -> List[datetime]:
    total_sec = int((end - start).total_seconds())
    offsets = rng.integers(0, total_sec + 1, size=n)
    return [start + timedelta(seconds=int(x)) for x in offsets]


@dataclass(frozen=True)
class CityStateCoord:
    city: str
    state: str
    lat: float
    lng: float


# ===== Categories =====
CATEGORIES: List[Tuple[str, str]] = [
    ("electronics", "Điện tử"),
    ("computers_accessories", "Máy tính & phụ kiện"),
    ("home_appliances", "Đồ điện gia dụng"),
    ("furniture", "Nội thất"),
    ("fashion_men", "Thời trang nam"),
    ("fashion_women", "Thời trang nữ"),
    ("beauty_health", "Làm đẹp & sức khỏe"),
    ("sports_leisure", "Thể thao & dã ngoại"),
    ("toys", "Đồ chơi"),
    ("groceries", "Hàng tiêu dùng"),
]

CUSTOMER_CITY_STATE: List[Tuple[str, str]] = [
    ("Thu Duc", "TD"),
    ("Da Nang", "DN"),
    ("Ho Chi Minh", "HCM"),
    ("Ha Noi", "HN"),
    ("Hai Phong", "HP"),
    ("Can Tho", "CT"),
    ("Nha Trang", "NT"),
    ("Thanh Hoa", "TH"),
    ("Buon Ma Thuot", "BMT"),
    ("Bien Hoa", "BH"),
    ("Hue", "HUE"),
    ("Vinh", "VINH"),
]

SELLER_GEO: List[CityStateCoord] = [
    CityStateCoord("Ho Chi Minh City", "HCM", 10.7769, 106.7009),
    CityStateCoord("Ha Noi", "HN", 21.0285, 105.8542),
    CityStateCoord("Da Nang", "DN", 16.0544, 108.2022),
    CityStateCoord("Hai Phong", "HP", 20.8449, 106.6881),
    CityStateCoord("Can Tho", "CT", 10.0452, 105.7469),
    CityStateCoord("Nha Trang", "KH", 12.2388, 109.1967),
    CityStateCoord("Hue", "TTH", 16.4637, 107.5909),
    CityStateCoord("Vung Tau", "BRVT", 10.4114, 107.1362),
]

PRODUCT_POOL: Dict[str, List[Tuple[str, str]]] = {
    "electronics": [
        ("Sony", "Tai nghe Sony WH-1000XM5"),
        ("Samsung", "Smart TV Samsung 55 inch 4K"),
        ("Xiaomi", "Máy lọc không khí Xiaomi 4 Lite"),
        ("JBL", "Loa Bluetooth JBL Charge 5"),
        ("LG", "Màn hình LG 27 inch IPS"),
        ("Panasonic", "Máy ảnh Panasonic Lumix"),
        ("Apple", "AirPods Pro (Gen 2)"),
    ],
    "computers_accessories": [
        ("ASUS", "Laptop ASUS VivoBook 15"),
        ("Apple", "Laptop MacBook Air M2"),
        ("Dell", "Laptop Dell XPS 13"),
        ("Logitech", "Chuột Logitech MX Master 3S"),
        ("Keychron", "Bàn phím cơ Keychron K6"),
        ("Seagate", "Ổ cứng di động Seagate 1TB"),
    ],
    "home_appliances": [
        ("Sharp", "Nồi cơm điện Sharp 1.8L"),
        ("Panasonic", "Máy sấy tóc Panasonic EH-NA"),
        ("Philips", "Nồi chiên không dầu Philips 4.1L"),
        ("Electrolux", "Máy hút bụi Electrolux"),
        ("Sunhouse", "Ấm siêu tốc Sunhouse 1.7L"),
    ],
    "furniture": [
        ("Nội thất OEM", "Bàn làm việc gỗ tự nhiên"),
        ("Nội thất OEM", "Ghế công thái học lưng lưới"),
        ("Nội thất OEM", "Kệ sách 5 tầng"),
        ("IKEA", "Tủ quần áo 2 cánh"),
        ("Nội thất OEM", "Bàn trà phòng khách"),
    ],
    "fashion_men": [
        ("Uniqlo", "Áo thun nam Uniqlo Airism"),
        ("Nike", "Áo khoác thể thao Nike"),
        ("Adidas", "Quần jogger Adidas"),
        ("Levi's", "Quần jeans Levi's 511"),
        ("Zara", "Sơ mi nam Zara slimfit"),
    ],
    "fashion_women": [
        ("Uniqlo", "Áo len nữ Uniqlo"),
        ("Zara", "Đầm nữ Zara midi"),
        ("H&M", "Áo khoác nữ H&M"),
        ("Charles & Keith", "Túi xách Charles & Keith"),
        ("Converse", "Giày Converse Chuck 70"),
    ],
    "beauty_health": [
        ("Anessa", "Kem chống nắng Anessa SPF50+"),
        ("3CE", "Son 3CE Velvet Lip Tint"),
        ("Cetaphil", "Sữa rửa mặt Cetaphil Gentle"),
        ("La Roche-Posay", "Kem dưỡng La Roche-Posay Cicaplast"),
        ("Dior", "Nước hoa Dior J’adore"),
    ],
    "sports_leisure": [
        ("Yonex", "Vợt cầu lông Yonex"),
        ("Decathlon", "Thảm yoga Decathlon 6mm"),
        ("Adidas", "Bóng đá Adidas size 5"),
        ("Naturehike", "Lều cắm trại Naturehike 2P"),
        ("Speedo", "Kính bơi Speedo"),
    ],
    "toys": [
        ("LEGO", "Bộ xếp hình LEGO City"),
        ("Hasbro", "Búp bê Barbie"),
        ("Mattel", "Xe mô hình Hot Wheels"),
        ("Montessori OEM", "Đồ chơi Montessori gỗ"),
        ("Ravensburger", "Tranh ghép hình 1000 mảnh"),
    ],
    "groceries": [
        ("Vinamilk", "Sữa tươi Vinamilk 1L"),
        ("Acecook", "Mì Hảo Hảo thùng 30 gói"),
        ("Trung Nguyên", "Cà phê Trung Nguyên G7"),
        ("Chinsu", "Nước mắm Chinsu 500ml"),
        ("Kinh Đô", "Bánh quy Kinh Đô hộp"),
    ],
}


def product_category_counts() -> Dict[str, int]:
    """
    Match your dataset logic: electronics=7, computers_accessories=6, other categories=5
    Total = 53 products.
    """
    d: Dict[str, int] = {"electronics": 7, "computers_accessories": 6}
    for c, _ in CATEGORIES:
        if c not in d:
            d[c] = 5
    return d


import argparse
from datetime import timedelta
from pathlib import Path
import numpy as np
import pandas as pd
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", default=".", help="Output directory (and input dir)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    out_dir = Path(args.out_dir).resolve()
    ensure_dir(out_dir)
    rng = make_rng(args.seed, salt=7)

    orders_path = out_dir / "olist_orders_dataset_vn_new.csv"
    products_path = out_dir / "olist_products_dataset_vn.csv"
    sellers_path = out_dir / "olist_sellers_dataset_vn.csv"

    for p in [orders_path, products_path, sellers_path]:
        if not p.exists():
            raise FileNotFoundError(f"Missing input: {p}")

    orders_df = pd.read_csv(orders_path)
    products_df = pd.read_csv(products_path)
    sellers_df = pd.read_csv(sellers_path)

    order_ids = orders_df["order_id"].tolist()
    if len(order_ids) != N_ORDERS:
        raise ValueError(f"Expected {N_ORDERS} orders, got {len(order_ids)}")

    # distribution 2/3/4 items (match your dataset totals)
    counts = ([2] * 3970) + ([3] * 4060) + ([4] * 3970)
    rng.shuffle(counts)
    if len(counts) != N_ORDERS or sum(counts) != N_ORDER_ITEMS:
        raise ValueError("Invalid item count distribution")

    active_sellers = rng.choice(sellers_df["seller_id"].values, size=80, replace=False)
    product_ids = products_df["product_id"].values

    # popularity weights (slight skew)
    ranks = np.arange(1, len(product_ids) + 1)
    w = 1 / (ranks ** 0.9)
    w = w / w.sum()

    order2approved = pd.to_datetime(orders_df.set_index("order_id")["order_approved_at"])

    rows = []
    for oid, n in zip(order_ids, counts):
        approved_dt = order2approved.loc[oid].to_pydatetime()
        ship_limit = (approved_dt + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

        picked_products = rng.choice(product_ids, size=int(n), replace=False, p=w)
        for k, pid in enumerate(picked_products, start=1):
            sid = rng.choice(active_sellers)
            price = float(np.round(rng.uniform(200_000, 6_000_000), 2))
            freight = float(np.round(rng.uniform(6_000, 900_000), 2))
            rows.append((oid, k, pid, sid, ship_limit, price, freight))

    df = pd.DataFrame(
        rows,
        columns=[
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "price",
            "freight_value",
        ],
    )

    if len(df) != N_ORDER_ITEMS:
        raise ValueError(f"Expected {N_ORDER_ITEMS} order_items, got {len(df)}")

    write_csv(df, out_dir / "olist_order_items_dataset_vn_new.csv", args.force)
    print("OK: olist_order_items_dataset_vn_new.csv")


if __name__ == "__main__":
    main()
