# clear_9_csv.py
# Xóa sạch dữ liệu của 9 file CSV (giữ header nếu có), có backup trước khi xóa.

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import shutil

# ====== CẤU HÌNH ======
# Đổi danh sách này đúng tên 9 file CSV của bạn
CSV_FILES = [
    "olist_customers_dataset_vn_new.csv",
    "olist_geolocation_dataset_vn.csv",
    "olist_order_items_dataset_vn_new.csv",
    "olist_order_payments_dataset_vn.csv",
    "olist_order_reviews_dataset_vn.csv",
    "olist_orders_dataset_vn_new.csv",
    "olist_products_dataset_vn.csv",
    "olist_sellers_dataset_vn.csv",
    "product_category_name_translation_vn.csv",
]

# Nếu CSV nằm trong thư mục khác, sửa BASE_DIR
BASE_DIR = Path(__file__).resolve().parent

# True: giữ lại dòng header (dòng đầu tiên) nếu file có nội dung
# False: xóa sạch cả header (file rỗng hoàn toàn)
KEEP_HEADER = True

# True: tạo bản sao lưu trước khi xóa
MAKE_BACKUP = True
# ======================


def clear_csv_file(path: Path, keep_header: bool, make_backup: bool) -> None:
    if not path.exists():
        print(f"[SKIP] Not found: {path}")
        return

    if make_backup:
        backup_dir = path.parent / "_backup_before_clear"
        backup_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{path.stem}__{ts}{path.suffix}"
        shutil.copy2(path, backup_path)
        print(f"[BACKUP] {path.name} -> {backup_path}")

    # Đọc dòng đầu (header) nếu cần
    header = ""
    if keep_header:
        try:
            with path.open("r", encoding="utf-8", newline="") as f:
                header = f.readline()
        except UnicodeDecodeError:
            # fallback nếu file dùng encoding khác
            with path.open("r", encoding="utf-8-sig", newline="") as f:
                header = f.readline()

    # Ghi lại file: chỉ header hoặc rỗng
    with path.open("w", encoding="utf-8", newline="") as f:
        if keep_header and header:
            f.write(header)

    print(f"[CLEARED] {path} (keep_header={keep_header and bool(header)})")


def main() -> None:
    for name in CSV_FILES:
        p = (BASE_DIR / name).resolve()
        clear_csv_file(p, KEEP_HEADER, MAKE_BACKUP)

    print("\nDone.")


if __name__ == "__main__":
    main()
