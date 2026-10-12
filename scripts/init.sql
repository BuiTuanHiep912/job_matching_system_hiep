-- scripts/init.sql

-- 1. BẢNG SKILLS_DIM (Master Ontology)
CREATE TABLE IF NOT EXISTS skills_dim (
    skill_id VARCHAR(50) PRIMARY KEY,
    canonical_name VARCHAR(100) NOT NULL,
    aliases JSONB DEFAULT '[]'::jsonb,
    category VARCHAR(100) NOT NULL,
    parent_skill_id VARCHAR(50) REFERENCES skills_dim(skill_id),
    description TEXT,
    status VARCHAR(20) DEFAULT 'active'
);

-- 2. BẢNG JOBS_CLEAN (Silver Layer)
CREATE TABLE IF NOT EXISTS jobs_clean (
    job_id VARCHAR(100) PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    source_job_id VARCHAR(100),
    url TEXT NOT NULL,
    title VARCHAR(255) NOT NULL,
    company_key VARCHAR(100) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    role_family VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT NOT NULL,
    benefits TEXT NOT NULL,
    salary_min NUMERIC(15, 2),
    salary_max NUMERIC(15, 2),
    currency VARCHAR(10),
    location VARCHAR(100),
    work_mode VARCHAR(20),
    level VARCHAR(50),
    experience_min NUMERIC(4, 1),
    experience_max NUMERIC(4, 1),
    posted_date DATE,
    deadline DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. BẢNG DEDUP_MAP (Ánh xạ trùng lặp)
CREATE TABLE IF NOT EXISTS dedup_map (
    canonical_job_id VARCHAR(100) NOT NULL REFERENCES jobs_clean(job_id) ON DELETE CASCADE,
    duplicate_job_id VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL,
    dedup_method VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (canonical_job_id, duplicate_job_id)
);

-- 4. BẢNG JOB_SKILLS (Gold Layer - Mapping Job và Skill)
CREATE TABLE IF NOT EXISTS job_skills (
    job_id VARCHAR(100) NOT NULL REFERENCES jobs_clean(job_id) ON DELETE CASCADE,
    skill_id VARCHAR(50) NOT NULL REFERENCES skills_dim(skill_id) ON DELETE CASCADE,
    requirement_type VARCHAR(20) NOT NULL,
    importance NUMERIC(3, 2) NOT NULL,
    evidence TEXT,
    section VARCHAR(50),
    experience_years NUMERIC(4, 1),
    extraction_method VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (job_id, skill_id)
);

-- 5. BẢNG ROLE_PROFILE (Gold Layer - Thống kê theo Role)
CREATE TABLE IF NOT EXISTS role_profile (
    role_family VARCHAR(50) PRIMARY KEY,
    job_count INT NOT NULL DEFAULT 0,
    common_skills JSONB DEFAULT '[]'::jsonb,
    characteristic_skills JSONB DEFAULT '[]'::jsonb,
    skill_distribution JSONB DEFAULT '{}'::jsonb,
    level_distribution JSONB DEFAULT '{}'::jsonb,
    experience_stats JSONB DEFAULT '{}'::jsonb,
    salary_stats JSONB DEFAULT '{}'::jsonb,
    location_distribution JSONB DEFAULT '{}'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. BẢNG CANDIDATE_PROFILE (Gold Layer - Profile ứng viên từ CV)
CREATE TABLE IF NOT EXISTS candidate_profile (
    candidate_id VARCHAR(100) PRIMARY KEY,
    role_probs JSONB DEFAULT '{}'::jsonb,
    experience_years NUMERIC(4, 1) DEFAULT 0.0,
    experience JSONB DEFAULT '[]'::jsonb,
    education JSONB DEFAULT '[]'::jsonb,
    level VARCHAR(50),
    location VARCHAR(100),
    certifications JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. BẢNG CANDIDATE_SKILLS (Mapping Candidate và Skill)
CREATE TABLE IF NOT EXISTS candidate_skills (
    candidate_id VARCHAR(100) NOT NULL REFERENCES candidate_profile(candidate_id) ON DELETE CASCADE,
    skill_id VARCHAR(50) NOT NULL REFERENCES skills_dim(skill_id) ON DELETE CASCADE,
    weight NUMERIC(3, 2) NOT NULL,
    user_confirmed BOOLEAN DEFAULT FALSE,
    evidence JSONB DEFAULT '[]'::jsonb,
    PRIMARY KEY (candidate_id, skill_id)
);

-- 8. BẢNG EVALUATION_GROUND_TRUTH (Group 4 - Ground Truth đánh giá)
CREATE TABLE IF NOT EXISTS evaluation_ground_truth (
    id SERIAL PRIMARY KEY,
    candidate_id VARCHAR(100) NOT NULL REFERENCES candidate_profile(candidate_id) ON DELETE CASCADE,
    job_id VARCHAR(100) NOT NULL REFERENCES jobs_clean(job_id) ON DELETE CASCADE,
    relevance_label INT NOT NULL CHECK (relevance_label BETWEEN 0 AND 3),
    human_matched_skills JSONB DEFAULT '[]'::jsonb,
    annotator VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_candidate_job UNIQUE (candidate_id, job_id)
);
