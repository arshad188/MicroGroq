# history.py
import json
import os
from config import HISTORY_FILE, MAX_HISTORY

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {"name": None, "chats": []}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Keep only last MAX_HISTORY
        data["chats"] = data.get("chats", [])[-MAX_HISTORY:]
        return data
    except Exception:
        return {"name": None, "chats": []}

def save_history(data):
    data["chats"] = data.get("chats", [])[-MAX_HISTORY:]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_chat(data, user_msg, assistant_msg):
    data["chats"].append({
        "user": user_msg,
        "assistant": assistant_msg
    })
    data["chats"] = data["chats"][-MAX_HISTORY:]
    save_history(data)

def get_brief_summary(chats):
    if not chats:
        return "No previous conversations yet."
    lines = []
    for i, c in enumerate(chats[-5:], 1):  # last 5 for brevity
        u = c["user"][:60] + ("..." if len(c["user"]) > 60 else "")
        a = c["assistant"][:80] + ("..." if len(c["assistant"]) > 80 else "")
        lines.append(f"{i}. You: {u}\n   Me : {a}")
    return "\n".join(lines)