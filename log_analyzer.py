from pathlib import Path
from collections import Counter

LEVELS = ("ERROR", "WARNING", "INFO", "CRITICAL")

def analyze_log(path):
    file_path = Path(path)
    counts = Counter()

    if not file_path.exists():
        return {
            "total_lines": 0,
            "errors": 0,
            "warnings": 0,
            "critical": 0,
            "recent_issues": ["Log file not found."]
        }

    issues = []
    lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    for line in lines:
        upper = line.upper()
        for level in LEVELS:
            if level in upper:
                counts[level] += 1
        if "ERROR" in upper or "CRITICAL" in upper or "WARNING" in upper:
            issues.append(line)

    return {
        "total_lines": len(lines),
        "errors": counts["ERROR"],
        "warnings": counts["WARNING"],
        "critical": counts["CRITICAL"],
        "recent_issues": issues[-8:]
    }
