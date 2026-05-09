# StockInsight AI

A multi-agent financial analysis tool that uses [Microsoft AutoGen](https://github.com/microsoft/autogen) and [Streamlit](https://streamlit.io) to automatically fetch stock data, retrieve market news, and generate a comprehensive written financial report.

---

## Features

- Retrieves live stock prices, P/E ratios, dividends, ROE, and more via `yfinance`
- Fetches recent news headlines for each stock from public sources
- Generates a normalized price performance chart
- Produces a full markdown financial report with tables, figures, and future scenario analysis
- Multi-agent review pipeline (legal, consistency, text-alignment, completion, meta reviewers)

---

## Project Structure

```
StockInsight_AI/
├── app.py                  # Streamlit entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .env                    # Your local secrets (never committed)
├── .gitignore
├── README.md
├── outputs/                # Runtime-generated charts and scripts (gitignored)
│   └── .gitkeep
└── src/                    # Core application package
    ├── __init__.py
    ├── config.py           # LLM configuration (loaded from .env)
    ├── agents.py           # AutoGen agent factory functions
    ├── tasks.py            # Task prompt definitions
    └── review.py           # Multi-agent review chat setup
```

---

## Prerequisites

- Python 3.10 or higher
- An [OpenAI API key](https://platform.openai.com/api-keys)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/StockInsight_AI.git
cd StockInsight_AI
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and set your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

Optionally override the model (default: `gpt-3.5-turbo`):

```
OPENAI_MODEL=gpt-4o
```

---

## Running the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

Enter one or more stock tickers (e.g. `AAPL, MSFT, GOOGL`) and click **Start Analysis**.

---

## How It Works

1. **Financial Agent** — fetches stock prices, ratios, and generates a normalized price chart saved to `outputs/normalized_prices.png`.
2. **Research Agent** — retrieves relevant news headlines for each stock.
3. **Writer + Critic** — the Writer drafts a full markdown financial report; the Critic reviews and refines it.
4. **Review pipeline** (`src/review.py`) — optional multi-agent review pass (legal, consistency, text alignment, completion, meta) that can be wired into the critic's nested chat.

---

## Agents

StockInsight AI uses **9 specialized AutoGen agents** organized into three stages.

### Stage 1 — Data Collection

| Agent | Type | Role |
|---|---|---|
| **Financial Assistant** | `AssistantAgent` | Fetches 6-month historical prices, fundamental ratios (P/E, Forward P/E, Dividends, Price-to-Book, Debt/Equity, ROE) via `yfinance`, and saves the normalized price chart |
| **Researcher** | `AssistantAgent` | Retrieves up-to-date market news headlines for each stock from Google News RSS (no API key required) |
| **User Proxy Auto** | `UserProxyAgent` | Executes all Python code produced by the data agents inside the `outputs/` directory. Runs fully autonomously (`human_input_mode="NEVER"`) |

### Stage 2 — Report Writing

| Agent | Type | Role |
|---|---|---|
| **Writer** | `AssistantAgent` | Produces the full markdown financial report — stock overview, fundamentals table, price performance narrative, comparative analysis, news summary, and future scenarios |
| **Critic** | `AssistantAgent` | Reviews the Writer's draft and provides constructive feedback to improve quality. Drives the writing loop (max 2 turns) |

### Stage 3 — Review Pipeline *(optional, via `src/review.py`)*

These reviewers can be wired into the Critic's nested chat for deeper quality control:

| Agent | Type | Role |
|---|---|---|
| **Legal Reviewer** | `AssistantAgent` | Checks the report for legal compliance and flags any potentially misleading financial statements |
| **Consistency Reviewer** | `AssistantAgent` | Ensures numbers and claims are consistent throughout the report; resolves contradictions using the underlying data |
| **Text Alignment Reviewer** | `AssistantAgent` | Verifies that written descriptions accurately match the numerical data — no text should contradict the figures |
| **Completion Reviewer** | `AssistantAgent` | Validates the report contains all required elements: news summary, ratio descriptions, future scenarios, a table, and at least one figure reference |
| **Meta Reviewer** | `AssistantAgent` | Aggregates feedback from all reviewers above and produces a single final recommendation for the Writer |

### Agent Communication Flow

```
User Input (tickers)
        │
        ▼
[User Proxy Auto] ◄──► [Financial Assistant]   ← Stage 1a: prices & ratios
        │
        ▼
[User Proxy Auto] ◄──► [Researcher]             ← Stage 1b: news headlines
        │
        ▼
     [Critic]     ◄──► [Writer]                 ← Stage 2: report (2 turns)
        │
        ▼  (optional nested chat)
[Legal / Consistency / Text Alignment /
 Completion Reviewers] ──► [Meta Reviewer]      ← Stage 3: quality review
        │
        ▼
   Final Report (displayed + downloadable as .md)
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | **Required.** Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | Model used by all agents |

---

## License

MIT
