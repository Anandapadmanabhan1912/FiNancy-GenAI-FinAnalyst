import re
from langchain_community.tools import DuckDuckGoSearchResults

def search_news(query: str):
    search = DuckDuckGoSearchResults(max_results=5)
    raw_results = search.run(query)

    links = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', raw_results)
    final_links = [l for l in links if "duckduckgo" not in l][:2]

    return final_links
