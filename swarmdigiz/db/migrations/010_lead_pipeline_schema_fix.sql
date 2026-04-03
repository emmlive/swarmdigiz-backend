-- =====================================================
-- 010_lead_pipeline_schema_fix.sql
-- Stabilize lead pipeline schema
-- =====================================================

ALTER TABLE inspection_runs ADD COLUMN lead_tier TEXT DEFAULT 'cold';
ALTER TABLE inspection_runs ADD COLUMN booking_status TEXT DEFAULT 'new';
ALTER TABLE inspection_runs ADD COLUMN customer_name TEXT;
ALTER TABLE inspection_runs ADD COLUMN customer_email TEXT;
ALTER TABLE inspection_runs ADD COLUMN customer_phone TEXT;
ALTER TABLE inspection_runs ADD COLUMN notes TEXT;