from telethon import events
from serpapi import GoogleSearch
import configparser
from modules.database import web_searches_collection
from datetime import datetime, timezone  # Import timezone for timezone-aware timestamps

# Load configurations
config = configparser.ConfigParser()
config.read('config.ini')
SERPAPI_KEY = config.get('default', 'serpapi_key')

async def fetch_results(event, search_query):
    # Call SerpAPI
    params = {
        "q": search_query,
        "api_key": SERPAPI_KEY,
        "num": 3
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract search results
    if "organic_results" in results:
        summary = "\n".join([f"{res['title']}: {res['link']}" for res in results["organic_results"][:3]])
        response = f"🔎 Search Results:\n{summary}"
    else:
        response = "❌ No results found."

    # Store search query & results in MongoDB
    web_searches_collection.insert_one({
        "chat_id": event.chat_id,
        "query": search_query,
        "results": results.get("organic_results", []),
        "timestamp": datetime.now(timezone.utc)
    })

    await event.respond(response)