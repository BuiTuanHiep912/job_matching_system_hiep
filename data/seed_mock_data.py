"""Seed dữ liệu mẫu đã validate bằng Pydantic vào PostgreSQL.

Chạy từ thư mục gốc dự án:
    python data/seed_mock_data.py
"""

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import text

from src.shared.db.session import SessionLocal
from src.shared.schemas import (
    CandidateProfile,
    CandidateSkill,
    JobClean,
    JobSkill,
    Level,
    RequirementType,
    RoleFamily,
    SkillDim,
    SkillStatus,
    WorkMode,
)


def _json(value):
    return json.dumps(value, ensure_ascii=False)


def build_skills():
    rows = [
        SkillDim(
            skill_id="skill_python",
            canonical_name="Python",
            aliases=["py", "python3"],
            category="Programming Language",
            description="Ngôn ngữ chính cho backend, data và machine learning.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_sql",
            canonical_name="SQL",
            aliases=["structured query language"],
            category="Data",
            description="Truy vấn và mô hình hóa dữ liệu quan hệ.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_pytorch",
            canonical_name="PyTorch",
            aliases=["torch"],
            category="ML Framework",
            parent_skill_id="skill_python",
            description="Framework huấn luyện mô hình deep learning.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_tensorflow",
            canonical_name="TensorFlow",
            aliases=["tf"],
            category="ML Framework",
            description="Framework machine learning của Google.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_sklearn",
            canonical_name="scikit-learn",
            aliases=["sklearn"],
            category="ML Framework",
            parent_skill_id="skill_python",
            description="Thư viện mô hình học máy cổ điển trên Python.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_pandas",
            canonical_name="Pandas",
            aliases=["pd"],
            category="Data",
            parent_skill_id="skill_python",
            description="Xử lý bảng dữ liệu và feature engineering.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_spark",
            canonical_name="Apache Spark",
            aliases=["spark", "pyspark"],
            category="Data",
            description="Xử lý dữ liệu phân tán cho pipeline ETL.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_aws",
            canonical_name="AWS",
            aliases=["amazon web services"],
            category="Cloud",
            description="Hạ tầng đám mây: S3, EC2, SageMaker.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_docker",
            canonical_name="Docker",
            aliases=["container"],
            category="DevOps",
            description="Đóng gói ứng dụng và mô hình thành container.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_kubernetes",
            canonical_name="Kubernetes",
            aliases=["k8s"],
            category="DevOps",
            description="Điều phối container trên cụm production.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_fastapi",
            canonical_name="FastAPI",
            aliases=["fast api"],
            category="Backend Framework",
            parent_skill_id="skill_python",
            description="Framework API Python hiệu năng cao.",
            status=SkillStatus.ACTIVE,
        ),
        SkillDim(
            skill_id="skill_postgresql",
            canonical_name="PostgreSQL",
            aliases=["postgres"],
            category="Database",
            parent_skill_id="skill_sql",
            description="Cơ sở dữ liệu quan hệ dùng cho ứng dụng và analytics.",
            status=SkillStatus.ACTIVE,
        ),
    ]
    parents = [skill for skill in rows if skill.parent_skill_id is None]
    children = [skill for skill in rows if skill.parent_skill_id is not None]
    return parents + children


