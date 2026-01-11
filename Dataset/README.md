# Hệ Thống Khuyến Nghị Sản Phẩm - Apriori Algorithm

Hệ thống khuyến nghị sản phẩm sử dụng thuật toán Apriori để phát hiện các luật kết hợp (association rules) từ dữ liệu giao dịch.

---

## 🎯 Tổng Quan

Hệ thống này thực hiện các bước sau:

1. **Tạo dữ liệu mẫu**: Sinh dữ liệu khách hàng và đơn hàng Việt Nam
2. **Chuẩn bị dữ liệu**: Chuyển đổi dữ liệu thành định dạng transaction cho Apriori
3. **Chạy Apriori**: Tìm các itemset phổ biến và sinh luật kết hợp
4. **Xử lý luật**: Lọc, chọn lọc và chuyển đổi format luật
5. **Xuất kết quả**: Tạo file JSON cho ứng dụng web

---

## 📁 Cấu Trúc Dự Án

```
Test4/
├── py/                                    # Thư mục chứa các script Python
│   ├── generate_customers_vn.py          # Tạo dữ liệu khách hàng
│   ├── data_mix.py                       # Tạo dữ liệu đơn hàng
│   ├── train_apriori.py                  # Chuẩn bị dữ liệu cho Apriori
│   ├── txt_to_json.py                    # Parse kết quả từ Weka/Python Apriori
│   ├── select_top_53_rules.py            # Chọn 53 luật tốt nhất
│   ├── json_id.py                        # Chuyển đổi ID sản phẩm
│   ├── filter_best_rules_for_products.py # Lọc luật cho sản phẩm cụ thể
│   └── extract_rules_to_json.py          # Trích xuất luật (phiên bản cũ)
├── apriori_from_csv.py                   # Triển khai Apriori bằng Python
├── txt/                                   # Thư mục chứa file TXT kết quả
│   ├── test.txt                          # Kết quả từ Weka
│   └── test1.txt                         # Kết quả từ Python Apriori
├── *.csv                                 # Các file dữ liệu CSV
├── *.json                                # Các file JSON kết quả
└── README.md                             # File này
```

---

## 🔧 Yêu Cầu Hệ Thống

### Python Packages

```bash
pip install pandas numpy
```

### File Dữ Liệu Cần Có

- `olist_products_dataset_vn.csv` - Danh sách sản phẩm (53 sản phẩm)
- `olist_order_items_dataset_vn_new.csv` - Chi tiết đơn hàng (36000 dòng)
- `olist_orders_dataset_vn_new.csv ` - Danh sách đơn hàng (12000 đơn)
- `olist_customers_dataset_vn_new.csv` - Danh sách khách hàng (5000 khách)
- (Tùy chọn) Các file CSV khác nếu bạn muốn dùng dữ liệu có sẵn

---

## 🔄 Pipeline Xử Lý

```
┌─────────────────────────────────────────────────────────────────┐
│                    BƯỚC 1: TẠO DỮ LIỆU MẪU                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │ 01_category_translation.py                │
        │ → product_category_name_translation_vn.csv│
        │ 02_geolocation.py                         │
        │ → olist_geolocation_dataset_vn.csv        │
        │ 03_sellers.py                             │
        │ → olist_sellers_dataset_vn.csv            │
        │ 04_customers.py                           │
        │ → olist_customers_dataset_vn_new.csv      │
        │ 05_products.py                            │
        │ → olist_products_dataset_vn.csv           │
        │ 06_orders.py                              │
        │ → olist_orders_dataset_vn_new.csv         │
        │ 07_order_items.py                         │
        │ → olist_order_items_dataset_vn_new.csv    │
        │ 08_payments.py                            │
        │ → olist_order_payments_dataset_vn.csv     │
        │ 09_reviews.py                             │
        │ → olist_order_reviews_dataset_vn.csv      │
        └───────────────────────────────────────────┘
                              │
                              ▼

┌─────────────────────────────────────────────────────────────────┐
│              BƯỚC 2: CHUẨN BỊ DỮ LIỆU CHO APRIORI               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │ train_apriori.py                    │
        │ → olist_recommender_transactions_   │
        │   mix.csv                           │
        │ → olist_recommender_transactions_   │
        │   mix.arff (cho Weka)               │
        │ → product_lookup.json               │
        └─────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              BƯỚC 3: CHẠY THUẬT TOÁN APRIORI                   │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌──────────────────┐                    ┌──────────────────┐
│  CÁCH 1: WEKA    │                    │  CÁCH 2: PYTHON  │
│                  │                    │                  │
│  (Thủ công)      │                    │ apriori_from_csv │
│  - Mở ARFF file  │                    │ .py              │
│  - Chạy Apriori  │                    │                  │
│  - Export TXT    │                    │ → test1_python   │
│                  │                    │   .txt           │
└──────────────────┘                    └──────────────────┘
        │                                           │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              BƯỚC 4: XỬ LÝ VÀ CHUYỂN ĐỔI LUẬT                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │ txt_to_json.py                      │
        │ → rules2.json (tất cả luật)         │
        └─────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │ select_top_53_rules.py              │
        │ → rules_top_53.json (53 luật tốt)   │
        └─────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │ json_id.py                          │
        │ → rules_top_53_short_id.json        │
        │   (cho web app)                     │
        └─────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │ filter_best_rules_for_products.py  │
        │ (Tùy chọn - nếu cần bổ sung)       │
        │ → missing_rules.json                │
        └─────────────────────────────────────┘
```

