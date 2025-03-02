import streamlit as st
import autogen
from config import llm_config
from agents import (
    create_financial_assistant, create_research_assistant, create_writer, 
    create_critic, create_user_proxy_auto
)
from tasks import get_financial_tasks, writing_tasks

def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content. 
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''

def main():
    assets = st.text_input("Assets you want to analyze (provide the tickers)?")
    hit_button = st.button('Start analysis')

    if hit_button is True:
        financial_assistant = create_financial_assistant()
        research_assistant = create_research_assistant()
        writer = create_writer()
        critic = create_critic()
        user_proxy_auto = create_user_proxy_auto()

        financial_tasks = get_financial_tasks(assets)

        with st.spinner("Agents working on the analysis...."):
            chat_results = autogen.initiate_chats(
                [
                    {
                        "sender": user_proxy_auto,
                        "recipient": financial_assistant,
                        "message": financial_tasks[0],
                        "silent": False,
                        "summary_method": "reflection_with_llm",
                        "summary_args": {
                            "summary_prompt" : "Return the stock prices of the stocks, their performance and all other metrics"
                            "into a JSON object only. Provide the name of all figure files created. Provide the full name of each stock.",
                                        },
                        "clear_history": False,
                        "carryover": "Wait for confirmation of code execution before terminating the conversation. Verify that the data is not completely composed of NaN values. Reply TERMINATE in the end when everything is done."
                    },
                    {
                        "sender": user_proxy_auto,
                        "recipient": research_assistant,
                        "message": financial_tasks[1],
                        "silent": False,
                        "summary_method": "reflection_with_llm",
                        "summary_args": {
                            "summary_prompt" : "Provide the news headlines as a paragraph for each stock, be precise but do not consider news events that are vague, return the result as a JSON object only.",
                                        },
                        "clear_history": False,
                        "carryover": "Wait for confirmation of code execution before terminating the conversation. Reply TERMINATE in the end when everything is done."
                    },
                    {
                        "sender": critic,
                        "recipient": writer,
                        "message": writing_tasks[0],
                        "carryover": "I want to include a figure and a table of the provided data in the financial report.",
                        "max_turns": 2,
                        "summary_method": "last_msg",
                    }
                ]
            )

        st.image("./coding/normalized_prices.png")
        st.markdown(chat_results[-1].chat_history[-1]["content"])

if __name__ == "__main__":
    main()