def build_jobs():
    return [
        JobClean(
            job_id="job_vinai_mle_001",
            source="topcv",
            source_job_id="topcv-88421",
            url="https://www.topcv.vn/viec-lam/machine-learning-engineer-vinai",
            title="Machine Learning Engineer",
            company_key="vinai",
            company_name="VinAI",
            role_family=RoleFamily.AI_ML,
            description="Xây dựng và triển khai mô hình thị giác máy tính cho sản phẩm nội bộ.",
            requirements="Thành thạo Python và PyTorch. Có kinh nghiệm SQL để chuẩn bị dữ liệu huấn luyện. Ưu tiên người đã dùng AWS SageMaker.",
            benefits="Lương cạnh tranh, ngân sách hội nghị, hybrid 3 ngày tại Hà Nội.",
            salary_min=45000000,
            salary_max=80000000,
            currency="VND",
            location="Ha Noi",
            work_mode=WorkMode.HYBRID,
            level=Level.SENIOR,
            experience_min=4.0,
            experience_max=7.0,
            posted_date=date(2026, 9, 12),
            deadline=date(2026, 10, 31),
        ),
        JobClean(
            job_id="job_fpt_nlp_002",
            source="vietnamworks",
            source_job_id="vnw-55210",
            url="https://www.vietnamworks.com/nlp-engineer-fpt-software",
            title="NLP Engineer",
            company_key="fpt_software",
            company_name="FPT Software",
            role_family=RoleFamily.AI_ML,
            description="Phát triển pipeline xử lý tiếng Việt cho chatbot nội bộ.",
            requirements="Bắt buộc Python, PyTorch và kinh nghiệm fine-tune mô hình ngôn ngữ. Biết Docker để đóng gói service.",
            benefits="Bảo hiểm sức khỏe, làm việc remote 2 ngày mỗi tuần.",
            salary_min=30000000,
            salary_max=50000000,
            currency="VND",
            location="Ho Chi Minh City",
            work_mode=WorkMode.HYBRID,
            level=Level.MID,
            experience_min=2.0,
            experience_max=4.0,
            posted_date=date(2026, 9, 20),
            deadline=date(2026, 11, 15),
        ),
        JobClean(
            job_id="job_tiki_be_003",
            source="itviec",
            source_job_id="itviec-33190",
            url="https://itviec.com/it-jobs/backend-engineer-tiki",
            title="Senior Backend Engineer",
            company_key="tiki",
            company_name="Tiki",
            role_family=RoleFamily.BACKEND,
            description="Thiết kế API đơn hàng và tích hợp thanh toán cho sàn thương mại điện tử.",
            requirements="Thành thạo Python, FastAPI và PostgreSQL. Bắt buộc Docker. Ưu tiên AWS và Kubernetes.",
            benefits="Lương tháng 13, stock option, onsite tại TP.HCM.",
            salary_min=40000000,
            salary_max=70000000,
            currency="VND",
            location="Ho Chi Minh City",
            work_mode=WorkMode.ONSITE,
            level=Level.SENIOR,
            experience_min=5.0,
            experience_max=8.0,
            posted_date=date(2026, 9, 5),
            deadline=date(2026, 10, 20),
        ),
        JobClean(
            job_id="job_vng_be_004",
            source="topcv",
            source_job_id="topcv-90112",
            url="https://www.topcv.vn/viec-lam/junior-backend-developer-vng",
            title="Junior Backend Developer",
            company_key="vng",
            company_name="VNG",
            role_family=RoleFamily.BACKEND,
            description="Tham gia xây dựng API nội dung cho sản phẩm Zalo.",
            requirements="Nắm vững Python và FastAPI. Biết SQL cơ bản. Có dự án cá nhân dùng PostgreSQL là lợi thế.",
            benefits="Đào tạo mentor 6 tháng, hybrid tại Đà Nẵng.",
            salary_min=15000000,
            salary_max=22000000,
            currency="VND",
            location="Da Nang",
            work_mode=WorkMode.HYBRID,
            level=Level.JUNIOR,
            experience_min=0.5,
            experience_max=2.0,
            posted_date=date(2026, 9, 28),
            deadline=date(2026, 11, 30),
        ),
        JobClean(
            job_id="job_grab_de_005",
            source="vietnamworks",
            source_job_id="vnw-61004",
            url="https://www.vietnamworks.com/data-engineer-grab",
            title="Data Engineer",
            company_key="grab",
            company_name="Grab",
            role_family=RoleFamily.DATA,
            description="Xây dựng pipeline dữ liệu chuyến đi trên Spark và kho PostgreSQL.",
            requirements="Bắt buộc SQL, Python và Apache Spark. Thành thạo Pandas cho data quality. Ưu tiên AWS.",
            benefits="Bảo hiểm gia đình, remote-first trong khu vực Việt Nam.",
            salary_min=35000000,
            salary_max=60000000,
            currency="VND",
            location="Ho Chi Minh City",
            work_mode=WorkMode.REMOTE,
            level=Level.MID,
            experience_min=3.0,
            experience_max=5.0,
            posted_date=date(2026, 8, 30),
            deadline=date(2026, 10, 25),
        ),
        JobClean(
            job_id="job_shopee_ds_006",
            source="itviec",
            source_job_id="itviec-44821",
            url="https://itviec.com/it-jobs/data-scientist-shopee",
            title="Data Scientist",
            company_key="shopee",
            company_name="Shopee",
            role_family=RoleFamily.DATA,
            description="Xây mô hình xếp hạng sản phẩm và theo dõi chỉ số recommendation.",
            requirements="Python, Pandas và scikit-learn là bắt buộc. Biết SQL để lấy dữ liệu. PyTorch là lợi thế.",
            benefits="Thưởng theo quý, làm việc hybrid tại Hà Nội.",
            salary_min=28000000,
            salary_max=48000000,
            currency="VND",
            location="Ha Noi",
            work_mode=WorkMode.HYBRID,
            level=Level.MID,
            experience_min=2.0,
            experience_max=4.0,
            posted_date=date(2026, 9, 18),
            deadline=date(2026, 11, 5),
        ),
    ]


