# test_contract.py
from src.shared.schemas import JobClean

try:
    # Cố tình truyền sai dữ liệu (truyền String vào trường Float, hoặc sai Enum)
    bad_job = JobClean(
        job_id="job_123",
        source="vietjobs",
        url="https://...",
        title="Python Dev",
        company_key="abc",
        company_name="ABC",
        role_family="Backend", # Đúng Enum
        description="...",
        requirements="...",
        benefits="...",
        experience_min="BA NĂM" # LỖI Ở ĐÂY: Phải là float
    )
except Exception as e:
    print("PHÁT HIỆN LỖI DATA CONTRACT:")
    print(e)
