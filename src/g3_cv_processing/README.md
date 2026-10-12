# 📄 Group 3: CV Processing & Profile Extraction (Tầng Raw CV $\rightarrow$ Gold)

Nhiệm vụ cốt lõi: **Đọc file CV (PDF/DOCX) $\rightarrow$ Trích xuất văn bản $\rightarrow$ Bóc tách kỹ năng ứng viên $\rightarrow$ Đẩy vào kho Profile chuẩn.**

## 🗺️ 1. Luồng dữ liệu (Data Workflow)

1. **PDF Parser (`pdf_to_text.py`)**: Nhận file CV từ người dùng $\rightarrow$ Dùng OCR/Text Parser (PyPDF2, pdfplumber) để trích xuất thành chuỗi văn bản thuần (Text).
2. **CV Extractor (`cv_extractor.py`)**: Đọc chuỗi văn bản, đối chiếu với bộ từ vựng `skills_dim` (của G2) $\rightarrow$ Lưu kết quả vào bảng `candidate_profile` và `candidate_skills`.

---

## 📋 2. Đặc tả công việc chi tiết (Tasks)

### Module 3.1: Trích xuất Văn bản (PDF Parser)
*   **Vị trí code:** `src/g3_cv_processing/pdf_to_text.py`
*   **Input:** File `.pdf` hoặc `.docx`.
*   **Output:** Biến kiểu `String` chứa toàn bộ nội dung CV.
*   **Lưu ý cực kỳ quan trọng:** Rất nhiều CV thiết kế dạng **2 cột**. Nếu dùng thư viện đọc PDF cùi bắp, nó sẽ đọc theo hàng ngang lấn từ cột trái sang cột phải làm nát bét câu văn. Hãy ưu tiên dùng `pdfplumber` hoặc các thư viện hỗ trợ layout-aware parsing.

### Module 3.2: Bóc tách Kỹ năng & Profile (CV Extractor)
*   **Vị trí code:** `src/g3_cv_processing/cv_extractor.py`
*   **Input:** Văn bản CV (String) + Danh mục `skills_dim`.
*   **Output:** Object `CandidateProfile` (Pydantic) $\rightarrow$ `INSERT` vào bảng PostgreSQL.
*   **Hướng dẫn xử lý:**
    1.  **Bắt buộc dùng chung NLP:** Việc bắt từ khóa kỹ năng phải dùng lại hàm của thư mục `src/shared/nlp_parser/` mà G2 đang dùng. Không được tự viết hàm Regex riêng.
    2.  **Tính Weight (Trọng số):** Thuật toán cần đánh giá độ tự tin (0.0 $\rightarrow$ 1.0). 
        * Nếu skill chỉ nằm trơ trọi ở mục "Skills": `weight = 0.4`.
        * Nếu skill nằm trong phần mô tả "Work Experience" kèm câu hoàn chỉnh: `weight = 0.8 - 1.0`.
    3.  **User Confirmed:** Mặc định khi AI bóc tách, `user_confirmed = False`. (Sẽ thành `True` nếu sau này có UI cho ứng viên tự tick chọn).

---

## 🔒 3. Data Contract (Hợp đồng Dữ liệu)

Toàn bộ logic insert vào DB phải đi qua Pydantic model `CandidateProfile`.

```python
from src.shared.schemas import CandidateProfile, CandidateSkill
from src.shared.db.session import SessionLocal

def process_cv_and_save(candidate_id: str, cv_text: str):
    # 1. Gọi hàm NLP dùng chung để bắt skill
    extracted_skills = extract_skills_with_nlp(cv_text)
    
    # 2. Xây dựng object Skill
    candidate_skills_list = []
    for data in extracted_skills:
        skill = CandidateSkill(
            skill_id=data["skill_id"], 
            weight=calculate_context_weight(cv_text, data["keyword"]),
            user_confirmed=False,
            evidence=[data["sentence_context"]]
        )
        candidate_skills_list.append(skill)
        
    try:
        # 3. Validate Profile tổng
        profile = CandidateProfile(
            candidate_id=candidate_id,
            skills=candidate_skills_list,
            role_probs={"Backend": 0.7, "Data": 0.3}, # Thuật toán dự đoán role
            experience_years=2.5 # Thuật toán extract từ chuỗi thời gian
        )
        
        # 4. Insert vào PostgreSQL bảng candidate_profile & candidate_skills
        db = SessionLocal()
        # [SQLAlchemy INSERT logic]
        
    except Exception as e:
        print(f"❌ CV {candidate_id} vi phạm Data Contract: {e}")
```

---

## 🚀 4. To-do List

1. [ ] Đọc các schema `CandidateProfile`, `CandidateSkill` trong `src/shared/schemas/candidates.py`.
2. [ ] Thử nghiệm `pdfplumber` với 5 CV mẫu xem có bị lỗi nối cột không.
3. [ ] Phối hợp với Group 2 để chốt hàm dùng chung trong `shared/nlp_parser/`.
4. [ ] Viết hàm tính weight dựa trên vị trí xuất hiện của từ khóa trong CV.