def build_job_skills():
    specs = [
        ("job_vinai_mle_001", "skill_python", RequirementType.REQUIRED, 0.95, "Thành thạo Python và PyTorch.", "requirements", 4.0, "section_parser"),
        ("job_vinai_mle_001", "skill_pytorch", RequirementType.REQUIRED, 0.98, "Thành thạo Python và PyTorch.", "requirements", 3.0, "section_parser"),
        ("job_vinai_mle_001", "skill_sql", RequirementType.REQUIRED, 0.70, "Có kinh nghiệm SQL để chuẩn bị dữ liệu huấn luyện.", "requirements", 2.0, "section_parser"),
        ("job_vinai_mle_001", "skill_aws", RequirementType.PREFERRED, 0.45, "Ưu tiên người đã dùng AWS SageMaker.", "requirements", None, "keyword_match"),
        ("job_fpt_nlp_002", "skill_python", RequirementType.REQUIRED, 0.90, "Bắt buộc Python, PyTorch.", "requirements", 2.0, "section_parser"),
        ("job_fpt_nlp_002", "skill_pytorch", RequirementType.REQUIRED, 0.92, "Bắt buộc Python, PyTorch và kinh nghiệm fine-tune.", "requirements", 2.0, "section_parser"),
        ("job_fpt_nlp_002", "skill_docker", RequirementType.PREFERRED, 0.55, "Biết Docker để đóng gói service.", "requirements", None, "keyword_match"),
        ("job_tiki_be_003", "skill_python", RequirementType.REQUIRED, 0.90, "Thành thạo Python, FastAPI và PostgreSQL.", "requirements", 5.0, "section_parser"),
        ("job_tiki_be_003", "skill_fastapi", RequirementType.REQUIRED, 0.88, "Thành thạo Python, FastAPI và PostgreSQL.", "requirements", 3.0, "section_parser"),
        ("job_tiki_be_003", "skill_postgresql", RequirementType.REQUIRED, 0.85, "Thành thạo Python, FastAPI và PostgreSQL.", "requirements", 3.0, "section_parser"),
        ("job_tiki_be_003", "skill_docker", RequirementType.REQUIRED, 0.75, "Bắt buộc Docker.", "requirements", 2.0, "keyword_match"),
        ("job_tiki_be_003", "skill_aws", RequirementType.PREFERRED, 0.50, "Ưu tiên AWS và Kubernetes.", "requirements", None, "keyword_match"),
        ("job_tiki_be_003", "skill_kubernetes", RequirementType.PREFERRED, 0.40, "Ưu tiên AWS và Kubernetes.", "requirements", None, "keyword_match"),
        ("job_vng_be_004", "skill_python", RequirementType.REQUIRED, 0.85, "Nắm vững Python và FastAPI.", "requirements", 1.0, "section_parser"),
        ("job_vng_be_004", "skill_fastapi", RequirementType.REQUIRED, 0.80, "Nắm vững Python và FastAPI.", "requirements", 1.0, "section_parser"),
        ("job_vng_be_004", "skill_sql", RequirementType.REQUIRED, 0.60, "Biết SQL cơ bản.", "requirements", 0.5, "keyword_match"),
        ("job_vng_be_004", "skill_postgresql", RequirementType.PREFERRED, 0.40, "Có dự án cá nhân dùng PostgreSQL là lợi thế.", "requirements", None, "keyword_match"),
        ("job_grab_de_005", "skill_sql", RequirementType.REQUIRED, 0.95, "Bắt buộc SQL, Python và Apache Spark.", "requirements", 3.0, "section_parser"),
        ("job_grab_de_005", "skill_python", RequirementType.REQUIRED, 0.85, "Bắt buộc SQL, Python và Apache Spark.", "requirements", 3.0, "section_parser"),
        ("job_grab_de_005", "skill_spark", RequirementType.REQUIRED, 0.92, "Bắt buộc SQL, Python và Apache Spark.", "requirements", 2.0, "section_parser"),
        ("job_grab_de_005", "skill_pandas", RequirementType.REQUIRED, 0.65, "Thành thạo Pandas cho data quality.", "requirements", 2.0, "keyword_match"),
        ("job_grab_de_005", "skill_aws", RequirementType.PREFERRED, 0.50, "Ưu tiên AWS.", "requirements", None, "keyword_match"),
        ("job_shopee_ds_006", "skill_python", RequirementType.REQUIRED, 0.90, "Python, Pandas và scikit-learn là bắt buộc.", "requirements", 2.0, "section_parser"),
        ("job_shopee_ds_006", "skill_pandas", RequirementType.REQUIRED, 0.80, "Python, Pandas và scikit-learn là bắt buộc.", "requirements", 2.0, "section_parser"),
        ("job_shopee_ds_006", "skill_sklearn", RequirementType.REQUIRED, 0.84, "Python, Pandas và scikit-learn là bắt buộc.", "requirements", 2.0, "section_parser"),
        ("job_shopee_ds_006", "skill_sql", RequirementType.REQUIRED, 0.70, "Biết SQL để lấy dữ liệu.", "requirements", 2.0, "keyword_match"),
        ("job_shopee_ds_006", "skill_pytorch", RequirementType.PREFERRED, 0.35, "PyTorch là lợi thế.", "requirements", None, "keyword_match"),
    ]
    return [
        JobSkill(
            job_id=job_id,
            skill_id=skill_id,
            requirement_type=requirement_type,
            importance=importance,
            evidence=evidence,
            section=section,
            experience_years=experience_years,
            extraction_method=extraction_method,
        )
        for job_id, skill_id, requirement_type, importance, evidence, section, experience_years, extraction_method in specs
    ]


