import json

# ====== CẤU HÌNH ======
RULES_JSON = "rules2.json"      # file JSON chứa toàn bộ luật từ Weka
OUT_JSON   = "missing_rules.json"  # sẽ lưu các luật tốt nhất cho các sản phẩm cần tìm

# Danh sách product cần tìm luật
TARGET_PRODUCTS = ["PRD_00003", "PRD_00007"]


def load_rules(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pick_best_rules_for_targets(rules, target_products):
    """
    Với mỗi product trong target_products, chọn 1 rule có consequent chứa product đó,
    ưu tiên rule có confidence cao nhất, nếu bằng nhau thì lift cao hơn.
    """
    best_rules = {p: None for p in target_products}

    for rule in rules:
        cons = rule.get("consequent", [])
        conf = float(rule.get("confidence", 0))
        lift = float(rule.get("lift", 0))

        # mỗi rule hiện tại chỉ có 1 consequent, nhưng vẫn xử lý list cho chắc
        for pid in cons:
            if pid in best_rules:
                current_best = best_rules[pid]
                if current_best is None:
                    best_rules[pid] = rule
                else:
                    c_conf = float(current_best.get("confidence", 0))
                    c_lift = float(current_best.get("lift", 0))

                    # Ưu tiên conf cao hơn, nếu bằng nhau thì lift cao hơn
                    if (conf > c_conf) or (conf == c_conf and lift > c_lift):
                        best_rules[pid] = rule

    # Loại bỏ những product không tìm được rule
    result = [r for r in best_rules.values() if r is not None]
    return result


def main():
    print(">>> Đọc toàn bộ luật từ:", RULES_JSON)
    rules = load_rules(RULES_JSON)
    print("Tổng số luật:", len(rules))

    best_for_targets = pick_best_rules_for_targets(rules, TARGET_PRODUCTS)

    print("\n>>> Các luật tốt nhất cho từng product mục tiêu:")
    for r in best_for_targets:
        cons = r["consequent"][0]
        print(f"- Consequent = {cons}, conf = {r['confidence']}, lift = {r['lift']}")
        print(f"  Antecedent: {', '.join(r['antecedent'])}")

    # Lưu ra file để tiện ghép với 53 luật hiện tại
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(best_for_targets, f, indent=4, ensure_ascii=False)

    print("\n>>> Đã lưu các luật còn thiếu vào:", OUT_JSON)


if __name__ == "__main__":
    main()
