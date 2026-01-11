import sys
import math
import pandas as pd
from itertools import combinations

#-N 1200 -T 0 -C 0.55 -D 0.01 -U 0.9 -M 0.01
# ============================
# CẤU HÌNH 
# ============================
MIN_SUPPORT = 0.01     # -M 0.01   (tối thiểu 1% giao dịch)
MIN_CONFIDENCE = 0.55  # -C 0.55   (độ tin cậy tối thiểu)
MAX_RULES = 1200       # -N 1200   (tối đa 1200 luật xuất ra)
MAX_ITEMSET_SIZE = 5   # giới hạn kích thước tập mục (có thể chỉnh 4–5 cho nhẹ)


# ============================
# ĐỌC TRANSACTIONS TỪ CSV
# ============================
def load_transactions_from_csv(path: str):
    """
    Đọc file CSV dạng:
        transaction_id,PRD_00001,PRD_00002,...,PRD_00053
        ORD_1,t,?,...,t
    Trả về:
        - transactions: list[frozenset(items)]
        - all_items: list[item_name]
    """
    df = pd.read_csv(path)

    # Coi như mọi cột trừ 'transaction_id' là item nhị phân
    item_columns = [c for c in df.columns if c != "transaction_id"]

    transactions = []
    for _, row in df.iterrows():
        items = []
        for col in item_columns:
            val = str(row[col]).strip().lower()
            # Chỉ tính 't' là mua, các giá trị khác (?, f, NaN) bỏ qua
            if val == "t":
                items.append(col)
        transactions.append(frozenset(items))

    return transactions, item_columns


# ============================
# TÍNH SUPPORT
# ============================
def get_support_counts(transactions, candidates):
    """
    Đếm support (số lần xuất hiện) của mỗi ứng viên trong transactions.
    candidates: iterable[frozenset]
    """
    counts = {c: 0 for c in candidates}
    for txn in transactions:
        for c in candidates:
            if c.issubset(txn):
                counts[c] += 1
    return counts


# ============================
# TẠO CANDIDATE (Apriori join)
# ============================
def generate_candidates(prev_frequents, k):
    """
    Sinh tập ứng viên C_k từ L_{k-1}
    prev_frequents: list[frozenset] (tập phổ biến kích thước k-1)
    """
    prev_list = list(prev_frequents)
    candidates = set()
    n = len(prev_list)

    for i in range(n):
        for j in range(i + 1, n):
            a = prev_list[i]
            b = prev_list[j]
            # join nếu k-2 phần tử đầu giống nhau
            union = a.union(b)
            if len(union) == k:
                # kiểm tra tính "Apriori" (mọi tập con k-1 của union phải nằm trong prev_frequents)
                all_subsets_ok = True
                for subset in combinations(union, k - 1):
                    if frozenset(subset) not in prev_frequents:
                        all_subsets_ok = False
                        break
                if all_subsets_ok:
                    candidates.add(frozenset(union))

    return candidates


# ============================
# CHẠY APRIORI
# ============================
def apriori(transactions, min_support_ratio, max_itemset_size=MAX_ITEMSET_SIZE):
    """
    Trả về:
      - support_counts: dict[frozenset, int]
      - frequent_itemsets_by_k: dict[k, list[frozenset]]
    """
    n_txn = len(transactions)
    min_support_count = math.ceil(min_support_ratio * n_txn)

    # L1: tất cả item đơn lẻ
    item_counts = {}
    for txn in transactions:
        for item in txn:
            key = frozenset([item])
            item_counts[key] = item_counts.get(key, 0) + 1

    L1 = [item for item, cnt in item_counts.items() if cnt >= min_support_count]
    support_counts = {k: v for k, v in item_counts.items() if k in L1}
    frequent_by_k = {1: L1}

    # L_k cho k >= 2
    k = 2
    current_L = L1
    while current_L and k <= max_itemset_size:
        candidates = generate_candidates(set(current_L), k)
        if not candidates:
            break

        cand_counts = get_support_counts(transactions, candidates)
        Lk = [c for c, cnt in cand_counts.items() if cnt >= min_support_count]

        if not Lk:
            break

        # Lưu support
        support_counts.update({c: cand_counts[c] for c in Lk})
        frequent_by_k[k] = Lk
        current_L = Lk
        k += 1

    return support_counts, frequent_by_k, n_txn