---

## 🚀 Hướng Dẫn Chạy Từng File

### **BƯỚC 1: Tạo Dữ Liệu Mẫu**

**File (9 file tạo dữ liệu):**

- `01_category_translation.py`
- `02_geolocation.py`
- `03_sellers.py`
- `04_customers.py`
- `05_products.py`
- `06_orders.py`
- `07_order_items.py`
- `08_payments.py`
- `09_reviews.py`

**Mô tả (tạo dữ liệu gì, như thế nào):**  
Bước này sinh **9 bảng CSV dữ liệu e-commerce** theo mô hình Olist (giả lập), :

- Sinh dữ liệu **synthetic** bằng random có kiểm soát (`seed`) để chạy lại ra dữ liệu giống nhau.
- Tạo bảng “cha” trước, rồi tạo bảng “con” dựa trên khóa tham chiếu:
  - `sellers` lấy zip/city/state từ `geolocation`
  - `orders` lấy `customer_id` từ `customers`
  - `order_items` tham chiếu `orders + products + sellers`
  - `payments` và `reviews` tham chiếu `orders` (chỉ subset 6500 order đầu để khớp bộ mẫu)
- Timestamp trong `orders` được sinh theo chuỗi thời gian hợp lý: purchase → approved → carrier → delivered → estimated.

**Mô tả (các file CSV được tạo và ý nghĩa):**

- `product_category_name_translation_vn.csv` — Bảng **dịch danh mục sản phẩm** (mapping `product_category_name` ↔ tên hiển thị), dùng để join với bảng products.
- `olist_geolocation_dataset_vn.csv` — Bảng **vị trí địa lý** gồm `zip_code_prefix`, `lat/lng`, `city`, `state` để gán khu vực cho sellers.
- `olist_sellers_dataset_vn.csv` — Bảng **người bán** gồm `seller_id`, `seller_zip_code_prefix`, `seller_city`, `seller_state` (zip/city/state lấy từ geolocation).
- `olist_customers_dataset_vn_new.csv` — Bảng **khách hàng** (5000 dòng) gồm `customer_id`, `customer_unique_id`, `zip_code_prefix`, `city`, `state`.
- `olist_products_dataset_vn.csv` — Bảng **sản phẩm** (53 sản phẩm) gồm `product_id`, `category`, `brand`, `name`, và các thuộc tính kích thước/khối lượng.
- `olist_orders_dataset_vn_new.csv` — Bảng **đơn hàng** (12000 đơn) gồm `order_id`, `customer_id`, trạng thái và các mốc thời gian (purchase/approved/carrier/delivered/estimated).
- `olist_order_items_dataset_vn_new.csv` — Bảng **chi tiết đơn hàng** (36000 dòng) liên kết `order_id` + `product_id` + `seller_id`, kèm `shipping_limit_date`, `price`, `freight_value`.
- `olist_order_payments_dataset_vn.csv` — Bảng **thanh toán** (6500 dòng) cho `ORD_00001 → ORD_06500`, gồm `payment_type`, `installments`, `payment_value`.
- `olist_order_reviews_dataset_vn.csv` — Bảng **đánh giá** (6500 dòng) cho `ORD_00001 → ORD_06500`, gồm `review_score`, nội dung, thời gian tạo và phản hồi.

