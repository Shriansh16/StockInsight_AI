# StockInsight_AI

## Overview
This project is a fully automated financial report generation system utilizing **AutoGen** and **Streamlit**. The system leverages multiple AI agents to collect, analyze, and generate financial reports based on real-time stock data and financial metrics.

## Features
- **Stock Data Retrieval**: Retrieves stock prices, performance data, and financial ratios.
- **News Analysis**: Collects and summarizes market news headlines for each stock.
- **Report Generation**: Creates comprehensive financial reports, including comparative analysis.
- **Automated Review System**: Multiple AI-based reviewers ensure content quality, accuracy, consistency, and legal compliance.
- **Streamlit UI**: Provides a simple user interface for input and analysis initiation.

## Architecture
The system employs multiple AI agents, each with a specific role:

### **Agents**
1. **Financial Assistant**: Retrieves stock data and fundamental ratios.
2. **Researcher**: Collects and summarizes relevant market news headlines.
3. **Writer**: Generates the final financial report in markdown format.
4. **Export Assistant**: Handles the export of the final report.
5. **Critic**: Reviews the report for overall quality.
6. **Legal Reviewer**: Ensures legal compliance.
7. **Consistency Reviewer**: Checks data consistency across the report.
8. **Text Alignment Reviewer**: Ensures numerical data aligns with the textual analysis.
9. **Completion Reviewer**: Verifies that the report contains all necessary elements.
10. **Meta Reviewer**: Aggregates feedback from all reviewers and provides final suggestions.

## How It Works
1. **User Input**:
   - The user provides the stock tickers for analysis through a Streamlit text input field.
   - Clicks the **Start Analysis** button to begin processing.
2. **Data Collection**:
   - The system fetches stock prices, performance metrics, and financial ratios.
   - News headlines related to the stocks are retrieved.
3. **Report Generation**:
   - The Writer agent compiles all collected information into a structured financial report.
4. **Review Process**:
   - The generated report undergoes multiple review stages to ensure quality, accuracy, and completeness.
5. **Final Report Output**:
   - The final reviewed report is ready for presentation/export.



## Output
- A **comprehensive financial report** in markdown format.
- Includes stock data, comparative tables, fundamental ratios, news analysis, and potential future scenarios.