# ============================
# SINH LUẬT ASSOCIATION
# ============================
def generate_rules(support_counts, n_txn, min_conf, max_rules=MAX_RULES):
    """
    Từ support_counts (các itemset phổ biến), sinh luật:
        A -> B
    Với:
        - confidence >= min_conf
        - lift = conf / support(B)

    Trả về list[dict]:
        {
            "antecedent": frozenset,
            "consequent": frozenset,
            "support": float,
            "confidence": float,
            "lift": float
        }
    """
    rules = []

    # tiện lookup support
    def support(itemset):
        return support_counts.get(itemset, 0) / n_txn

    for itemset, sup_cnt in support_counts.items():
        if len(itemset) < 2:
            continue  # không thể tạo luật từ tập 1 phần tử

        sup_itemset = sup_cnt / n_txn
        items = list(itemset)

        # mọi non-empty proper subset làm antecedent
        for r in range(1, len(items)):
            for antecedent_tuple in combinations(items, r):
                antecedent = frozenset(antecedent_tuple)
                consequent = itemset - antecedent
                if not consequent:
                    continue

                sup_ante = support(antecedent)
                sup_cons = support(consequent)
                if sup_ante == 0 or sup_cons == 0:
                    continue

                conf = sup_itemset / sup_ante
                if conf < min_conf:
                    continue

                lift = conf / sup_cons

                rules.append({
                    "antecedent": antecedent,
                    "consequent": consequent,
                    "support": sup_itemset,
                    "confidence": conf,
                    "lift": lift
                })

    # sắp xếp: ưu tiên confidence, rồi lift, rồi support, rồi độ dài antecedent
    rules_sorted = sorted(
        rules,
        key=lambda r: (r["confidence"], r["lift"], r["support"], len(r["antecedent"])),
        reverse=True
    )

    # giới hạn MAX_RULES
    return rules_sorted[:max_rules]


# ============================
# GHI KẾT QUẢ KIỂU WEKA
# ============================
def write_rules_like_weka(rules, output_path):
    """
    Ghi file txt giống dạng Weka:
      1. A=t B=t ==> C=t   <conf:(0.98)> lift:(1.03)
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=== Python Apriori (CSV) ===\n\n")
        f.write(f"Number of rules: {len(rules)}\n\n")

        for idx, r in enumerate(rules, start=1):
            antecedent_str = " ".join(f"{item}=t" for item in sorted(r["antecedent"]))
            consequent_str = " ".join(f"{item}=t" for item in sorted(r["consequent"]))

            conf = r["confidence"]
            lift = r["lift"]

            line = (
                f"{idx}. {antecedent_str} ==> {consequent_str}    "
                f"<conf:({conf:.2f})> lift:({lift:.2f})\n"
            )
            f.write(line)


# ============================
# MAIN
# ============================
def main():
    if len(sys.argv) < 3:
        print("Cách dùng:")
        print("  python apriori_from_csv.py <input_csv> <output_txt>")
        print("Ví dụ:")
        print("  python apriori_from_csv.py olist_recommender_transactions_mix.csv test1_python.txt")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_txt = sys.argv[2]

    print("=== APRIORI TỪ CSV (KHÔNG DÙNG WEKA) ===")
    print(f">>> Input CSV : {input_csv}")
    print(f">>> Output TXT: {output_txt}")
    print(f">>> Min support    (M): {MIN_SUPPORT}")
    print(f">>> Min confidence (C): {MIN_CONFIDENCE}")
    print(f">>> Max rules      (N): {MAX_RULES}")

    # 1) Load transactions
    transactions, items = load_transactions_from_csv(input_csv)
    print(f">>> Số transaction: {len(transactions)}")
    print(f">>> Số item       : {len(items)}")

    # 2) Chạy Apriori
    support_counts, frequent_by_k, n_txn = apriori(
        transactions,
        min_support_ratio=MIN_SUPPORT,
        max_itemset_size=MAX_ITEMSET_SIZE
    )

    total_freq = sum(len(v) for v in frequent_by_k.values())
    print(f">>> Tổng số itemset phổ biến: {total_freq}")
    for k, lst in frequent_by_k.items():
        print(f"    L({k}) = {len(lst)} itemset")

    # 3) Sinh luật
    rules = generate_rules(
        support_counts,
        n_txn=n_txn,
        min_conf=MIN_CONFIDENCE,
        max_rules=MAX_RULES
    )
    print(f">>> Số luật sinh ra: {len(rules)}")

    # 4) Ghi ra file txt
    write_rules_like_weka(rules, output_txt)
    print(f">>> Đã ghi xong file: {output_txt}")


if __name__ == "__main__":
    main()
