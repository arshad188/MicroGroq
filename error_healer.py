# error_healer.py
import traceback
import sys

def analyze_error(exc: Exception) -> str:
    """Classify the error and give concrete improvement suggestions."""
    tb = traceback.format_exc()
    name = type(exc).__name__
    msg = str(exc)

    suggestions = []

    if name == "ModuleNotFoundError":
        suggestions.append("→ Install the missing package in Pydroid: Pip → install <package>")
        suggestions.append("→ Or wrap the import in a try/except and give a friendly message.")
    elif name == "ConnectionError" or "timeout" in msg.lower() or "network" in msg.lower():
        suggestions.append("→ Check internet connection / Wi-Fi.")
        suggestions.append("→ Add longer timeout or retry logic.")
        suggestions.append("→ Provide an offline fallback message.")
    elif name == "KeyError":
        suggestions.append("→ Use .get(key, default) instead of direct dictionary access.")
    elif name == "IndexError":
        suggestions.append("→ Check list length before indexing.")
    elif name == "JSONDecodeError":
        suggestions.append("→ Validate or recreate the history file.")
        suggestions.append("→ Add a backup / default empty structure.")
    elif name == "AttributeError":
        suggestions.append("→ Check object type before calling methods.")
    else:
        suggestions.append("→ Add more specific try/except blocks.")
        suggestions.append("→ Log the full traceback for debugging.")

    report = (
        f"⚠️ Error Analysis\n"
        f"Type : {name}\n"
        f"Msg  : {msg}\n\n"
        f"Suggestions to improve the code:\n"
        + "\n".join(suggestions)
        + f"\n\nFull traceback (for developers):\n{tb}"
    )
    return report

def try_heal(func, *args, **kwargs):
    """
    Simple self-healing wrapper.
    Tries the function; on failure runs analysis and, for a few common cases,
    attempts a safer alternative.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        report = analyze_error(e)
        print("\n" + report + "\n")

        # Very light self-healing examples
        if "ModuleNotFoundError" in type(e).__name__:
            print("→ Healing attempt: continuing without the missing optional feature.")
            return "Feature temporarily unavailable (missing module)."
        if "timeout" in str(e).lower() or "Connection" in type(e).__name__:
            print("→ Healing attempt: returning offline message.")
            return "I couldn't reach the internet right now. Please try again later."

        # Generic fallback
        return f"Something went wrong, but I recovered: {e}"