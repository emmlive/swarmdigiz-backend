-- =====================================================
-- 006_business_isolation.sql
-- Multi-tenant business isolation layer
-- SAFE / IDEMPOTENT VERSION
-- =====================================================

PRAGMA foreign_keys = OFF;

BEGIN TRANSACTION;

-- -----------------------------------------------------
-- BUSINESSES TABLE
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS businesses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_username TEXT NOT NULL,
    business_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- SWARM RUNS
-- -----------------------------------------------------

-- SQLite safe column add
ALTER TABLE swarm_runs ADD COLUMN business_id INTEGER DEFAULT 0;

CREATE INDEX IF NOT EXISTS idx_swarm_runs_business
ON swarm_runs(business_id);

-- -----------------------------------------------------
-- SWARM OUTPUTS
-- -----------------------------------------------------

ALTER TABLE swarm_outputs ADD COLUMN business_id INTEGER DEFAULT 0;

-- -----------------------------------------------------
-- INSPECTION RUNS
-- -----------------------------------------------------

ALTER TABLE inspection_runs ADD COLUMN business_id INTEGER DEFAULT 0;

CREATE INDEX IF NOT EXISTS idx_inspections_business
ON inspection_runs(business_id);

COMMIT;

PRAGMA foreign_keys = ON;