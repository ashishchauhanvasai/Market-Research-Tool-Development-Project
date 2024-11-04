import requests
from tavily import TavilyClient
import json
import pandas as pd 
import os
from groq import Groq
import streamlit as st

# API Keys (replace with your actual API keys)
TAVILY_API_KEY = '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'
SERPER_API_KEY = '4a97c465520ed029175a5db6f23b3a75238d03cd'
GROQ_API_KEY = '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'  # Replace with your actual Groq API key
os.environ['GROQ_API_KEY'] = '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'

# Initialize Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

class MarketResearchAgent:
    def __init__(self, industry=None, company=None, specific_market=None):
        self.industry = industry if industry else "Retail"
        self.company = company if company else "Reliance Digital"
        self.specific_market = specific_market if specific_market else "Customer Satisfaction"

    def search_tavily_market(self):
        query = f"Market Research in {self.industry} industry for {self.company} Company focusing on {self.specific_market}"
        response = tavily_client.search(query, search_depth="advanced", max_results=10)
        results = []
        for item in response.get("results", []):
            if item['score'] > 0.9:
                result = {
                    "content": item['content'],
                    "link": item['url']               
                }
                results.append(result)
        return results
    
    def search_tavily_competitor(self):
        query = f"Competitor Analysis in {self.industry} industry for {self.company} Company focusing on {self.specific_market}"
        response = tavily_client.search(query, search_depth="advanced")
        results = []
        for item in response.get("results", []):
            if item['score'] > 0.9:
                result = {
                    "content": item['content'],
                    "link": item['url']
                }
                results.append(result)
        return results
    
    def search_tavily_ml(self):
        query = f"AI/ML Trends in {self.industry} industry for {self.company} Company focusing on {self.specific_market}"
        response = tavily_client.search(query, search_depth="advanced")
        results = []
        for item in response.get("results", []):
            if item['score'] > 0.9:
                result = {
                    "content": item['content'],
                    "link": item['url']
                }
                results.append(result)
        return results
    
    def search_serper(self, query):
        """Search for competitor analysis using Serper's API."""
        url = "https://google.serper.dev/search"
        headers = {'X-API-KEY': SERPER_API_KEY,'Content-Type': 'application/json'}
        # query = f"Competitor analysis in {self.industry} industry for {self.company} Company"
        payload=json.dumps({"q": query,"gl":"in"})
        response = requests.request("POST",url,headers=headers, data=payload).json()
        results=[]
        for item in response.get("organic", []):
            result={
                "title":item['title'],
                "link":item['link'],
                "snippet":item['snippet']
            }
            results.append(result)
        return results

# Modify perform_search to return the path of the generated CSV file
def perform_search(self):
    # Define queries for Serper API
    market_query = f"Market trends in {self.industry} industry for {self.company}"
    competitor_query = f"Competitor analysis in {self.industry} industry for {self.company}"
    ai_ml_query = f"AI and ML trends in {self.industry} industry for {self.company}"

    # Collecting search results from Tavily API
    market_trends = self.search_tavily_market()
    competitor_analysis = self.search_tavily_competitor()
    ai_ml_trends = self.search_tavily_ml()

    # Collecting search results from Serper API
    market_trends_serper = self.search_serper(market_query)
    competitor_analysis_serper = self.search_serper(competitor_query)
    ai_ml_trends_serper = self.search_serper(ai_ml_query)

    # Combining Tavily API results into a single text
    combined_text_tavily = (
        "Market Trends (Tavily):\n" + "\n".join([item["content"] for item in market_trends]) + "\n\n" +
        "Competitor Analysis (Tavily):\n" + "\n".join([item["content"] for item in competitor_analysis]) + "\n\n" +
        "AI/ML Trends (Tavily):\n" + "\n".join([item["content"] for item in ai_ml_trends])
    )

    # Creating DataFrame for Serper results
    serper_data = {
        "title": [item['title'] for item in market_trends_serper + competitor_analysis_serper + ai_ml_trends_serper],
        "snippet": [item['snippet'] for item in market_trends_serper + competitor_analysis_serper + ai_ml_trends_serper],
        "link": [item['link'] for item in market_trends_serper + competitor_analysis_serper + ai_ml_trends_serper]
    }
    serper_df = pd.DataFrame(serper_data)

    # Save the DataFrame to a CSV file
    csv_path = "market_research.csv"
    serper_df.to_csv(csv_path, index=False)

    return combined_text_tavily, csv_path

# Update main to display the CSV file
def main():
    st.title("Market Research & AI Use Case Generator")
    st.write("This application conducts market research and generates AI/ML use cases for specific industries and companies.")
    
    # User input fields for industry, company, and market focus
    industry = st.text_input("Industry", value="Retail")
    company = st.text_input("Company Name", value="Reliance Digital")
    specific_market = st.text_input("Specific Market Focus Area", value="Customer Satisfaction")
    
    if st.button("Run Market Research"):
        # Instantiate and run the Market Research Agent
        market_agent = MarketResearchAgent(industry=industry, company=company, specific_market=specific_market)
        with st.spinner("Conducting market research..."):
            research_output, csv_path = market_agent.perform_search()
        st.subheader("Market Research Output")
        st.write(research_output)
        
        # Display the CSV file generated
        st.subheader("Market Research Data (from CSV)")
        st.write(pd.read_csv(csv_path))
    
        # Generate use cases based on the market research output
        use_case_agent = UseCaseGenerationAgent(research_output=research_output, emphasis="Customer Experience")
        with st.spinner("Generating use cases..."):
            use_case_output = use_case_agent.generate_use_cases()
        st.subheader("Generated Use Cases")
        st.write("\n\n".join(use_case_output))
        
        # Resource Asset Collection based on generated use cases
        resource_agent = ResourceAssetCollectionAgent()
        with st.spinner("Collecting dataset resources..."):
            resource_agent.curate_resources()
        st.success("Resource links saved to Resource_Links.csv")
        st.subheader("Resource Links")
        st.write(pd.read_csv("Resource_Links.csv"))

if __name__ == "__main__":
    main()