def build_candidates():
    return [
        CandidateProfile(
            candidate_id="cand_junior_linh",
            skills=[
                CandidateSkill(skill_id="skill_python", weight=0.70, user_confirmed=True, evidence=["CV: Python Developer intern tại VNG, 2025-2026"]),
                CandidateSkill(skill_id="skill_fastapi", weight=0.65, user_confirmed=True, evidence=["Dự án cá nhân: REST API quản lý đơn hàng bằng FastAPI"]),
                CandidateSkill(skill_id="skill_sql", weight=0.45, user_confirmed=False, evidence=["Mô tả kinh nghiệm có viết truy vấn báo cáo"]),
                CandidateSkill(skill_id="skill_postgresql", weight=0.40, user_confirmed=False, evidence=["Đồ án tốt nghiệp dùng PostgreSQL"]),
            ],
            role_probs={"Backend": 0.72, "Data": 0.15, "AI/ML": 0.08},
            experience_years=1.5,
            experience=[
                {
                    "title": "Backend Intern",
                    "company": "VNG",
                    "start": "2025-06",
                    "end": "2026-06",
                    "highlights": ["Viết API nội bộ bằng Python", "Viết truy vấn SQL cho báo cáo vận hành"],
                }
            ],
            education=[{"school": "Đại học Bách khoa Đà Nẵng", "degree": "Cử nhân CNTT", "year": 2025}],
            level=Level.JUNIOR,
            location="Da Nang",
            certifications=[],
        ),
        CandidateProfile(
            candidate_id="cand_mid_ha",
            skills=[
                CandidateSkill(skill_id="skill_sql", weight=0.85, user_confirmed=True, evidence=["3 năm viết pipeline SQL tại Grab"]),
                CandidateSkill(skill_id="skill_python", weight=0.75, user_confirmed=True, evidence=["PySpark job xử lý log chuyến đi"]),
                CandidateSkill(skill_id="skill_spark", weight=0.70, user_confirmed=False, evidence=["CV ghi Apache Spark nhưng chưa được ứng viên xác nhận"]),
                CandidateSkill(skill_id="skill_pandas", weight=0.60, user_confirmed=True, evidence=["Notebook kiểm tra chất lượng dữ liệu"]),
                CandidateSkill(skill_id="skill_aws", weight=0.40, user_confirmed=False, evidence=["Nhắc tới S3 trong một dự án phụ"]),
            ],
            role_probs={"Data": 0.68, "Backend": 0.18, "AI/ML": 0.10},
            experience_years=3.0,
            experience=[
                {
                    "title": "Data Engineer",
                    "company": "Grab",
                    "start": "2023-07",
                    "end": "2026-09",
                    "highlights": ["Duy trì pipeline Spark hàng ngày", "Chuẩn hóa bảng sự kiện trên PostgreSQL"],
                }
            ],
            education=[{"school": "Đại học Khoa học Tự nhiên TP.HCM", "degree": "Cử nhân Toán tin", "year": 2023}],
            level=Level.MID,
            location="Ho Chi Minh City",
            certifications=["AWS Cloud Practitioner"],
        ),
        CandidateProfile(
            candidate_id="cand_senior_minh",
            skills=[
                CandidateSkill(skill_id="skill_python", weight=0.92, user_confirmed=True, evidence=["6 năm sản xuất mô hình Python tại VinAI"]),
                CandidateSkill(skill_id="skill_pytorch", weight=0.95, user_confirmed=True, evidence=["Huấn luyện mô hình phát hiện đối tượng bằng PyTorch"]),
                CandidateSkill(skill_id="skill_sql", weight=0.55, user_confirmed=True, evidence=["Viết truy vấn lấy tập huấn luyện từ kho dữ liệu"]),
                CandidateSkill(skill_id="skill_aws", weight=0.60, user_confirmed=True, evidence=["Triển khai endpoint trên AWS SageMaker"]),
                CandidateSkill(skill_id="skill_docker", weight=0.50, user_confirmed=False, evidence=["Dockerfile có trong repo nội bộ, chưa xác nhận trên CV"]),
                CandidateSkill(skill_id="skill_sklearn", weight=0.35, user_confirmed=False, evidence=["Dùng baseline scikit-learn trước khi chuyển sang deep learning"]),
            ],
            role_probs={"AI/ML": 0.78, "Data": 0.14, "Backend": 0.05},
            experience_years=6.5,
            experience=[
                {
                    "title": "Machine Learning Engineer",
                    "company": "VinAI",
                    "start": "2020-03",
                    "end": "2026-09",
                    "highlights": ["Đưa mô hình thị giác vào production", "Fine-tune mô hình ngôn ngữ tiếng Việt"],
                }
            ],
            education=[{"school": "Đại học Bách khoa Hà Nội", "degree": "Thạc sĩ Khoa học máy tính", "year": 2020}],
            level=Level.SENIOR,
            location="Ha Noi",
            certifications=["AWS Certified Machine Learning Specialty"],
        ),
    ]


