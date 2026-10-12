from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from .enums import Level

class CandidateSkill(BaseModel):
    skill_id: str
    weight: float = Field(..., ge=0.0, le=1.0)
    user_confirmed: bool = False
    evidence: List[str] = Field(default_factory=list)

class CandidateProfile(BaseModel):
    candidate_id: str
    skills: List[CandidateSkill] = Field(default_factory=list)
    
    role_probs: Dict[str, float] = Field(
        default_factory=dict,
        description="Ví dụ: {'AI/ML': 0.55, 'Backend': 0.20}"
    )
    
    experience_years: float = 0.0
    experience: List[Dict] = Field(default_factory=list)
    education: List[Dict] = Field(default_factory=list)
    
    level: Optional[Level] = None
    location: Optional[str] = None
    certifications: List[str] = Field(default_factory=list)
