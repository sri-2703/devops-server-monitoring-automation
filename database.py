import sqlite3
from pathlib import Path

DB_PATH = Path("monitoring.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_percent REAL NOT NULL,
                memory_percent REAL NOT NULL,
                disk_percent REAL NOT NULL,
                network_reachable INTEGER NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                message TEXT NOT NULL,
                severity TEXT NOT NULL
            )
        """)


def save_metrics(metrics, network_reachable):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO metrics
            (timestamp, cpu_percent, memory_percent, disk_percent, network_reachable)
            VALUES (?, ?, ?, ?, ?)
        """, (
            metrics["timestamp"],
            metrics["cpu_percent"],
            metrics["memory_percent"],
            metrics["disk_percent"],
            int(network_reachable)
        ))


def save_alert(timestamp, alert_type, message, severity):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO alerts
            (timestamp, alert_type, message, severity)
            VALUES (?, ?, ?, ?)
        """, (timestamp, alert_type, message, severity))


def get_recent_metrics(limit=30):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT timestamp,
                   cpu_percent,
                   memory_percent,
                   disk_percent,
                   network_reachable
            FROM metrics
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    rows.reverse()

    return [
        {
            "timestamp": row[0],
            "cpu_percent": row[1],
            "memory_percent": row[2],
            "disk_percent": row[3],
            "network_reachable": bool(row[4])
        }
        for row in rows
    ]


def get_recent_alerts(limit=10):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT timestamp,
                   alert_type,
                   message,
                   severity
            FROM alerts
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return [
        {
            "timestamp": row[0],
            "alert_type": row[1],
            "message": row[2],
            "severity": row[3]
        }
        for row in rows
    ]