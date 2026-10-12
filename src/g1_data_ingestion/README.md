# 🕸 Group 1: Data Ingestion, Cleaning & Deduplication (Tầng Bronze $\rightarrow$ Silver)

Nhiệm vụ cốt lõi: **Thu thập dữ liệu tuyển dụng thô $\rightarrow$ Dọn dẹp/Chuẩn hóa $\rightarrow$ Xóa trùng lặp $\rightarrow$ Đẩy vào kho chuẩn.**

## 🗺️ 1. Luồng dữ liệu (Data Workflow)

1. **Crawler (`crawlers/`)**: Cào dữ liệu từ Web (TopCV, ITviec, VietnamWorks...) $\rightarrow$ Lưu nguyên si vào Collection `jobs_bronze` trên **MongoDB** (Bronze Layer).
2. **Cleaner (`cleaners/`)**: Đọc dữ liệu thô từ **MongoDB**, xử lý chuỗi, ép kiểu số $\rightarrow$ Validate bằng **Pydantic** $\rightarrow$ Lưu vào bảng `jobs_clean` trên **PostgreSQL** (Silver Layer).
3. **Deduplicator (`deduplication/`)**: Quét bảng `jobs_clean` (PostgreSQL) tìm các tin tuyển dụng bị trùng $\rightarrow$ Lưu lịch sử trùng vào bảng `dedup_map`.

---

## 📋 2. Đặc tả công việc chi tiết (Tasks)

### Module 1.1: Cào dữ liệu thô (Crawlers)
*   **Vị trí code:** `src/g1_data_ingestion/crawlers/`
*   **Input:** URL các trang web tuyển dụng.
*   **Output:** `INSERT` vào collection **`jobs_bronze`** (MongoDB).
*   **Quy tắc:** Cào được gì lấy nấy, không làm sạch ở bước này. Giữ nguyên HTML gốc (`raw_html`) hoặc JSON gốc (`raw_json`). MongoDB chấp nhận mọi format nên không cần lo lỗi schema.

### Module 1.2: Dọn dẹp & Chuẩn hóa (Cleaners)
*   **Vị trí code:** `src/g1_data_ingestion/cleaners/job_cleaner.py`
*   **Input:** Dữ liệu đọc từ **MongoDB**.
*   **Output:** Object `JobClean` (Pydantic) $\rightarrow$ `INSERT` vào bảng **`jobs_clean`** (PostgreSQL).
*   **Hướng dẫn xử lý:**
    1. **Text JD:** Gộp `description_raw`, `requirements_raw`, `benefits_raw` lại thành text sạch (loại bỏ toàn bộ HTML tags).
    2. **Mức lương (Salary):** Parse ra `salary_min`, `salary_max` (float) và `currency` (VD: VND, USD). Nếu JD ghi "Thương lượng" thì để null.
    3. **Kinh nghiệm (Experience):** Parse ra `experience_min`, `experience_max` (float). Nếu JD ghi "Không yêu cầu" thì min=0.0, max=0.0.
    4. **Ép chuẩn Enum:** Các trường `level` và `role_family` **bắt buộc** phải map với bộ Enum được định nghĩa trong `src/shared/schemas/enums.py`.

### Module 1.3: Xử lý trùng lặp (Deduplicator)
*   **Vị trí code:** `src/g1_data_ingestion/deduplication/dedup_engine.py`
*   **Input:** Bảng `jobs_clean` (PostgreSQL).
*   **Output:** `INSERT` vào bảng **`dedup_map`** (PostgreSQL).
*   **Quy tắc (Matching Logic):**
    *   Trùng URL (Exact match).
    *   Trùng ngữ nghĩa: `company_name` giống nhau VÀ `title` giống nhau VÀ `similarity(description1, description2) > 0.9`.
    *   Ghi lại ID canonical và ID duplicate, kèm phương pháp dedup.

---

## 🔒 3. Data Contract (Hợp đồng Dữ liệu)

Đoạn code kết nối giữa MongoDB và PostgreSQL qua cầu nối Pydantic:

```python
from src.shared.schemas import JobClean
from src.shared.db.session import SessionLocal, mongo_db

def transform_and_save():
    # 1. Đọc data thô từ MongoDB
    raw_jobs = mongo_db["jobs_bronze"].find({"is_processed": {"$ne": True}})
    
    db = SessionLocal()
    for raw_data in raw_jobs:
        try:
            # 2. Validate qua Pydantic
            clean_job = JobClean(
                job_id=raw_data["_id"], # Dùng ID của MongoDB hoặc tự gen ID mới
                source=raw_data["source"],
                url=raw_data["url"],
                title=raw_data["title_raw"], 
                company_key="tech_abc", # Generate logic
                company_name=raw_data["company_raw"],
                role_family="Backend",  # Map với Enum
                description=clean_html(raw_data["description_raw"]),
                # ... các field khác
            )
            
            # 3. Nếu data hợp lệ, insert Postgres
            # [SQLAlchemy INSERT logic cho clean_job]
            
            # Đánh dấu đã xử lý trên Mongo
            mongo_db["jobs_bronze"].update_one({"_id": raw_data["_id"]}, {"$set": {"is_processed": True}})
            
        except Exception as e:
            print(f"❌ Dữ liệu job {raw_data['_id']} vi phạm Data Contract: {e}")
```

---

## 🚀 4. To-do List

1. [ ] Đọc schema `JobClean` trong `src/shared/schemas/jobs.py`.
2. [ ] Test kết nối MongoDB và PostgreSQL (`docker compose up -d`).
3. [ ] Viết Crawler (Scrapy/Selenium) lưu vào MongoDB (`mongo_db["jobs_bronze"].insert_one(...)`).
4. [ ] Viết module tách số (salary, experience) bằng Regex.
5. [ ] Áp dụng validation Pydantic và đẩy dữ liệu hoàn thiện từ Mongo sang Postgres.