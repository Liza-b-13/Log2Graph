# parse_logs.py
import re
import pandas as pd

LOG_PATTERN = re.compile(
    r'(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+user=(?P<user>\S+)\s+action=(?P<action>\S+)(?:\s+file=(?P<file>\S+))?(?:\s+src=(?P<src>\S+))?(?:\s+dst=(?P<dst>\S+))?(?:\s+method=(?P<method>\S+))?'
)

def parse_line(line):
    m = LOG_PATTERN.search(line)
    if not m:
        return None
    return m.groupdict()

def parse_file(path):
    rows = []
    with open(path, 'r') as f:
        for line in f:
            p = parse_line(line.strip())
            if p:
                rows.append(p)
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = parse_file("../data/sample_logs.txt")
    print(df)

