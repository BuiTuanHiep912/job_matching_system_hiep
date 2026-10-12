from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from .enums import RequirementType, SkillStatus

class SkillDim(BaseModel):
    skill_id: str
    canonical_name: str
    aliases: List[str] = Field(default_factory=list)
    category: str
    parent_skill_id: Optional[str] = None
    description: Optional[str] = None
    status: SkillStatus = SkillStatus.ACTIVE

class JobSkill(BaseModel):
    job_id: str
    skill_id: str
    requirement_type: RequirementType
    importance: float = Field(..., ge=0.0, le=1.0)
    evidence: str
    section: str
    experience_years: Optional[float] = None
    extraction_method: str

class RoleProfile(BaseModel):
    role_family: str
    job_count: int
    common_skills: List[Dict[str, Any]] = Field(default_factory=list)
    characteristic_skills: List[Dict[str, Any]] = Field(default_factory=list)
    skill_distribution: Dict[str, Any] = Field(default_factory=dict)
    level_distribution: Dict[str, Any] = Field(default_factory=dict)
    experience_stats: Dict[str, Any] = Field(default_factory=dict)
    salary_stats: Dict[str, Any] = Field(default_factory=dict)
    location_distribution: Dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
