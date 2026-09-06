# searcher.py
import requests
from bs4 import BeautifulSoup
import re

def search_web(query: str, max_results: int = 5) -> str:
    """Simple DuckDuckGo HTML search + clean summary."""
    if not query.strip():
        return "Empty search query."

    try:
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        }
        resp = requests.post(url, data={"q": query}, headers=headers, timeout=12)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        results = []

        for a in soup.select("a.result__a")[:max_results]:
            title = a.get_text(strip=True)
            link = a.get("href", "")
            # Clean DuckDuckGo redirect links
            if "uddg=" in link:
                match = re.search(r"uddg=([^&]+)", link)
                if match:
                    from urllib.parse import unquote
                    link = unquote(match.group(1))
            results.append(f"• {title}\n  {link}")

        if not results:
            return "No results found. Try a different query."

        summary = f"🔍 Search results for «{query}»:\n\n" + "\n\n".join(results)
        summary += "\n\n(Tip: open the links in your browser for full details.)"
        return summary

    except requests.exceptions.RequestException as e:
        return f"Network error while searching: {e}"
    except Exception as e:
        return f"Search failed: {e}"