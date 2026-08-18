# Research Agent

Research Agent is a LangChain-powered system that turns a research question into a sourced report and an independent critique. It combines live web search, web-page extraction, report writing, and quality review in a Streamlit workspace.

## What It Does

The system runs a four-stage pipeline:

1. **Search**: Uses Tavily to find recent and relevant web sources.
2. **Read**: Selects a relevant URL and extracts its main content.
3. **Write**: Combines the search notes and scraped content into a structured report.
4. **Critique**: Reviews the report and returns a score, strengths, areas to improve, and a verdict.

The Streamlit interface provides:

- A dark research workspace for submitting questions
- Preset research prompts
- Live pipeline status and a detailed session trace
- Report, source, and scraped-content views
- A visible critic report
- Markdown report download

## Project Structure

```text
Research Agent/
├── app.py                  # Streamlit user interface
├── main.py                 # Command-line pipeline entry point
├── requirements.txt        # Python dependencies
└── src/
    ├── agents/
    │   └── agents.py       # Search, reader, writer, and critic definitions
    ├── pipelines/
    │   └── pipeline.py     # Four-stage research orchestration
    └── tools/
        └── tools.py        # Tavily search and web scraping tools
```

## Requirements

- Python 3.10 or newer
- A Tavily API key
- An Azure OpenAI deployment configured for `AzureChatOpenAI`

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the project packages:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root. The application loads environment variables with `python-dotenv`.

```env
TAVILY_API_KEY=your_tavily_api_key
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

The Azure deployment name is configured in `src/agents/agents.py` as `gpt-41-mini`. Change it there if your Azure OpenAI deployment uses a different name.

Get a Tavily API key from [tavily.com](https://tavily.com). Azure OpenAI credentials and deployment access are provided through your Azure account.

## Run the Streamlit Application

Start the research workspace with:

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, normally `http://localhost:8501`. Enter a question, choose **Begin research**, and wait for the four pipeline stages to complete.

## Run from the Command Line

`main.py` runs the pipeline with the example topic defined in that file:

```bash
python main.py
```

The command prints search results, scraped content, the generated report, and the critic report to the terminal.

## Use the Tools Directly

The tools are LangChain tools and can be invoked programmatically:

```python
from src.tools.tools import scrape_url, web_search

search_results = web_search.invoke({"query": "your research question"})
print(search_results)

page_content = scrape_url.invoke({"url": "https://example.com"})
print(page_content)
```

## Validation

Compile the Streamlit entry point to check for Python syntax errors:

```bash
python -m py_compile app.py
```

## Dependencies

- `langchain` and `langchain-core` for agent and chain orchestration
- `langchain-openai` for Azure OpenAI integration
- `streamlit` for the research interface
- `tavily-python` for web search
- `trafilatura`, `readability-lxml`, and `beautifulsoup4` for content extraction
- `requests` and `lxml` for HTTP and HTML handling
- `python-dotenv` for local configuration

## License

MIT

## Contributing

Contributions are welcome. Please open an issue to discuss a change before submitting a pull request.
