import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="📈 Financial AI Analyst", layout="centered")

st.title("💼 Financial AI Analyst")
st.markdown("Ask about any stock ticker to get **analyst recommendations** and the **latest news**.")

ticker = st.text_input("Enter a Stock Ticker (e.g., `NVDA`, `AAPL`, `TSLA`):", value="NVDA")

if st.button("🔍 Analyze Stock") and ticker.strip() != "":
    with st.spinner("Thinking... fetching financial data and news..."):
        web_search_agent = Agent(
            name="Web Search Agent",
            role="Search the web for the information",
            model=Groq(id="llama3-70b-8192"),
            tools=[DuckDuckGo()],
            instructions=["Always include sources"],
            show_tools_calls=True,
            markdown=True
        )

        finance_agent = Agent(
            name="Finance AI Agent",
            model=Groq(id="llama3-70b-8192"),
            tools=[
                YFinanceTools(
                    stock_price=True,
                    analyst_recommendations=True,
                    stock_fundamentals=True,
                    company_news=True,
                )
            ],
            instructions=["Use tables to display the data"],
            show_tool_calls=True,
            markdown=True
        )

        multi_ai_agent = Agent(
            name="Multi AI Agent",
            model=Groq(id="llama3-70b-8192"),
            team=[web_search_agent, finance_agent],
            instructions=[
                "Always include sources",
                "Use table to display the data"
            ],
            show_tool_calls=True,
            markdown=True
        )

        query = f"Summarize analyst recommendations and share the latest news for {ticker.upper()}"
        try:
            response = multi_ai_agent.run(query)
            st.markdown(response)
        except Exception as e:
            st.error(f"❌ Something went wrong:\n{e}")

st.markdown("---")
st.markdown("🔗 Powered by `Groq` + `PHI` + `Streamlit`")
