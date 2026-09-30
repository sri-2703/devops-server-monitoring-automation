# DevOps Server Monitoring & Automation System

A student-level DevOps project built with Python, Bash, Linux, SQLite, Docker and Git.

## Features

- CPU, memory and disk monitoring
- Linux/system information
- Network connectivity check
- Application log analysis
- SQLite monitoring history
- Python automation
- Bash health-check and backup scripts
- Docker containerization
- Web dashboard
- Git/GitHub-ready project structure

## Architecture

User -> Flask Dashboard -> Monitoring API -> System Metrics / Network / Logs -> SQLite

## Requirements

- Python 3.10+
- Git
- Docker Desktop (optional)
- Linux/Ubuntu/WSL recommended for Bash scripts

## Run locally

### 1. Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start application

```bash
python app.py
```

Open:

http://127.0.0.1:5000

The dashboard refreshes every 10 seconds.

## Run with Docker

```bash
docker build -t devops-monitor .
docker run -p 5000:5000 devops-monitor
```

Or:

```bash
docker compose up --build
```

Open:

http://localhost:5000

## Bash scripts

From Linux/WSL:

```bash
chmod +x scripts/*.sh

./scripts/health_check.sh
./scripts/system_info.sh
./scripts/backup.sh
```

## API endpoints

### GET /api/status

Returns:

- CPU usage
- Memory usage
- Disk usage
- Host information
- Network reachability
- Log statistics

### GET /api/history

Returns the latest monitoring records stored in SQLite.

## Suggested GitHub workflow

```bash
git init
git add .
git commit -m "Initial DevOps monitoring project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Interview explanation

"I built a DevOps Server Monitoring and Automation System using Python, Bash, Linux and Docker. It collects CPU, memory and disk metrics, checks network connectivity, analyzes application logs, stores monitoring history in SQLite, and exposes the information through a Flask dashboard. I also created Bash scripts for health checks, system information and log backups. Docker was used to containerize the application."

## Future improvements

- Prometheus metrics
- Grafana dashboards
- Jenkins CI/CD
- Kubernetes deployment
- Email/Slack alerts
- ELK-based centralized logging
