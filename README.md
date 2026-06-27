# Multi-Agent-AI-Reasearch-System
A multi-agent AI research system built with LangChain and Streamlit. Four specialized agents — Search, Reader, Writer, and Critic — work in sequence to automatically research any topic, scrape relevant sources, draft a report, and review it for quality.

## How It Works
The pipeline runs 4 agents in sequence:

1. **Search Agent** — Queries the web for recent and reliable information on the topic
2. **Reader Agent** — Picks the most relevant URL and scrapes it for deeper content
3. **Writer Chain** — Drafts a structured research report from all gathered data
4. **Critic Chain** — Reviews the report and provides quality feedback

## Tech Stack

- Python
- LangChain
- Streamlit
- OpenAI (LLM)
- Tavily (Web Search)

## Setup & Installation
1. Clone the repository
```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
```
2. Create and activate virtual environment
```bash
   python -m venv .venv
   .venv\Scripts\activate
```
3. Install dependencies
```bash
   pip install -r requirements.txt
```
4. Add your API keys in a `.env` file
   OPENAI_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here

5. Run the app
```bash
   streamlit run app.py
```
## Live Demo

[View the deployed app](https://your-app-link.streamlit.app)

## Author
Made by Prashasthi-18
