from langchain.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich import print

import requests
import os

load_dotenv()

tavily = TavilySearch(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=5
)

@tool
def web_search(query: str) -> str:
    """
    Search for recent and reliable information on a topic.
    Returns titles, URLs and snippets(summary).
    """

    results = tavily.invoke(query)
    # print(type(results))
    # print(results)

    output = []

    for r in results['results']:
        output.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )

    return "\n-------------------------\n".join(output)

#result = web_search.invoke("What are the recent news of war?")
#print(result)

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text content from a given URL for deeper reading.
    """
    try:  #Websites may fail → avoid crashing program
        resp = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}  #Some websites block bots. This makes request look like browser.
        )

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)[:3000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
res = scrape_url.invoke("https://docs.langchain.com/oss/python/langchain/overview?utm_source=chatgpt.com")
print(res)
