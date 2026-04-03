-- ============================================================
-- SwarmDigiz — Connector Execution History
-- ============================================================

CREATE TABLE IF NOT EXISTS connector_executions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  run_id INTEGER,
  connector_name TEXT NOT NULL,
  success INTEGER NOT NULL,
  message TEXT,
  request_json TEXT,
  response_json TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_connector_exec_username
  ON connector_executions(username);

CREATE INDEX IF NOT EXISTS idx_connector_exec_run_id
  ON connector_executions(run_id);

CREATE INDEX IF NOT EXISTS idx_connector_exec_created_at
  ON connector_executions(created_at);