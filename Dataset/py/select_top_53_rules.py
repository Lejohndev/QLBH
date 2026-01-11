import json
import re

RULES_JSON = "rules2.json"          # file JSON chứa TẤT CẢ luật từ Apriori
OUT_JSON   = "rules_top_53.json"    # file JSON output chuẩn cho web


def extract_pid_number(pid: str) -> int:
    """Lấy số từ PRD_00029 -> 29 để sort."""
    m = re.search(r"PRD_(\d+)", pid)
    return int(m.group(1)) if m else 9999


def load_rules(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("File JSON luật phải là list các object.")
    return data


def rule_score(rule: dict):
    """
    Hàm tính điểm cho 1 luật:
    - Ưu tiên confidence cao hơn
    - Sau đó ưu tiên lift cao hơn
    - Sau đó ưu tiên antecedent dài hơn (nhiều điều kiện hơn)
    """
    conf = rule.get("confidence", 0.0)
    lift = rule.get("lift", 1.0)
    antecedent = rule.get("antecedent", [])
    return (conf, lift, len(antecedent))


def build_best_rule_per_product(all_rules, product_ids):
    """
    Với mỗi product_id:
      1) Nếu có luật mà product_id nằm ở consequent:
           -> Lấy luật có score mạnh nhất.
      2) Nếu KHÔNG có consequent:
           -> Tìm luật mà product_id nằm ở antecedent.
              Từ luật mạnh nhất đó, tạo 1 luật synthetic:
                 antecedent_new = (antecedent cũ bỏ product_id) + consequent cũ
                 consequent_new = [product_id]
                 confidence/lift giữ nguyên
    """
    # Index nhanh
    rules_by_conseq = {}
    rules_by_ante   = {}

    for r in all_rules:
        conseq = r.get("consequent", [])
        ants   = r.get("antecedent", [])

        if conseq:
            pid_c = conseq[0]
            rules_by_conseq.setdefault(pid_c, []).append(r)

        for a in ants:
            rules_by_ante.setdefault(a, []).append(r)

    selected_rules = []

    for pid in product_ids:
        best_rule = None
        mode = None   # "consequent" hoặc "synthetic"

        # 1) Ưu tiên rule mà pid nằm ở consequent
        cand_conseq = rules_by_conseq.get(pid, [])
        if cand_conseq:
            best_rule = max(cand_conseq, key=rule_score)
            mode = "consequent"
        else:
            # 2) Không có consequent -> fallback dùng antecedent
            cand_ante = rules_by_ante.get(pid, [])
            if cand_ante:
                source_rule = max(cand_ante, key=rule_score)

                src_ants = source_rule.get("antecedent", [])
                src_conseq = source_rule.get("consequent", [])

                # antecedent mới: bỏ chính pid khỏi antecedent,
                # rồi cộng các item trong consequent cũ
                new_ante = [x for x in src_ants if x != pid]
                for c in src_conseq:
                    if c not in new_ante and c != pid:
                        new_ante.append(c)

                if not new_ante:
                    # Nếu lỡ trống (trường hợp hiếm), bỏ qua
                    print(f"[CẢNH BÁO] Không thể tạo antecedent mới cho {pid}")
                    continue

                best_rule = {
                    "antecedent": new_ante,
                    "consequent": [pid],
                    "confidence": source_rule.get("confidence", 0.0),
                    "lift": source_rule.get("lift", 1.0),
                    "synthetic": True   # đánh dấu là luật tạo thêm
                }
                mode = "synthetic"
            else:
                print(f"[CẢNH BÁO] Không tìm được luật (consequent/antecedent) cho {pid}")
                continue

        # Log cho dễ kiểm tra
        conseq_pid = best_rule["consequent"][0]
        ants_str = ", ".join(best_rule["antecedent"])
        print(f">> Rule cho {pid} (mode={mode}): "
              f"[{ants_str}] => {conseq_pid} "
              f"(conf={best_rule['confidence']:.2f}, lift={best_rule['lift']:.2f})")

        selected_rules.append(best_rule)

    return selected_rules


def sort_rules_by_pid(rules):
    return sorted(rules, key=lambda r: extract_pid_number(r["consequent"][0]))


def main():
    print("=== BUILD 1 RULE / PRODUCT (ƯU TIÊN CONSEQUENT, Fallback ANTECEDENT + SYNTHETIC) ===")

    rules = load_rules(RULES_JSON)
    print(f">>> Tổng số luật đọc được: {len(rules)}")

    # PRD_00001..PRD_00053
    product_ids = [f"PRD_{i:05d}" for i in range(1, 54)]

    best_rules = build_best_rule_per_product(rules, product_ids)
    print(f">>> Số luật chọn được: {len(best_rules)}")

    best_rules_sorted = sort_rules_by_pid(best_rules)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(best_rules_sorted, f, ensure_ascii=False, indent=4)

    print(f">>> ĐÃ LƯU: {OUT_JSON}")

    print("\n>>> Một vài luật đầu sau khi sắp xếp:")
    for i, r in enumerate(best_rules_sorted[:10], start=1):
        print(f"{i}. {r['antecedent']} => {r['consequent'][0]} "
              f"(conf={r['confidence']:.2f}, lift={r['lift']:.2f})")


if __name__ == "__main__":
    main()
