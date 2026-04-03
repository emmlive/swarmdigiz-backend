# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timedelta

DB_PATH = "swarmdigiz/swarmdigiz.db"


def check_system_health():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    issues = []

    # Recent inspections
    cur.execute(
        """
        SELECT COUNT(*)
        FROM inspection_runs
        WHERE created_at > datetime('now','-24 hours')
        """
    )

    inspections = cur.fetchone()[0]

    if inspections == 0:
        issues.append("⚠ No inspections detected in the last 24 hours")

    # Campaign launches
    try:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM swarm_runs
            WHERE created_at > datetime('now','-24 hours')
            """
        )

        campaigns = cur.fetchone()[0]

        if campaigns == 0:
            issues.append("⚠ Marketing Swarm has not launched campaigns recently")

    except:
        pass

    conn.close()

    if not issues:
        issues.append("✅ All AI systems operating normally")

    return issues