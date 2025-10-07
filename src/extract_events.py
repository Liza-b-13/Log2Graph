# src/extract_events.py
import pandas as pd
import json
from typing import List, Dict
from dateutil import parser
from src.llm_interface import simulate_llm_inference

def parse_csv_to_events(csv_path: str, mode: str = "llm") -> List[Dict]:
    """
    Lis le CSV et transforme chaque ligne en événement structuré.
    mode: "llm" (utilise simulate_llm_inference) ou "rule" (regex simple).
    """
    df = pd.read_csv(csv_path)
    events = []

    for _, row in df.iterrows():
        ts_raw = row.get("timestamp")
        try:
            timestamp = parser.isoparse(ts_raw) if pd.notna(ts_raw) else None
        except Exception:
            timestamp = None

        raw = row.get("raw_message", "")
        # Mode LLM : demander à l'interface LLM (ici simulée)
        if mode == "llm":
            llm_out = simulate_llm_inference(raw)
            action = llm_out["action"]
            ips = llm_out["ips"]
            user = llm_out["user"] or row.get("user")
        else:
            # Mode rule-based simple
            text = raw.lower()
            if "ssh" in text:
                action = "ssh_connect"
            elif "sudo" in text:
                action = "privilege_escalation"
            elif "logged in" in text or "login" in text:
                action = "login"
            elif "failed" in text:
                action = "login_failed"
            elif "cat /etc/passwd" in text or "sensitive" in text:
                action = "file_access"
            else:
                action = "unknown"
            ips = []
            if pd.notna(row.get("src_ip")):
                ips.append(row.get("src_ip"))
            if pd.notna(row.get("dst_ip")):
                ips.append(row.get("dst_ip"))
            user = row.get("user")

        # Normalize: prefer src_ip/dst_ip columns if present
        src_ip = row.get("src_ip") if pd.notna(row.get("src_ip")) else (ips[0] if len(ips) >= 1 else None)
        dst_ip = row.get("dst_ip") if pd.notna(row.get("dst_ip")) else (ips[1] if len(ips) >= 2 else None)

        ev = {
            "timestamp": timestamp.isoformat() if timestamp else None,
            "action": action,
            "user": user,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "raw": raw
        }
        events.append(ev)

    return events

def save_events_json(events: List[Dict], out_path: str):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

# Si on exécute ce fichier directement:
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python extract_events.py logs.csv out_events.json [mode]")
    else:
        csv = sys.argv[1]
        out = sys.argv[2]
        mode = sys.argv[3] if len(sys.argv) > 3 else "llm"
        ev = parse_csv_to_events(csv, mode=mode)
        save_events_json(ev, out)
        print(f"Saved {len(ev)} events to {out}")
