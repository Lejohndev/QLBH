


import pandas as pd
import json

# ===========================
# 1. Path CSV input
# ===========================
CUSTOMERS_CSV    = "olist_customers_dataset_vn_new.csv"
ORDERS_CSV       = "olist_orders_dataset_vn_new.csv"
ORDER_ITEMS_CSV  = "olist_order_items_dataset_vn_new.csv"
PRODUCTS_CSV     = "olist_products_dataset_vn.csv"

# ===========================
# 2. Output
# ===========================
OUT_CSV    = "olist_recommender_transactions_mix.csv"
OUT_ARFF   = "olist_recommender_transactions_mix.arff"
OUT_LOOKUP = "product_lookup.json"
    

# ==================================================================
# Build 1 row vector {product_id = t / ?}
#   - t : sản phẩm có xuất hiện trong transaction
#   - ? : không dùng, để missing (tránh rule dạng product=f)
# ==================================================================
def build_matrix_from_group(group_series, product_ids, prefix):
    rows = []

    for idx, prod_list in group_series.items():
        # Loại trùng lặp trong 1 transaction
        prod_set = set(prod_list)

        # Bỏ transaction rỗng (phòng hờ)
        if len(prod_set) == 0:
            continue

        row = {"transaction_id": f"{prefix}_{idx}"}
        for pid in product_ids:
            row[pid] = "t" if pid in prod_set else "f"   # t/f tạm, lát sẽ đổi f -> ?
        rows.append(row)

    return pd.DataFrame(rows)


def main():
    print("\n==============================")
    print("  BUILD TRAIN DATASET")
    print("==============================\n")

    # -------------------------------------------------
    # Đọc dữ liệu nguồn
    # -------------------------------------------------
    orders      = pd.read_csv(ORDERS_CSV, encoding="utf-8")
    order_items = pd.read_csv(ORDER_ITEMS_CSV, encoding="utf-8")
    customers   = pd.read_csv(CUSTOMERS_CSV, encoding="utf-8")
    products    = pd.read_csv(PRODUCTS_CSV, encoding="utf-8")

    # -------------------------------------------------
    # Tạo lookup sản phẩm cho web (JSON)
    # -------------------------------------------------
    lookup = {}
    for _, r in products.iterrows():
        pid = r["product_id"]
        lookup[pid] = {
            "name":     r.get("product_name", ""),
            "category": r.get("product_category_name", ""),
            "brand":    r.get("product_brand", "")
        }

    with open(OUT_LOOKUP, "w", encoding="utf-8") as f:
        json.dump(lookup, f, indent=4, ensure_ascii=False)

    print(f">>> Created {OUT_LOOKUP}")

    # -------------------------------------------------
    # Danh sách product_id cố định (53 sản phẩm của bạn)
    # -------------------------------------------------
    product_ids = sorted(products["product_id"].unique().tolist())
    print(f">>> Tổng sản phẩm: {len(product_ids)}")

    # Chỉ giữ order_items chứa product_id hợp lệ
    order_items = order_items[order_items["product_id"].isin(product_ids)]

    # ==================================================================
    # 1) TRANSACTION THEO ĐƠN HÀNG (ORD)
    # ==================================================================
    print("\n>>> Transaction theo đơn hàng (ORD)")
    order_group = order_items.groupby("order_id")["product_id"].apply(list)
    order_matrix = build_matrix_from_group(order_group, product_ids, prefix="ORD")
    print("    Số ORD transaction (trước lọc):", len(order_matrix))

    # ==================================================================
    # 2) TRANSACTION THEO KHÁCH HÀNG (CUS)
    # ==================================================================
    print(">>> Transaction theo khách hàng (CUS)")
    orders_small = orders[["order_id", "customer_id"]]
    oi_join = order_items.merge(orders_small, on="order_id", how="left")

    customer_group = oi_join.groupby("customer_id")["product_id"].apply(list)
    customer_matrix = build_matrix_from_group(customer_group, product_ids, prefix="CUS")
    print("    Số CUS transaction (trước lọc):", len(customer_matrix))

    # ==================================================================
    # 3) GỘP & LỌC TRANSACTION
    #    - Gộp ORD + CUS
    #    - Chỉ giữ transaction có ít nhất 2 sản phẩm được mua (>=2 't')
    # ==================================================================
    combined = pd.concat([order_matrix, customer_matrix], ignore_index=True)
    combined = combined[["transaction_id"] + product_ids]

    # Đếm số 't' trên từng transaction
    t_counts = (combined[product_ids] == "t").sum(axis=1)
    before_filter = len(combined)
    combined = combined[t_counts >= 2].reset_index(drop=True)
    after_filter = len(combined)

    print(f"\n>>> Tổng transaction trước lọc : {before_filter}")
    print(f">>> Giữ lại (>= 2 sản phẩm)     : {after_filter}")

    # Đổi 'f' -> '?' để chỉ encode "có mua" (t) và missing
    for pid in product_ids:
        combined[pid] = combined[pid].apply(lambda v: "t" if v == "t" else "?")

    # -------------------------------------------------
    # 4) Lưu CSV (giữ transaction_id để debug / kiểm tra)
    # -------------------------------------------------
    combined.to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(">>> Saved CSV:", OUT_CSV)

    # -------------------------------------------------
    # 5) Tạo file ARFF cho Weka (BỎ transaction_id)
    #     - Attribute: {t,f} nhưng data chỉ dùng t hoặc ?
    #       (Weka hiểu ? là missing, sẽ KHÔNG sinh rule với =f)
    # -------------------------------------------------
    print(">>> Tạo file ARFF cho Weka:", OUT_ARFF)
    with open(OUT_ARFF, "w", encoding="utf-8") as f:
        f.write("@RELATION olist_recommender_transactions_mix\n\n")

        for pid in product_ids:
            f.write(f"@ATTRIBUTE {pid} {{t,f}}\n")

        f.write("\n@DATA\n")

        for _, row in combined.iterrows():
            values = [row[pid] for pid in product_ids]  # chỉ 't' hoặc '?'
            f.write(",".join(values) + "\n")

    print("\n>>> DONE!!!")
    print("    File train CSV :", OUT_CSV)
    print("    File ARFF      :", OUT_ARFF)
    print("    File lookup    :", OUT_LOOKUP)


if __name__ == "__main__":
    main()