**Câu lệnh :**

````bash
# chạy tại thư mục DATASET
python 01_category_translation.py --all --out_dir . --seed 42 --force

---

### **BƯỚC 2: Chuẩn Bị Dữ Liệu Cho Apriori**

**File:** `train_apriori.py`

**Mô tả:** Chuyển đổi dữ liệu đơn hàng thành định dạng transaction (ma trận nhị phân) cho thuật toán Apriori.

**Câu lệnh:**

```bash
python train_apriori.py
````

**Yêu cầu:**

- `olist_customers_dataset_vn_new.csv`
- `olist_orders_dataset_vn_new.csv`
- `olist_order_items_dataset_vn_new.csv`
- `olist_products_dataset_vn.csv`

**Output:**

- `olist_recommender_transactions_mix.csv` - File CSV transaction
- `olist_recommender_transactions_mix.arff` - File ARFF cho Weka
- `product_lookup.json` - Lookup thông tin sản phẩm

**Giải thích:**

- Tạo transaction theo đơn hàng (ORD) và theo khách hàng (CUS)
- Chỉ giữ transaction có ≥2 sản phẩm
- Giá trị: `t` = có mua, `?` = không mua (missing)

---

### **BƯỚC 4A: Chạy Apriori Bằng Python (Khuyến nghị)**

**File:** `apriori_from_csv.py`

**Mô tả:** Triển khai thuật toán Apriori bằng Python, không cần Weka.

**Câu lệnh:**

```bash
python apriori_from_csv.py olist_recommender_transactions_mix.csv test1_python.txt
```

**Tham số:**

- `olist_recommender_transactions_mix.csv` - File CSV transaction (input)
- `test1_python.txt` - File TXT kết quả (output)

**Cấu hình trong file:**

```python
MIN_SUPPORT = 0.01      # Tối thiểu 1% giao dịch
MIN_CONFIDENCE = 0.55   # Độ tin cậy tối thiểu 55%
MAX_RULES = 1200        # Tối đa 1200 luật
MAX_ITEMSET_SIZE = 5    # Itemset tối đa 5 phần tử
```

**Output:**

- `test1_python.txt` - File TXT chứa các luật (format giống Weka)

**Ví dụ output:**

```
1. PRD_00001=t PRD_00002=t ==> PRD_00003=t    <conf:(0.85)> lift:(1.23)
2. PRD_00005=t ==> PRD_00010=t                <conf:(0.72)> lift:(2.15)
```

---

### **BƯỚC 4B: Chạy Apriori Bằng Weka (Tùy chọn)**

**Nếu bạn muốn dùng Weka:**

1. Mở Weka Explorer
2. Load file `olist_recommender_transactions_mix.arff`
3. Chọn tab "Associate"
4. Chọn "Apriori"
5. Cấu hình:
   - `-N 1200` (max rules)
   - `-T 0` (class index)
   - `-C 0.55` (min confidence)
   - `-D 0.005` (delta)
   - `-U 0.9` (upper bound)
   - `-M 0.01` (min support)
6. Click "Start"
7. Right-click kết quả → "Save result buffer" → Lưu thành `txt/test1.txt`

---

### **BƯỚC 5: Parse Kết Quả Sang JSON**

**File:** `py/txt_to_json.py`

**Mô tả:** Chuyển đổi file TXT kết quả từ Apriori sang định dạng JSON.

**Câu lệnh:**

```bash
cd py
python txt_to_json.py
```

**Cấu hình trong file:**

```python
INPUT_TXT = "test1.txt"        # File TXT từ Weka/Python
OUTPUT_JSON = "rules2.json"    # File JSON output
```

**Lưu ý:** Nếu bạn dùng Python Apriori, cần sửa `INPUT_TXT = "../test1_python.txt"` hoặc copy file vào thư mục `py/`.

**Output:**

- `rules2.json` - File JSON chứa tất cả các luật

**Format JSON:**

```json
[
  {
    "antecedent": ["PRD_00001", "PRD_00002"],
    "consequent": ["PRD_00003"],
    "confidence": 0.85,
    "lift": 1.23
  },
  ...
]
```

---

### **BƯỚC 6: Chọn 53 Luật Tốt Nhất**

**File:** `py/select_top_53_rules.py`

**Mô tả:** Chọn 1 luật tốt nhất cho mỗi sản phẩm (PRD_00001 → PRD_00053).

**Câu lệnh:**

```bash
cd py
python select_top_53_rules.py
```

**Yêu cầu:**

- `rules2.json` (từ bước 5)

**Cấu hình trong file:**

```python
RULES_JSON = "rules2.json"
OUT_JSON = "rules_top_53.json"
```

**Logic:**

- Với mỗi sản phẩm, ưu tiên luật có sản phẩm ở **consequent**
- Nếu không có, tạo **synthetic rule** từ luật có sản phẩm ở **antecedent**
- Điểm số: confidence > lift > độ dài antecedent

**Output:**

- `rules_top_53.json` - 53 luật tốt nhất (1 luật/sản phẩm)

---

### **BƯỚC 7: Chuyển Đổi ID Sản Phẩm**

**File:** `py/json_id.py`

**Mô tả:** Rút gọn ID sản phẩm từ `PRD_00008` → `08` (cho web app).

**Câu lệnh:**

```bash
cd py
python json_id.py
```

**Yêu cầu:**

- `rules_top_53.json` (từ bước 6)

**Cấu hình trong file:**

```python
INPUT_JSON = "rules_top_53.json"
OUTPUT_JSON = "rules_top_53_short_id.json"
```

**Output:**

- `rules_top_53_short_id.json` - File JSON với ID ngắn gọn

**Ví dụ chuyển đổi:**

```json
// Trước
{
  "antecedent": ["PRD_00001", "PRD_00008"],
  "consequent": ["PRD_00012"]
}

