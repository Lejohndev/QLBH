import re
import json

INPUT_TXT = "test1.txt"        # file TXT export từ Weka
OUTPUT_JSON = "rules2.json"    # output JSON

# Regex mới mạnh hơn – hỗ trợ mọi rule Weka tạo ra
rule_pattern = re.compile(
    r"^\s*\d+\.\s*(.*?)\s*==>\s*(.*?)\s*<conf:\((.*?)\)>\s*lift:\((.*?)\)",
    re.IGNORECASE
)

def extract_items(raw):
    """
    Tách item dạng:
       'PRD_00010=t PRD_00012=f PRD_00013=t'
    → chỉ giữ các item có giá trị 't'
    """
    items = []
    raw = raw.strip()

    # tách theo dấu cách
    for token in raw.split():
        token = token.strip()
        if "=" in token:
            pid, val = token.split("=")
            if val.lower() == "t":
                items.append(pid)
    return items

rules = []
with open(INPUT_TXT, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        m = rule_pattern.match(line)
        if not m:
            continue

        ante_raw = m.group(1)
        cons_raw = m.group(2)
        conf = float(m.group(3))
        lift = float(m.group(4))

        ante = extract_items(ante_raw)
        cons = extract_items(cons_raw)

        if not ante or not cons:
            continue

        rules.append({
            "antecedent": ante,
            "consequent": cons,
            "confidence": conf,
            "lift": lift
        })

# Ghi JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(rules, f, indent=4, ensure_ascii=False)

print("✔ DONE!")
print("✔ File JSON tạo:", OUTPUT_JSON)
print("✔ Tổng rule hợp lệ:", len(rules))
