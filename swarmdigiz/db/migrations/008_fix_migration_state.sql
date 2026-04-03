-- =====================================================
-- 007_fix_migration_state.sql
-- Fix partially applied migration 006
-- =====================================================

INSERT OR IGNORE INTO migration_log (version, name, checksum)
VALUES (6, '006_business_isolation.sql', 'manual_fix');

UPDATE schema_version
SET version = 6
WHERE id = 1;