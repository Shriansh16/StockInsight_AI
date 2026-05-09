import os
import sys

# Force UTF-8 encoding for all agent-spawned subprocesses on Windows
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

import streamlit as st
import autogen
from datetime import datetime

from src.agents import (
    create_financial_assistant,
    create_research_assistant,
    create_writer,
    create_critic,
    create_user_proxy_auto,
)
from src.tasks import get_financial_tasks, writing_tasks

OUTPUTS_DIR = "outputs"
CHART_PATH = f"{OUTPUTS_DIR}/normalized_prices.png"


def save_report(report_content: str, tickers: str) -> str:
    """Save the markdown report to outputs/ and return the file path."""
    safe_tickers = tickers.replace(" ", "").replace(",", "_").upper()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUTS_DIR}/report_{safe_tickers}_{timestamp}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_content)
    return filename


def render_results():
    """Render chart, download button, and report from session state."""
    report_content = st.session_state.report_content
    tickers = st.session_state.tickers

    st.success("Analysis complete!")

    col1, col2 = st.columns([6, 1])
    with col1:
        if os.path.exists(CHART_PATH):
            st.image(CHART_PATH, caption="Normalized Price Performance")
        else:
            st.warning(f"Chart not found at `{CHART_PATH}`. It may not have been generated.")
    with col2:
        safe_name = tickers.replace(" ", "").replace(",", "_").upper()
        st.download_button(
            label="⬇ Download Report",
            data=report_content,
            file_name=f"report_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
        )

    st.markdown("---")
    st.markdown(report_content)


def main():
    st.set_page_config(page_title="StockInsight AI", page_icon="📈", layout="wide")
    st.title("📈 StockInsight AI")
    st.caption("Multi-agent financial analysis powered by AutoGen")

    assets = st.text_input(
        "Enter stock tickers to analyse (comma-separated):",
        placeholder="e.g. AAPL, MSFT, GOOGL",
    )
    hit_button = st.button("Start Analysis", type="primary")

    if hit_button and assets.strip():
        # Clear any previous results when a new analysis is started
        st.session_state.report_content = None
        st.session_state.tickers = assets.strip()

        financial_assistant = create_financial_assistant()
        research_assistant = create_research_assistant()
        writer = create_writer()
        critic = create_critic()
        user_proxy_auto = create_user_proxy_auto()

        financial_tasks = get_financial_tasks(assets)

        with st.spinner("Agents working on the analysis — this may take a few minutes..."):
            chat_results = autogen.initiate_chats(
                [
                    {
                        "sender": user_proxy_auto,
                        "recipient": financial_assistant,
                        "message": financial_tasks[0],
                        "silent": False,
                        "summary_method": "reflection_with_llm",
                        "summary_args": {
                            "summary_prompt": (
                                "Return the stock prices of the stocks, their performance "
                                "and all other metrics into a JSON object only. "
                                "Provide the name of all figure files created. "
                                "Provide the full name of each stock."
                            ),
                        },
                        "clear_history": False,
                        "carryover": (
                            "IMPORTANT: You must execute real code using yfinance to fetch actual market data. "
                            "Do NOT generate random or mock data. "
                            "After each code block executes, verify the output contains real numbers (not NaN). "
                            "Confirm the normalized_prices.png file was saved. "
                            "Reply TERMINATE only after all steps are verified."
                        ),
                    },
                    {
                        "sender": user_proxy_auto,
                        "recipient": research_assistant,
                        "message": financial_tasks[1],
                        "silent": False,
                        "summary_method": "reflection_with_llm",
                        "summary_args": {
                            "summary_prompt": (
                                "Provide the news headlines as a paragraph for each stock, "
                                "be precise but do not consider news events that are vague. "
                                "Return the result as a JSON object only."
                            ),
                        },
                        "clear_history": False,
                        "carryover": (
                            "Wait for confirmation of code execution before terminating "
                            "the conversation. Reply TERMINATE when everything is done."
                        ),
                    },
                    {
                        "sender": critic,
                        "recipient": writer,
                        "message": writing_tasks[0],
                        "carryover": (
                            "Use the REAL data values from earlier in this conversation. "
                            "Do NOT embed any images. Do NOT write N/A for values that were provided. "
                            "Include a markdown table of fundamental ratios."
                        ),
                        "max_turns": 2,
                        "summary_method": "last_msg",
                    },
                ]
            )

        report_content = chat_results[-1].chat_history[-1]["content"]

        # Persist results so they survive button/download reruns
        st.session_state.report_content = report_content
        save_report(report_content, assets)

    elif hit_button and not assets.strip():
        st.warning("Please enter at least one ticker symbol.")

    # Always render results if they exist in session state
    if st.session_state.get("report_content"):
        render_results()


if __name__ == "__main__":
    main()
