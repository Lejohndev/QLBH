import pandas as pd
import random

# ========================
# CONFIG
# ========================
NUM_CUSTOMERS = 5000
CUSTOMERS_OUT = "olist_customers_dataset_vn_new.csv"

# Danh sách tỉnh thành VN (phân bố thực tế)
VIETNAM_CITIES = [
    ("Ho Chi Minh", "HCM"),
    ("Ha Noi", "HN"),
    ("Da Nang", "DN"),
    ("Can Tho", "CT"),
    ("Hai Phong", "HP"),
    ("Bien Hoa", "BH"),
    ("Thu Duc", "TD"),
    ("Nha Trang", "NT"),
    ("Hue", "HUE"),
    ("Buon Ma Thuot", "BMT"),
    ("Thanh Hoa", "TH"),
    ("Vinh", "VINH"),
]

def random_zip():
    """Sinh zip code 700000 → 980000 theo vùng thực tế."""
    return random.randint(700000, 980000)

def main():
    rows = []

    for i in range(1, NUM_CUSTOMERS + 1):
        cid = f"CUS_{i:05d}"
        unique_id = f"UNIQ_{i:05d}"

        city, state = random.choice(VIETNAM_CITIES)

        rows.append({
            "customer_id": cid,
            "customer_unique_id": unique_id,
            "customer_zip_code_prefix": random_zip(),
            "customer_city": city,
            "customer_state": state
        })

    df = pd.DataFrame(rows)
    df.to_csv(CUSTOMERS_OUT, index=False, encoding="utf-8")

    print(">>> DONE!")
    print(f"  • Sinh {NUM_CUSTOMERS} khách hàng")
    print(f"  • File: {CUSTOMERS_OUT}")

if __name__ == "__main__":
    main()
