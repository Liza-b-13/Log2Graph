# tests/test_extract.py
from src.extract_events import parse_csv_to_events
import os

def test_parse_sample():
    path = "sample_logs.csv"
    events = parse_csv_to_events(path, mode="llm")
    assert isinstance(events, list)
    assert len(events) >= 1
    assert "action" in events[0]
