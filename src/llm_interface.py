# src/llm_interface.py
import re
from typing import Dict, Any, List
import json
from pathlib import Path

# Optional: load extra keyword patterns from data/keywords.json if present
def load_custom_keywords(path: str = "data/keywords.json") -> Dict[str, List[str]]:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Expect format: {"ssh_connect": ["ssh", "connected via ssh", ...], ...}
            return {k: v for k, v in data.items() if isinstance(v, list)}
    except Exception:
        return {}

# Core simulation function with extended keywords / regex
def simulate_llm_inference(text: str) -> Dict[str, Any]:
    """
    Simulation améliorée d'un LLM : retourne un dict contenant:
      - action: type d'événement (login, ssh_connect, privilege_escalation, file_access, credential_use, login_failed, unknown)
      - ips: liste d'IP trouvées
      - user: utilisateur (si trouvé)
      - raw: texte original

    La fonction utilise une combinaison de mots-clefs simples et de regex pour
    reconnaître des variantes courantes dans les logs. Elle charge aussi des
    mots-clefs personnalisés depuis data/keywords.json si ce fichier existe.
    """
    if text is None:
        text = ""
    t = text.lower()

    # Load custom keywords (optional)
    custom = load_custom_keywords()

    # Prebuilt keyword -> canonical action mapping (list of patterns or simple substrings)
    keyword_map = {
        "privilege_escalation": [
            r"\bsudo\b",
            r"\bescalat(e|ed|ion)\b",
            r"privilege escalation",
            r"su -",
            r"admin rights",
            r"become root"
        ],
        "ssh_connect": [
            r"\bssh\b",
            r"connected via ssh",
            r"ssh from",
            r"ssh connection",
            r"remote login via ssh",
            r"connection to .*ssh"
        ],
        "login": [
            r"\blogged in\b",
            r"\bsuccessful login\b",
            r"\bsign?ed in\b",
            r"\bsession opened\b",
            r"\blogin\b(?!.*failed)"
        ],
        "login_failed": [
            r"\bfailed login\b",
            r"\bauthentication failure\b",
            r"\binvalid password\b",
            r"\blogin failed\b",
            r"\bfailed sign?in\b"
        ],
        "file_access": [
            r"cat /etc/passwd",
            r"cat /etc/shadow",
            r"cat /var/secret",
            r"\bcat\b.*(/etc|/var|secret|passwd|shadow)",
            r"\bread\b.*(password|secret|shadow|passwd)",
            r"\bdownload(ed|ing)?\b",
            r"\baccess(ed|ing)?\b.*(file|sensitive|secret)"
        ],
        "credential_use": [
            r"\bcredential\b",
            r"\bpassword\b.*used\b",
            r"\bused password\b",
            r"\buse credential\b",
            r"\bcreds\b",
            r"\btoken\b.*used\b"
        ]
    }

    # Merge custom patterns (if provided) — custom overrides/extends builtins
    for act, patterns in custom.items():
        if act in keyword_map:
            # extend list
            keyword_map[act].extend(patterns)
        else:
            keyword_map[act] = patterns

    # Try matching patterns (first match wins, order above gives priority)
    action = "unknown"
    for act, patterns in keyword_map.items():
        for pat in patterns:
            try:
                # If pattern looks like a simple substring (no special regex chars), do substring check for speed
                if re.match(r'^[\w\s/-]+$', pat):
                    if pat in t:
                        action = act
                        break
                else:
                    if re.search(pat, t):
                        action = act
                        break
            except re.error:
                # Fallback: substring match
                if pat in t:
                    action = act
                    break
        if action != "unknown":
            break

    # Extraction d'IPs : supporte IPv4 et IPv6-ish simple (focus IPv4)
    ip_match = re.findall(r'(?:\d{1,3}\.){3}\d{1,3}', text)
    # Also try to catch hostnames like host-01.example.com (simple heuristic)
    host_match = re.findall(r'\b[a-z0-9-]+(?:\.[a-z0-9-]+)+\b', text, flags=re.IGNORECASE)
    # Keep unique, prioritise IPs
    ips = ip_match.copy()
    for h in host_match:
        # ignore if looks like an IP
        if not re.match(r'^(?:\d{1,3}\.){3}\d{1,3}$', h):
            ips.append(h)
    # deduplicate preserving order
    seen = set()
    ips = [x for x in ips if not (x in seen or seen.add(x))]

    # Extraction de l'utilisateur : plusieurs motifs possibles
    user = None
    user_patterns = [
        r'\bby\s+([a-z0-9_.-]+)\b',          # "by alice"
        r'\buser[:=]\s*([a-z0-9_.-]+)\b',    # "user: alice"
        r'\bfor\s+user\s+([a-z0-9_.-]+)\b',  # "for user alice"
        r'\buser\s+([a-z0-9_.-]+)\b',        # "user alice"
        r'\baccount\s+([a-z0-9_.-]+)\b'      # "account alice"
    ]
    for up in user_patterns:
        m = re.search(up, text, flags=re.IGNORECASE)
        if m:
            user = m.group(1)
            break

    # Final return
    return {
        "action": action,
        "ips": ips,
        "user": user,
        "raw": text
    }
