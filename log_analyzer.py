import argparse
import os
import glob
import json
import re
from dataclasses import dataclass
from collections import Counter, defaultdict

LOG_PATTERN = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.+)\] "([A-Z]+) (.*?)' \
              r' HTTP/1\.[01]" \d{3} \d+ ".*?" ".*?" (\d+)'
METHODS = ('GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'DELETE')


@dataclass
class LogEntry:
    ip: str
    timestamp: str
    method: str
    url: str
    duration: int


def analyze_log_file(file_path):
    stats = defaultdict(int)
    ip_counter = Counter()
    longest_requests = []

    with open(file_path, 'r') as f:
        for line in f:
            match = re.search(LOG_PATTERN, line)
            if match:
                ip, timestamp, method, url, duration = match.groups()
                log_entry = LogEntry(ip, timestamp, method, url, int(duration))

                stats['total_requests'] += 1
                if log_entry.method in METHODS:
                    stats[log_entry.method] += 1
                ip_counter[log_entry.ip] += 1
                longest_requests.append(log_entry)

    stats['top_ips'] = {ip: count for ip, count in ip_counter.most_common(3)}
    stats['top_longest'] = [{'ip': entry.ip, 'date': f"[{entry.timestamp}]", 'method': entry.method, 'url': entry.url,
                             'duration': entry.duration} for
                            entry in sorted(longest_requests, key=lambda x: x.duration, reverse=True)[:3]]
    stats['total_stat'] = {key: value for key, value in stats.items() if key in METHODS}

    return stats


def save_and_print_stats(stats, output_file):
    with open(output_file, 'w') as f:
        json.dump(stats, f, indent=2, sort_keys=True)
    print(json.dumps(stats, indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description='Analyze access.log files')
    parser.add_argument('input_path', help='Path to the log file or directory containing log files')
    args = parser.parse_args()

    if os.path.isfile(args.input_path):
        log_files = [args.input_path]
    elif os.path.isdir(args.input_path):
        log_files = glob.glob(os.path.join(args.input_path, '*.log'))
    else:
        print(f"Invalid input path: {args.input_path}")
        return

    for log_file in log_files:
        print(f"Analyzing log file: {log_file}")
        stats = analyze_log_file(log_file)
        output_file = f"{os.path.splitext(log_file)[0]}_result.json"
        save_and_print_stats(stats, output_file)


if __name__ == "__main__":
    main()
