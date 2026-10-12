# 🧠 Group 2: Job Ontology & Skill Extraction (Tầng Silver -> Gold)

Nhiệm vụ cốt lõi: **Xây dựng từ điển kỹ năng chuẩn (Taxonomy/Ontology) -> Đọc text Job Description -> Trích xuất thành các kỹ năng cụ thể -> Thống kê dữ liệu theo Role.**

## 🗺️ 1. Luồng dữ liệu (Data Workflow)

1. **Taxonomy Builder (`taxonomy_builder.py`)**: Tạo và quản lý danh mục kỹ năng gốc -> Lưu vào bảng `skills_dim`.
2. **Job Extractor (`job_extractor.py`)**: Đọc field `description` và `requirements` từ bảng `jobs_clean` (do Nhóm 1 làm), đối chiếu với `skills_dim` để tìm kỹ năng -> Lưu kết quả vào bảng `job_skills`.
3. **Role Profiler (`role_profiler.py`)**: Gom nhóm dữ liệu từ `job_skills` theo `role_family` -> Thống kê skill phổ biến -> Lưu vào bảng `role_profile`.

---

## 📋 2. Đặc tả công việc chi tiết (Tasks)

### Module 2.1: Quản lý Từ điển Kỹ năng (Taxonomy Builder)
*   **Vị trí code:** `src/g2_job_ontology/taxonomy_builder.py`
*   **Output:** `INSERT` vào bảng **`skills_dim`**.
*   **Quy tắc:**
    *   Bảng này là **Hợp đồng chung cho cả hệ thống**. Tuyệt đối không được phép có 2 ID cho cùng một skill (VD: Không được tồn tại cả `SK_PYTHON` và `SK_PYTHON3`).
    *   Phải quản lý tốt `aliases` (từ đồng nghĩa). Ví dụ: `canonical_name` là "PyTorch", thì `aliases` là `["torch", "py-torch"]`. Thuật toán NLP sẽ dùng mảng `aliases` này để bắt keyword.

### Module 2.2: Trích xuất Kỹ năng từ Job (Job Extractor) - *[QUAN TRỌNG NHẤT]*
*   **Vị trí code:** `src/g2_job_ontology/job_extractor.py` và `src/shared/nlp_parser/`
*   **Input:** Text từ `jobs_clean`.
*   **Output:** Object `JobSkill` (Pydantic) -> `INSERT` vào bảng **`job_skills`**.
*   **Hướng dẫn xử lý:**
    1.  **Dùng chung Module NLP:** Logic match text với `skills_dim` **bắt buộc** phải viết trong thư mục `src/shared/nlp_parser/skill_matcher.py`. Nhóm 3 (CV) sẽ gọi lại đúng hàm này để bắt skill.
    2.  **Requirement Type:** Dựa vào từ khóa xung quanh, xác định skill này là `required` (bắt buộc) hay `preferred` (ưu tiên).
    3.  **Importance Score:** Tính trọng số (0.0 -> 1.0). Skill required = 1.0, preferred = 0.5.
    4.  **Kinh nghiệm:** Nếu bắt được cụm "3 years of Python", ghi số `3.0` vào field `experience_years`.

### Module 2.3: Xây dựng Profile cho Role (Role Profiler)
*   **Vị trí code:** `src/g2_job_ontology/role_profiler.py`
*   **Input:** Bảng `jobs_clean` JOIN với `job_skills`.
*   **Output:** Object `RoleProfile` -> `INSERT` vào bảng **`role_profile`**.
*   **Hướng dẫn xử lý:**
    *   Dùng Pandas hoặc SQL `GROUP BY role_family`.
    *   Tính tần suất xuất hiện của các skill trong 1 role (VD: Backend có 1000 jobs, 800 jobs yêu cầu SQL -> SQL có `frequency = 0.8`).

---

## 🔒 3. Data Contract (Hợp đồng Dữ liệu)

Mọi dòng dữ liệu trước khi đẩy vào SQL phải đi qua Pydantic schema của Nhóm 2.

```python
from src.shared.schemas import JobSkill, RequirementType
from src.shared.db.session import SessionLocal

def process_job_and_save(job_id: str, job_description_text: str):
    # 1. Gọi hàm NLP dùng chung để bắt skill từ text
    extracted_data = extract_skills_with_nlp(job_description_text) 
    
    db = SessionLocal()
    for data in extracted_data:
        try:
            # 2. Validate qua Pydantic
            job_skill = JobSkill(
                job_id=job_id,
                skill_id=data["skill_id"], 
                requirement_type=RequirementType(data["type"]), # Ép Enum
                importance=1.0 if data["type"] == "required" else 0.5,
                evidence=data["ev"],
                section="requirements",
                experience_years=data.get("years", None),
                extraction_method="spacy_ner_matcher"
            )
            
            # 3. Nếu data hợp lệ, insert Postgres
            # [SQLAlchemy INSERT logic cho job_skill]
            
        except Exception as e:
            print(f"❌ Map lỗi Job {job_id} với Skill {data['skill_id']}: {e}")
```

---

## 🚀 4. To-do List

1. [ ] Đọc các schema `SkillDim`, `JobSkill`, `RoleProfile` trong `src/shared/schemas/skills.py`.
2. [ ] Lên danh sách JSON hardcode tầm 100 Skill phổ biến ngành IT (Kèm alias) và chạy script insert vào `skills_dim`.
3. [ ] Viết hàm `extract_skills_with_nlp()` đặt vào `src/shared/nlp_parser/`.
4. [ ] Truy vấn thử 50 `jobs_clean` từ PostgreSQL, chạy qua hàm NLP và insert kết quả vào `job_skills`.
5. [ ] Viết câu lệnh SQL/Pandas sinh ra dữ liệu cho `role_profile`. 