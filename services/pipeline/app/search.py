import os
import requests

def fetch_webcrawler_results(query: str) -> str:

    api_key = os.getenv("TAVILY_API_KEY")
    url = os.getenv("TAVILY_URL")

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": False
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        web_context = "\n".join([f"Source: {r['title']}\nContent: {r['content']}\n" for r in results[:3]])
        return web_context

    except Exception as e:
        print(f"[TAVILY ERROR] {e}")
        return ""