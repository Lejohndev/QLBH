#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEP 8: Create olist_order_payments_dataset_vn.csv
Requires: olist_orders_dataset_vn_new.csv
(Only for ORD_00001..ORD_06500 to match your dataset)
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
    rng = make_rng(args.seed, salt=8)

    orders_path = out_dir / "olist_orders_dataset_vn_new.csv"
    if not orders_path.exists():
        raise FileNotFoundError(f"Missing input: {orders_path}")

    orders_df = pd.read_csv(orders_path)
    order_ids = orders_df["order_id"].tolist()
    pay_orders = order_ids[:N_PAYMENTS]

    payment_types = ["credit_card", "boleto", "voucher", "debit_card"]
    pt_weights = np.array([0.593, 0.207, 0.105, 0.095], dtype=float)
    pt_weights = pt_weights / pt_weights.sum()

    inst_values = np.array([1, 2, 3, 4, 5, 6])
    inst_weights = np.array([0.45, 0.16, 0.12, 0.11, 0.09, 0.07], dtype=float)
    inst_weights = inst_weights / inst_weights.sum()

    pay_vals = rng.lognormal(mean=np.log(2.3e6), sigma=0.5, size=N_PAYMENTS)
    pay_vals = np.clip(pay_vals, 48_000, 7_600_000)
    pay_vals = np.round(pay_vals, 2)

    rows = []
    for i, oid in enumerate(pay_orders):
        rows.append(
            (
                oid,
                1,
                str(rng.choice(payment_types, p=pt_weights)),
                int(rng.choice(inst_values, p=inst_weights)),
                float(pay_vals[i]),
            )
        )

    df = pd.DataFrame(
        rows,
        columns=["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"],
    )
    write_csv(df, out_dir / "olist_order_payments_dataset_vn.csv", args.force)
    print("OK: olist_order_payments_dataset_vn.csv")


if __name__ == "__main__":
    main()
