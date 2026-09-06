# micro_grolk.py
# Run this file on Pydroid 3

from config import APP_NAME, VERSION
from history import load_history, save_history, add_chat, get_brief_summary
from improver import improve_input, make_plan_if_needed
from searcher import search_web
from error_healer import try_heal, analyze_error

def welcome(data):
    name = data.get("name")
    if name:
        print(f"\n👋 Welcome back, {name}!")
        print("Here’s a brief summary of our last chats:\n")
        print(get_brief_summary(data["chats"]))
        print("-" * 40)
    else:
        print(f"\n🌟 Hello! I am {APP_NAME} v{VERSION}")
        print("I’m a tiny assistant that can improve your requests,")
        print("make plans, search the web, and remember our last 10 chats.")
        name = input("What should I call you? → ").strip() or "Friend"
        data["name"] = name
        save_history(data)
        print(f"Nice to meet you, {name}! Let’s begin.\n")

def process_input(raw: str, data: dict) -> str:
    # 1. Improve input
    improved = improve_input(raw)
    print(f"\n✨ Improved request: {improved}")

    # 2. Optional plan
    plan = make_plan_if_needed(improved)
    if plan:
        print("\n📋 Suggested plan:")
        print(plan)

    # 3. Decide whether to search
    lower = improved.lower()
    needs_search = any(w in lower for w in [
        "search", "find", "what is", "who is", "latest", "news",
        "look up", "google", "information about", "tell me about"
    ])

    if needs_search:
        # Extract a clean query
        query = improved
        for prefix in ["search for ", "find ", "look up ", "tell me about ", "what is ", "who is "]:
            if query.lower().startswith(prefix):
                query = query[len(prefix):].strip()
                break
        print(f"\n🌐 Searching the web for: {query}")
        result = try_heal(search_web, query)
        return result
    else:
        # Simple conversational reply (can be expanded later)
        reply = (
            f"Got it! You asked: «{improved}»\n\n"
            "I can help you plan it, search for information, or just chat.\n"
            "Type a clearer request or say “search …” if you want me to look something up."
        )
        if plan:
            reply = plan + "\n\n" + reply
        return reply

def main():
    print(f"=== {APP_NAME} v{VERSION} ===")
    print("Type 'exit', 'quit' or 'bye' to leave.\n")

    data = load_history()
    welcome(data)

    while True:
        try:
            raw = input(f"\n{data['name']} → ").strip()
            if not raw:
                continue
            if raw.lower() in {"exit", "quit", "bye", "q"}:
                print(f"\nGoodbye, {data['name']}! See you next time 👋")
                break

            # Process with self-healing
            answer = try_heal(process_input, raw, data)
            print("\n" + "─" * 40)
            print(answer)
            print("─" * 40)

            # Record conversation
            add_chat(data, raw, answer)

        except KeyboardInterrupt:
            print(f"\n\nInterrupted. Bye, {data.get('name', 'Friend')}!")
            break
        except Exception as e:
            print(analyze_error(e))

if __name__ == "__main__":
    main()