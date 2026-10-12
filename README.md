# 🚀 Job-CV Matching System

Hệ thống tự động thu thập tin tuyển dụng, trích xuất dữ liệu, phân tích kỹ năng từ CV ứng viên và thực hiện thuật toán Gợi ý việc làm (Recommendation) có độ chính xác cao.

Dự án được xây dựng dựa trên kiến trúc **Medallion Architecture (Bronze -> Silver -> Gold)** kết hợp với **Interface-Driven Development** (định nghĩa chuẩn dữ liệu khắt khe giữa các team thông qua Pydantic).

---

## 🏗 Kiến trúc Hệ thống Tổng thể

Dự án sử dụng cơ sở dữ liệu phân lớp để đảm bảo an toàn, tốc độ và dễ bảo trì:

*   🥉 **Tầng Bronze (Data Lake - MongoDB):** Nơi chứa dữ liệu thô (Raw HTML/JSON) cào từ web. Dữ liệu ở đây có thể lộn xộn, thiếu sót.
*   🥈 **Tầng Silver (Data Warehouse - PostgreSQL):** Dữ liệu đã được làm sạch, ép kiểu (số ra số, ngày ra ngày) và xóa trùng lặp.
*   🥇 **Tầng Gold (ML/Analytics - PostgreSQL):** Dữ liệu mang tính nghiệp vụ đã được NLP/LLM bóc tách (Bảng Mapping Job-Skill, Candidate-Skill). Đây là đầu vào trực tiếp cho thuật toán Match CV.

---

## 👥 Phân công & Cấu trúc Thư mục

Dự án áp dụng mô hình Monorepo, được chia làm 4 Nhóm (Groups) hoạt động độc lập:

```text
src/
├── shared/               # 🛑 VÙNG BẤT KHẢ XÂM PHẠM (Dùng chung)
│   ├── schemas/          # Các Data Contract (Pydantic) - LUẬT của hệ thống
│   ├── db/               # Kết nối PostgreSQL và MongoDB
│   └── nlp_parser/       # Bộ thư viện bóc tách Text dùng chung cho G2 & G3
│
├── g1_data_ingestion/    # [Nhóm 1] Crawl Web -> Lưu MongoDB -> Clean -> Lưu Postgres
├── g2_job_ontology/      # [Nhóm 2] Quản lý bộ từ điển Kỹ năng (Taxonomy) & Parse Job Text
├── g3_cv_processing/     # [Nhóm 3] Đọc file CV (PDF/DOCX) -> Parse CV Text
└── g4_recommendation/    # [Nhóm 4] Thuật toán Matching, Ranking CV-Job & Đánh giá (Metrics)
```
👉 *Đọc kỹ file `README.md` bên trong từng thư mục `g1`, `g2`, `g3`, `g4` để biết chi tiết task của nhóm mình.*

---

## 🛠 Hướng dẫn Setup Môi trường Local

Để bắt đầu code, các thành viên làm theo đúng 4 bước sau (yêu cầu máy đã cài Python 3.10+ và Docker):

### Bước 1: Clone code và tạo môi trường ảo (Virtual Environment)
```bash
git clone <url-repo-cua-ban>
cd job_matching_system

# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường (Windows)
venv\Scripts\activate
# Kích hoạt môi trường (Mac/Linux)
source venv/bin/activate
```

### Bước 2: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 3: Khởi động Database (PostgreSQL & MongoDB)
Dự án đã cấu hình sẵn Docker Compose. Bạn chỉ cần chạy:
```bash
docker compose up -d
```
*(Hệ thống sẽ tự động tạo các bảng DB cấu trúc Silver & Gold thông qua file `scripts/init.sql`).*

### Bước 4: Bơm Dữ liệu Mẫu (Mock Data)
Để Nhóm 2, 3, 4 có dữ liệu chạy thuật toán ngay lập tức mà không cần chờ Nhóm 1 cào data, hãy chạy script sau:
```bash
python data/seed_mock_data.py
```
✅ *Nếu terminal báo "Đã bơm mock data thành công!", bạn đã sẵn sàng bắt tay vào code chức năng của nhóm mình!*

---

## ⚠️ 3 Quy tắc Vàng (Rules of Engagement)

1.  **Tôn trọng Data Contract:** Mọi dữ liệu đẩy xuống PostgreSQL **BẮT BUỘC** phải Validate thông qua các Class trong thư mục `src/shared/schemas/`. Nếu Pydantic báo lỗi sai kiểu dữ liệu, KHÔNG ĐƯỢC ép kiểu bừa bãi, phải sửa lại code logic của nhóm mình.
2.  **Làm việc trên Nhánh riêng (Git Branching):** 
    *   Nhóm nào tạo nhánh tên nhóm đó (VD: `feature/g1-crawler`, `feature/g4-jaccard-scoring`).
    *   Tuyệt đối không push thẳng lên nhánh `main`.
3.  **Dùng chung Core NLP:** Nhóm 2 (Đọc Job) và Nhóm 3 (Đọc CV) phải cùng đóng góp và gọi chung hàm bóc tách text tại `src/shared/nlp_parser/`. Điều này đảm bảo Job và CV bắt ra được chung 1 mã Skill_ID.