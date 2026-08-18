from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns titles, url and content"""
    results = tavily.search(query=query, max_results=5)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )

    return "\n----\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """Scrape and extract the main content from a given URL. Returns the cleaned text content of the page."""
    try:
        # Fetch the URL with a timeout
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Try trafilatura first (best for content extraction)
        content = trafilatura.extract(response.text, include_comments=False, include_tables=True)
        
        if content:
            return content.strip()
        
        # Fallback to readability
        doc = Document(response.text)
        content = doc.summary()
        
        if content:
            # Clean up HTML tags
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        
        # Last resort: use BeautifulSoup on the whole page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
        
    except requests.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error scraping URL: {str(e)}"
    