def _insert_many(session, label, statement, rows):
    print(f"Đang tạo bảng {label}...")
    inserted = 0
    skipped = 0
    for row in rows:
        result = session.execute(statement, row)
        if result.rowcount:
            inserted += result.rowcount
        else:
            skipped += 1
    print(f"Hoàn thành {label}: thêm {inserted}, bỏ qua {skipped} bản ghi đã tồn tại.")


def seed():
    skills = build_skills()
    jobs = build_jobs()
    job_skills = build_job_skills()
    candidates = build_candidates()
    print(
        f"Validate Pydantic xong: {len(skills)} skills, {len(jobs)} jobs, "
        f"{len(job_skills)} job_skills, {len(candidates)} candidates."
    )

    skill_sql = text(
        """
        INSERT INTO skills_dim (
            skill_id, canonical_name, aliases, category,
            parent_skill_id, description, status
        ) VALUES (
            :skill_id, :canonical_name, CAST(:aliases AS jsonb), :category,
            :parent_skill_id, :description, :status
        )
        ON CONFLICT (skill_id) DO NOTHING
        """
    )
    job_sql = text(
        """
        INSERT INTO jobs_clean (
            job_id, source, source_job_id, url, title, company_key, company_name,
            role_family, description, requirements, benefits,
            salary_min, salary_max, currency, location, work_mode, level,
            experience_min, experience_max, posted_date, deadline
        ) VALUES (
            :job_id, :source, :source_job_id, :url, :title, :company_key, :company_name,
            :role_family, :description, :requirements, :benefits,
            :salary_min, :salary_max, :currency, :location, :work_mode, :level,
            :experience_min, :experience_max, :posted_date, :deadline
        )
        ON CONFLICT (job_id) DO NOTHING
        """
    )
    job_skill_sql = text(
        """
        INSERT INTO job_skills (
            job_id, skill_id, requirement_type, importance, evidence,
            section, experience_years, extraction_method
        ) VALUES (
            :job_id, :skill_id, :requirement_type, :importance, :evidence,
            :section, :experience_years, :extraction_method
        )
        ON CONFLICT (job_id, skill_id) DO NOTHING
        """
    )
    candidate_sql = text(
        """
        INSERT INTO candidate_profile (
            candidate_id, role_probs, experience_years, experience, education,
            level, location, certifications
        ) VALUES (
            :candidate_id, CAST(:role_probs AS jsonb), :experience_years,
            CAST(:experience AS jsonb), CAST(:education AS jsonb),
            :level, :location, CAST(:certifications AS jsonb)
        )
        ON CONFLICT (candidate_id) DO NOTHING
        """
    )
    candidate_skill_sql = text(
        """
        INSERT INTO candidate_skills (
            candidate_id, skill_id, weight, user_confirmed, evidence
        ) VALUES (
            :candidate_id, :skill_id, :weight, :user_confirmed, CAST(:evidence AS jsonb)
        )
        ON CONFLICT (candidate_id, skill_id) DO NOTHING
        """
    )

    skill_rows = []
    for skill in skills:
        row = skill.model_dump(mode="json")
        row["aliases"] = _json(row["aliases"])
        skill_rows.append(row)

    job_rows = [job.model_dump(mode="json") for job in jobs]
    job_skill_rows = [item.model_dump(mode="json") for item in job_skills]

    candidate_rows = []
    candidate_skill_rows = []
    for candidate in candidates:
        profile = candidate.model_dump(mode="json")
        nested_skills = profile.pop("skills")
        profile["role_probs"] = _json(profile["role_probs"])
        profile["experience"] = _json(profile["experience"])
        profile["education"] = _json(profile["education"])
        profile["certifications"] = _json(profile["certifications"])
        candidate_rows.append(profile)
        for skill in nested_skills:
            skill["evidence"] = _json(skill["evidence"])
            skill["candidate_id"] = candidate.candidate_id
            candidate_skill_rows.append(skill)

    with SessionLocal() as session:
        with session.begin():
            _insert_many(session, "skills_dim", skill_sql, skill_rows)
            _insert_many(session, "jobs_clean", job_sql, job_rows)
            _insert_many(session, "job_skills", job_skill_sql, job_skill_rows)
            _insert_many(session, "candidate_profile", candidate_sql, candidate_rows)
            _insert_many(session, "candidate_skills", candidate_skill_sql, candidate_skill_rows)

            counts = session.execute(
                text(
                    """
                    SELECT 'skills_dim' AS table_name, COUNT(*) FROM skills_dim
                    UNION ALL SELECT 'jobs_clean', COUNT(*) FROM jobs_clean
                    UNION ALL SELECT 'job_skills', COUNT(*) FROM job_skills
                    UNION ALL SELECT 'candidate_profile', COUNT(*) FROM candidate_profile
                    UNION ALL SELECT 'candidate_skills', COUNT(*) FROM candidate_skills
                    ORDER BY table_name
                    """
                )
            ).all()
    print("Hoàn thành seed. Số dòng hiện có:")
    for table_name, count in counts:
        print(f"  {table_name}: {count}")


if __name__ == "__main__":
    seed()
