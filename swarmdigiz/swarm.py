
import threading
import sqlite3
from datetime import datetime
from main import run_marketing_swarm

def db(db_path):
    return sqlite3.connect(db_path, check_same_thread=False)

def save_history(db_path, project_id, agent, output, cost):
    conn = db(db_path)
    conn.execute(
        "INSERT INTO swarm_history (project_id,agent,output,cost,run_at) VALUES (?,?,?,?,?)",
        (project_id, agent, output, cost, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def run_agent_async(db_path, project_id, agent, payload, cost, callback):
    def task():
        out = run_marketing_swarm({**payload, "active_swarm":[agent]})
        result = out.get(agent, "")
        save_history(db_path, project_id, agent, result, cost)
        callback(agent, result)
    threading.Thread(target=task, daemon=True).start()
