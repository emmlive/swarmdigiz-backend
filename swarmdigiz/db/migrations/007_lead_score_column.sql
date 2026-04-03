-- =========================================================
-- LEAD INTELLIGENCE COLUMN
-- =========================================================

ALTER TABLE inspection_runs
ADD COLUMN lead_score INTEGER DEFAULT 0;