// Sau
{
  "antecedent": ["01", "08"],
  "consequent": ["12"]
}
```

---

### **BƯỚC 8: Lọc Luật Cho Sản Phẩm Cụ Thể (Tùy chọn)**

**File:** `py/filter_best_rules_for_products.py`

**Mô tả:** Tìm luật tốt nhất cho danh sách sản phẩm cụ thể (thường dùng để bổ sung luật còn thiếu).

**Câu lệnh:**

```bash
cd py
python filter_best_rules_for_products.py
```

**Yêu cầu:**

- `rules2.json` (từ bước 5)

**Cấu hình trong file:**

```python
RULES_JSON = "rules2.json"
OUT_JSON = "missing_rules.json"
TARGET_PRODUCTS = ["PRD_00003", "PRD_00007"]  # Danh sách sản phẩm cần tìm
```

**Output:**

- `missing_rules.json` - Các luật tốt nhất cho sản phẩm mục tiêu

---

## 📊 Giải Thích Input/Output

### **Input Files**

| File                                     | Mô tả                 | Format                                                                      |
| ---------------------------------------- | --------------------- | --------------------------------------------------------------------------- |
| `olist_products_dataset_vn.csv`          | Danh sách 53 sản phẩm | CSV với cột: product_id, product_name, product_category_name                |
| `olist_customers_dataset_vn_new.csv`     | Dữ liệu khách hàng    | CSV với cột: customer_id, customer_unique_id, customer_city, customer_state |
| `olist_orders_dataset_vn_new.csv`        | Dữ liệu đơn hàng      | CSV với cột: order_id, customer_id, order_status, timestamps                |
| `olist_order_items_dataset_vn_new.csv`   | Chi tiết đơn hàng     | CSV với cột: order_id, product_id, seller_id, price, freight_value          |
| `olist_recommender_transactions_mix.csv` | Transaction matrix    | CSV với cột: transaction_id, PRD_00001, PRD_00002, ... (giá trị: t hoặc ?)  |
| `test1.txt` hoặc `test1_python.txt`      | Kết quả Apriori       | TXT với format: `1. A=t B=t ==> C=t <conf:(0.85)> lift:(1.23)`              |

### **Output Files**

| File                         | Mô tả                            | Format                                             |
| ---------------------------- | -------------------------------- | -------------------------------------------------- |
| `rules2.json`                | Tất cả các luật từ Apriori       | JSON array of rules                                |
| `rules_top_53.json`          | 53 luật tốt nhất (1/sản phẩm)    | JSON array với ID đầy đủ                           |
| `rules_top_53_short_id.json` | 53 luật với ID ngắn gọn          | JSON array với ID rút gọn (cho web)                |
| `missing_rules.json`         | Luật bổ sung cho sản phẩm cụ thể | JSON array                                         |
| `product_lookup.json`        | Lookup thông tin sản phẩm        | JSON object: {product_id: {name, category, brand}} |

---

## 🔍 Các Tham Số Quan Trọng

### **Apriori Parameters**

| Tham số            | Giá trị | Ý nghĩa                             |
| ------------------ | ------- | ----------------------------------- |
| `MIN_SUPPORT`      | 0.01    | Tối thiểu 1% giao dịch chứa itemset |
| `MIN_CONFIDENCE`   | 0.55    | Độ tin cậy tối thiểu 55%            |
| `MAX_RULES`        | 1200    | Tối đa 1200 luật được sinh ra       |
| `MAX_ITEMSET_SIZE` | 5       | Itemset tối đa 5 phần tử            |

### **Data Generation Parameters**

| Tham số               | Giá trị | Ý nghĩa                         |
| --------------------- | ------- | ------------------------------- |
| `NUM_CUSTOMERS`       | 5000    | Số khách hàng                   |
| `NUM_ORDERS`          | 12000   | Số đơn hàng                     |
| `MIN_ITEMS_PER_ORDER` | 2       | Tối thiểu 2 sản phẩm/đơn        |
| `MAX_ITEMS_PER_ORDER` | 4       | Tối đa 4 sản phẩm/đơn           |
| `CROSS_CATEGORY_PROB` | 0.10    | 10% khả năng mua cross-category |

---

## ⚠️ Lưu Ý Quan Trọng

1. **Thứ tự chạy:** Phải chạy theo đúng thứ tự pipeline (Bước 1 → 2 → 3 → 4 → 5 → 6 → 7)

2. **Đường dẫn file:**

   - Các file trong thư mục `py/` tham chiếu file ở thư mục gốc
   - Nếu chạy từ thư mục gốc, cần sửa đường dẫn trong code

3. **File paths trong code:**

   - Nếu chạy từ thư mục `py/`, các file CSV phải ở thư mục `../`
   - Nếu chạy từ thư mục gốc, các file CSV ở cùng thư mục

4. **Encoding:** Tất cả file đều dùng UTF-8 encoding

5. **Python version:** Khuyến nghị Python 3.7+

---

## 🐛 Troubleshooting

### **Lỗi: File not found**

- Kiểm tra đường dẫn file trong code
- Đảm bảo đã chạy các bước trước đó

### **Lỗi: No rules generated**

- Giảm `MIN_SUPPORT` hoặc `MIN_CONFIDENCE`
- Kiểm tra dữ liệu transaction có đủ không

### **Lỗi: Memory error**

- Giảm `MAX_ITEMSET_SIZE` xuống 4 hoặc 3
- Giảm số lượng transaction

---

## 📝 Ví Dụ Chạy Đầy Đủ

```bash
# Bước 1: Tạo khách hàng
cd py
python generate_customers_vn.py

# Bước 2: Tạo đơn hàng
python data_mix.py

# Bước 3: Chuẩn bị transaction
python train_apriori.py

# Bước 4: Chạy Apriori (từ thư mục gốc)
cd ..
python apriori_from_csv.py olist_recommender_transactions_mix.csv test1_python.txt

# Bước 5: Parse sang JSON
cd py
# Sửa INPUT_TXT trong txt_to_json.py thành "../test1_python.txt"
python txt_to_json.py

# Bước 6: Chọn 53 luật tốt nhất
python select_top_53_rules.py

# Bước 7: Chuyển đổi ID
python json_id.py

# Kết quả cuối cùng: rules_top_53_short_id.json
```

---

## 📚 Tài Liệu Tham Khảo

- **Apriori Algorithm:** Thuật toán khai phá luật kết hợp
- **Association Rules:** Confidence, Support, Lift
- **Weka:** Công cụ khai phá dữ liệu (nếu dùng)

---

**Chúc bạn thành công! 🎉**
