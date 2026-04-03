-- =====================================================
-- 010_add_lead_tier.sql
-- Add lead tier classification
-- =====================================================

ALTER TABLE inspection_runs
ADD COLUMN lead_tier TEXT DEFAULT 'cold';