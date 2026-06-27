from langchain.tools import tool
from langchain_tavily import TavilySearch

from bs4 import BeautifulSoup
from dotenv import load_dotenv

import requests
import streamlit as st
import os

# Load local .env (works locally)
load_dotenv()


# Read API key
try:
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except Exception:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize Tavily Search
tavily = TavilySearch(
    api_key=TAVILY_API_KEY,
    max_results=5
)


@tool
def web_search(query: str) -> str:
    """
    Search for recent and reliable information.
    Returns titles, URLs and snippets.
    """

    try:
        results = tavily.invoke(query)

        output = []

        for r in results["results"]:
            output.append(
                f"Title: {r['title']}\n"
                f"URL: {r['url']}\n"
                f"Snippet: {r['content'][:300]}"
            )

        return "\n\n-----------------------------\n\n".join(output)

    except Exception as e:
        return f"Search Error: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text from a webpage.
    """

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text[:3000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"