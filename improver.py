# improver.py
def improve_input(raw: str) -> str:
    """Make the user's request clearer and more actionable."""
    raw = raw.strip()
    if not raw:
        return "Please tell me what you need help with."

    # Simple heuristic improvements
    improved = raw
    lower = raw.lower()

    # Common polite fillers removal / clarification
    if lower.startswith(("can you ", "could you ", "please ")):
        improved = raw[raw.find(" ") + 1:].strip()
        improved = improved[0].upper() + improved[1:] if improved else improved

    # Add clarity markers
    if "?" not in improved and not any(w in lower for w in ["how", "what", "why", "explain", "plan", "steps"]):
        improved = f"Help me with: {improved}"

    return improved

def make_plan_if_needed(text: str) -> str:
    """Turn a request into a short doable plan when it looks complex."""
    lower = text.lower()
    keywords = ["plan", "steps", "how to", "guide", "tutorial", "build", "create", "learn", "project"]
    if any(k in lower for k in keywords) or len(text.split()) > 12:
        plan = (
            f"Doable plan for: «{text}»\n\n"
            "1. Clarify the exact goal and constraints.\n"
            "2. Break it into 3–5 small, concrete steps.\n"
            "3. Gather any missing information or resources.\n"
            "4. Execute step by step and check results.\n"
            "5. Review and improve.\n\n"
            "Would you like me to expand any of these steps?"
        )
        return plan
    return ""