from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field
from .enums import RoleFamily, Level, WorkMode

class JobBronze(BaseModel):
    raw_id: str
    source: str
    url: str
    crawl_time: datetime
    title_raw: Optional[str] = None
    company_raw: Optional[str] = None
    description_raw: Optional[str] = None
    requirements_raw: Optional[str] = None
    benefits_raw: Optional[str] = None
    salary_raw: Optional[str] = None
    location_raw: Optional[str] = None
    experience_raw: Optional[str] = None
    level_raw: Optional[str] = None
    posted_date_raw: Optional[str] = None
    deadline_raw: Optional[str] = None

class JobClean(BaseModel):
    job_id: str = Field(..., description="ID của job canonical sau dedup")
    source: str
    source_job_id: Optional[str] = None
    url: str
    title: str
    company_key: str
    company_name: str
    role_family: RoleFamily
    description: str
    requirements: str
    benefits: str
    
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[WorkMode] = None
    level: Optional[Level] = None
    
    experience_min: Optional[float] = None
    experience_max: Optional[float] = None
    
    posted_date: Optional[date] = None
    deadline: Optional[date] = None

class DedupMap(BaseModel):
    canonical_job_id: str = Field(..., description="ID job được giữ lại")
    duplicate_job_id: str = Field(..., description="ID job bị trùng")
    source: str = Field(..., description="Nguồn của job duplicate")
    dedup_method: str = Field(..., description="Ví dụ: exact_url, title_company_match, manual")
