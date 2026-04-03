-- =========================================================
-- ADD MISSING VISUAL INSPECTOR COLUMNS
-- =========================================================


-- ---------------------------------------------------------
-- inspection_runs.service_type
-- ---------------------------------------------------------

ALTER TABLE inspection_runs
ADD COLUMN service_type TEXT;


-- ---------------------------------------------------------
-- inspection_runs.estimated_quote
-- ---------------------------------------------------------

ALTER TABLE inspection_runs
ADD COLUMN estimated_quote REAL;


-- ---------------------------------------------------------
-- services.config
-- JSON configuration used by pricing engine
-- ---------------------------------------------------------

ALTER TABLE services
ADD COLUMN config TEXT;