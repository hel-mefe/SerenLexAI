-- UI / CRUD entities: source of truth for the frontend.
-- Requires: users table (FK user_id). Run after your main schema.

CREATE TABLE IF NOT EXISTS analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  original_filename VARCHAR(255),
  source_type VARCHAR(50) NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  overall_risk VARCHAR(20),
  risk_score INT,
  flagged_count INT DEFAULT 0,
  high_count INT DEFAULT 0,
  medium_count INT DEFAULT 0,
  low_count INT DEFAULT 0,
  raw_text TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS clauses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  analysis_id UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  severity VARCHAR(20) NOT NULL,
  original_text TEXT NOT NULL,
  risk_explanation TEXT NOT NULL,
  recommended_action TEXT NOT NULL,
  clause_type VARCHAR(50),
  position_index INT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS clauses_analysis_id_idx ON clauses(analysis_id);

CREATE TABLE IF NOT EXISTS actions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  analysis_id UUID REFERENCES analyses(id) ON DELETE SET NULL,
  type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description VARCHAR(512) NOT NULL,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS actions_analysis_id_idx ON actions(analysis_id);
CREATE INDEX IF NOT EXISTS actions_user_id_idx ON actions(user_id);
