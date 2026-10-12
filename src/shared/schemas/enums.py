from enum import Enum

class RoleFamily(str, Enum):
    AI_ML = "AI/ML"
    BACKEND = "Backend"
    FRONTEND = "Frontend"
    DATA = "Data"
    DEVOPS_CLOUD = "DevOps/Cloud"
    QA = "QA"
    MOBILE = "Mobile"
    SECURITY = "Security"
    PRODUCT_PROJECT = "Product/Project"
    UI_UX = "UI/UX"
    OTHER = "Other"

class Level(str, Enum):
    INTERN = "Intern"
    FRESHER = "Fresher"
    JUNIOR = "Junior"
    MID = "Mid"
    SENIOR = "Senior"
    LEAD = "Lead"
    MANAGER = "Manager"

class WorkMode(str, Enum):
    REMOTE = "remote"
    ONSITE = "onsite"
    HYBRID = "hybrid"

class RequirementType(str, Enum):
    REQUIRED = "required"
    PREFERRED = "preferred"

class SkillStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
