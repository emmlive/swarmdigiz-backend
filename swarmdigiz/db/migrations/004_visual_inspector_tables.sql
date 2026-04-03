-- =========================================================
-- VISUAL INSPECTOR CORE TABLES
-- Migration: 004_visual_inspector_tables.sql
-- Purpose:
--   Adds tables required for:
--   - Lead Pipeline
--   - Campaign Analytics
--   - Visual Inspector
--   - Quote Engine
--   - Booking Automation
-- =========================================================


-- =========================================================
-- SERVICES
-- Stores the services a business offers
-- Used by:
--   Service Configuration
--   Quote Engine
--   Visual Inspector
-- =========================================================

CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT,
    base_price REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_services_business
ON services(business_id);



-- =========================================================
-- INSPECTION RUNS
-- Stores visual inspection results + generated quotes
-- Used by:
--   Lead Pipeline
--   Visual Inspector
--   Quote Engine
-- =========================================================

CREATE TABLE IF NOT EXISTS inspection_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    lead_name TEXT,
    lead_email TEXT,
    inspection_result TEXT,
    quote_amount REAL,
    status TEXT DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_inspection_business
ON inspection_runs(business_id);



-- =========================================================
-- CONNECTOR LOGS
-- Tracks outbound integrations (ads, CRM, email, etc.)
-- Used by:
--   Campaign Analytics
--   AI Operations Monitor
-- =========================================================

CREATE TABLE IF NOT EXISTS connector_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    connector_type TEXT,
    payload TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_connector_business
ON connector_logs(business_id);