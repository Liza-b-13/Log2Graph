# src/llm_interface.py
import re
from typing import Dict, Any

def simulate_llm_inference(text: str) -> Dict[str, Any]:
    """
    Simulation simple d'un LLM : transformation d'un message brut en
    événement structuré. On recherche des mots-clés et on renvoie un dict.
    """
    t = text.lower()

    # mapping simple par mot-clé
    if "sudo" in t or "privilege escalation" in t or "privilege_escalation" in t:
        action = "privilege_escalation"
    elif "ssh" in t or "ssh connection" in t:
        action = "ssh_connect"
    elif "logged in" in t or "login" in t:
        action = "login"
    elif "failed login" in t or "failed authentication" in t:
        action = "login_failed"
    elif "cat /etc/passwd" in t or "sensitive file" in t:
        action = "file_access"
    elif "credential" in t or "use credential" in t or "used password" in t:
        action = "credential_use"
    else:
        # fallback: try to extract verbs/nouns (very naive)
        if re.search(r'\baccess(ed|ing)?\b', t):
            action = "file_access"
        else:
            action = "unknown"

    # tentative d'extraction de IP / user (regex simple)
    ip_match = re.findall(r'(?:\d{1,3}\.){3}\d{1,3}', t)
    user_match = re.search(r'\bby ([a-z0-9_.-]+)\b', t)
    user = user_match.group(1) if user_match else None

    return {
        "action": action,
        "ips": ip_match,
        "user": user,
        "raw": text
    }

# Optional: placeholder to integrate a real LLM (transformers / OpenAI)
# def real_llm_infer(text: str):
#     """
#     Exemple (commenté) : si tu veux appeler transformers pipeline ou l'API OpenAI,
#     implémente ici. Garder la simulation si tu n'as pas de clé / GPU.
#     """
#     from transformers import pipeline
#     clf = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
#     candidates = ["login", "ssh_connect", "privilege_escalation", "file_access", "credential_use"]
#     res = clf(text, candidate_labels=candidates)
#     best = res['labels'][0]
#     return {"action": best, "score": res['scores'][0], "raw": text}
