from flask import Flask, render_template, jsonify
from datetime import datetime

from monitor import collect_system_metrics, check_network
from log_analyzer import analyze_log
from database import (
    init_db,
    save_metrics,
    save_alert,
    get_recent_metrics,
    get_recent_alerts
)

app = Flask(__name__)

init_db()


# -----------------------------
# Thresholds
# -----------------------------

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 85


# -----------------------------
# Alert Checking
# -----------------------------

def check_alerts(metrics, network):

    alerts = []

    if metrics["cpu_percent"] >= CPU_THRESHOLD:
        alerts.append({
            "type": "CPU",
            "message": f"CPU usage is high: {metrics['cpu_percent']}%",
            "severity": "HIGH"
        })

    if metrics["memory_percent"] >= MEMORY_THRESHOLD:
        alerts.append({
            "type": "MEMORY",
            "message": f"Memory usage is high: {metrics['memory_percent']}%",
            "severity": "HIGH"
        })

    if metrics["disk_percent"] >= DISK_THRESHOLD:
        alerts.append({
            "type": "DISK",
            "message": f"Disk usage is high: {metrics['disk_percent']}%",
            "severity": "HIGH"
        })

    if not network["reachable"]:
        alerts.append({
            "type": "NETWORK",
            "message": "Network connectivity check failed",
            "severity": "CRITICAL"
        })

    # Save alerts to database
    for alert in alerts:
        save_alert(
            metrics["timestamp"],
            alert["type"],
            alert["message"],
            alert["severity"]
        )

    return alerts


# -----------------------------
# Dashboard
# -----------------------------

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# -----------------------------
# Current Status API
# -----------------------------

@app.route("/api/status")
def status():

    metrics = collect_system_metrics()

    network = check_network("8.8.8.8")

    log_summary = analyze_log("logs/application.log")

    # Save monitoring data
    save_metrics(
        metrics,
        network["reachable"]
    )

    # Check alerts
    alerts = check_alerts(
        metrics,
        network
    )

    return jsonify({
        "metrics": metrics,
        "network": network,
        "logs": log_summary,
        "alerts": alerts
    })


# -----------------------------
# Monitoring History API
# -----------------------------

@app.route("/api/history")
def history():

    return jsonify(
        get_recent_metrics(30)
    )


# -----------------------------
# Alert History API
# -----------------------------

@app.route("/api/alerts")
def alerts():

    return jsonify(
        get_recent_alerts(30)
    )


# -----------------------------
# Test Alert API
# -----------------------------

@app.route("/api/test-alerts", methods=["POST"])
def test_alerts():

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    test_alert_list = [

        {
            "type": "NETWORK",
            "message": "Test network connectivity failure",
            "severity": "CRITICAL"
        },

        {
            "type": "CPU",
            "message": "Test CPU usage exceeded threshold",
            "severity": "WARNING"
        },

        {
            "type": "MEMORY",
            "message": "Test memory usage exceeded threshold",
            "severity": "WARNING"
        }

    ]

    # Save test alerts
    for alert in test_alert_list:

        save_alert(
            timestamp,
            alert["type"],
            alert["message"],
            alert["severity"]
        )

    return jsonify({
        "message": "Test alerts generated successfully",
        "alerts": test_alert_list
    })


# -----------------------------
# Run Application
# -----------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )