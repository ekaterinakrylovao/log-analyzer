import re
from datetime import datetime

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^]]+)] "(?P<method>\S+) (?P<resource>\S+) \S+" (?P<status>\d+) (?P<size>\d+|-) '
    r'"(?P<referrer>[^"]*)" "(?P<agent>[^"]*)"'
)


def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    time_str = match.group("time")
    log_time = datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S %z")

    return {
        "ip": match.group("ip"),
        "time": log_time,
        "method": match.group("method"),
        "resource": match.group("resource"),
        "status": int(match.group("status")),
        "size": int(match.group("size")) if match.group("size") != "-" else 0,
        "agent": match.group("agent"),  # Добавляем поле agent
    }
