CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS contracts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT,
  raw_text TEXT,
  normalized_text TEXT,
  input_format TEXT,
  file_name TEXT,
  file_size_bytes INT,
  page_count INT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS contract_sections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contract_id UUID REFERENCES contracts(id) ON DELETE CASCADE,
  section_type TEXT NOT NULL,
  clause_type TEXT,
  title TEXT,
  content TEXT NOT NULL,
  page_start INT,
  page_end INT,
  position_index INT,
  embedding vector(1536),
  is_amendment BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS contract_sections_embedding_idx
  ON contract_sections USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE TABLE IF NOT EXISTS clause_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  analysis_run_id UUID NOT NULL,
  section_id UUID REFERENCES contract_sections(id),
  clause_type TEXT NOT NULL,
  section_type TEXT,
  extracted_text TEXT NOT NULL,
  key_terms JSONB DEFAULT '[]',
  defined_terms_used JSONB DEFAULT '[]',
  cross_references JSONB DEFAULT '[]',
  risk_level TEXT CHECK (risk_level IN ('low','medium','high','critical')),
  risk_score NUMERIC(4,2),
  risk_rationale TEXT,
  recommendation TEXT,
  suggested_language TEXT,
  recommendation_priority TEXT,
  similar_precedents JSONB DEFAULT '[]',
  page_start INT,
  page_end INT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS analysis_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contract_id UUID REFERENCES contracts(id) ON DELETE CASCADE,
  status TEXT DEFAULT 'pending' 
    CHECK (status IN ('pending','running','completed','failed','partial')),
  overall_risk_score NUMERIC(4,2),
  overall_risk_level TEXT,
  score_breakdown JSONB DEFAULT '{}',
  explanation TEXT,
  clause_count INT,
  high_risk_count INT,
  critical_risk_count INT,
  workflow_version TEXT DEFAULT '1.0.0',
  total_tokens_used INT,
  total_latency_ms INT,
  started_at TIMESTAMPTZ DEFAULT now(),
  completed_at TIMESTAMPTZ,
  error_summary JSONB DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS node_executions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  analysis_run_id UUID REFERENCES analysis_runs(id) ON DELETE CASCADE,
  node_name TEXT NOT NULL,
  status TEXT CHECK (status IN ('started','completed','failed','skipped')),
  input_snapshot JSONB,
  output_snapshot JSONB,
  tool_calls JSONB DEFAULT '[]',
  model_used TEXT,
  prompt_tokens INT,
  completion_tokens INT,
  latency_ms INT,
  error TEXT,
  executed_at TIMESTAMPTZ DEFAULT now()
);

