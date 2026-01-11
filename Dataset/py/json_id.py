import json
import re

# ==========================
# Cấu hình file
# ==========================
INPUT_JSON  = "rules_top_53.json"          # file json gốc (đang dùng PRD_000xx)
OUTPUT_JSON = "rules_top_53_short_id.json" # file json sau khi chuyển id (08, 12,...)


def convert_pid(pid: str) -> str:
    """
    Chuyển 'PRD_00008' -> '08'
    Chuyển 'PRD_0003'  -> '03'
    Chuyển 'PRD_00053' -> '53'
    """
    m = re.search(r"PRD_0*(\d+)", pid)
    if not m:
        # Nếu không đúng pattern, trả nguyên chuỗi cũ
        return pid
    num = int(m.group(1))
    # format 2 chữ số: 01..53
    return f"{num:02d}"


def main():
    # 1) Load JSON gốc
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        rules = json.load(f)

    if not isinstance(rules, list):
        raise ValueError("File JSON phải là 1 list các rule.")

    new_rules = []

    # 2) Duyệt từng rule và convert id
    for r in rules:
        ante = r.get("antecedent", [])
        conseq = r.get("consequent", [])

        new_ante = [convert_pid(pid) for pid in ante]
        new_conseq = [convert_pid(pid) for pid in conseq]

        new_rule = dict(r)  # copy
        new_rule["antecedent"] = new_ante
        new_rule["consequent"] = new_conseq

        new_rules.append(new_rule)

    # 3) Ghi ra file mới
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(new_rules, f, ensure_ascii=False, indent=4)

    print(f"✔ Đã chuyển đổi ID và lưu vào: {OUTPUT_JSON}")
    print(f"✔ Tổng số rule: {len(new_rules)}")


if __name__ == "__main__":
    main()
