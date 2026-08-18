# Research Agent

An AI-powered research agent built with LangChain that leverages web search and content scraping capabilities to gather and process information from the internet.

## Features

- **Web Search**: Search the web using Tavily Search API for recent and reliable information
- **URL Scraping**: Extract and clean main content from web pages using multiple extraction methods (trafilatura, readability, BeautifulSoup)
- **LangChain Integration**: Built on top of LangChain framework for extensible AI agent capabilities
- **Error Handling**: Robust error handling for network and parsing failures

## Project Structure

```
Research Agent/
├── app.py                  # Streamlit application (WIP)
├── main.py                 # Entry point for testing tools
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore patterns
├── .env.example           # Environment variables template
└── src/
    ├── __init__.py
    ├── agents/
    │   ├── __init__.py
    │   └── agents.py       # Agent definitions (WIP)
    ├── pipelines/
    │   ├── __init__.py
    │   └── pipeline.py     # Pipeline orchestration (WIP)
    └── tools/
        ├── __init__.py
        └── tools.py        # Tool implementations (web_search, scrape_url)
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Research Agent"
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create a .env file with:
TAVILY_API_KEY=your_tavily_api_key_here
```

## Usage

### Basic Tool Testing

Run the example in `main.py`:
```bash
python main.py
```

This will scrape content from a URL and print the extracted text.

### Using Tools Programmatically

```python
from src.tools.tools import web_search, scrape_url

# Search the web
results = web_search.invoke({"query": "your search query"})
print(results)

# Scrape a URL
content = scrape_url.invoke({"url": "https://example.com"})
print(content)
```

## Dependencies

- **langchain** (0.2.0+) - AI framework for building with LLMs
- **tavily-python** (0.3.0+) - Web search API
- **beautifulsoup4** (4.12.0+) - HTML parsing
- **readability-lxml** - Content extraction
- **trafilatura** - Main content extraction
- **requests** (2.31.0+) - HTTP library
- **python-dotenv** (1.0.0+) - Environment variable management
- **rich** (13.7.0+) - Pretty terminal output

## API Keys Required

- **Tavily API Key**: Get one at [https://tavily.com](https://tavily.com)

## Roadmap

- [ ] Complete agent implementations in `src/agents/agents.py`
- [ ] Implement pipeline orchestration in `src/pipelines/pipeline.py`
- [ ] Build Streamlit UI in `app.py`
- [ ] Add additional tools (PDF scraping, data processing, etc.)
- [ ] Add unit tests
- [ ] Add logging and monitoring

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
