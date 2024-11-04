import requests
from tavily import TavilyClient
import requests
import json
from exa_py import Exa
import torch
from transformers import pipeline

# API Keys (replace with your actual API keys)
TAVILY_API_KEY = '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'
EXA_API_KEY = 'f386cd21-0912-4236-ade1-b1cdc5d16803'
SERPER_API_KEY = '72ee7556bc02b61b1df8f1bd6e28b4154c66e51a'

# Initialize Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

class MarketResearchAgent:
    def __init__(self, industry=None, company=None, specific_market=None):
        # Set default values if inputs are left blank
        self.industry = industry if industry else "Retail"
        self.company = company if company else "Reliance Digital"
        self.specific_market = specific_market if specific_market else "Customer Satisfaction"
        # self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def search_tavily_market(self):
        """Search for Market trends using Tavily's API."""
        query = f"Market Research  in {self.industry} industry for {self.company} Company focusing on {self.specific_market}"
        response = tavily_client.search(query, search_depth="advanced",max_results=10)
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
        """Search for Comeptitor Analysis using Tavily's API."""
        query = f"Comeptitor Analysis in {self.industry} industry for {self.company} Company focusing on {self.specific_market}"
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
        """Search for Comeptitor Analysis using Tavily's API."""
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

    # def search_exa_ml(self):
    #     """Search for AI/ML Trends using Exa's API."""
    #     exa = Exa(api_key=EXA_API_KEY)
    #     query = f"AI and ML trends in {self.industry} industry for {self.company} Company focusing on {self.specific_market}"
    #     response = exa.search_and_contents(query,type='neural',use_autoprompt=True,num_results=10,text=True,category='company',summary=True)
    #     results=[]
    #     for item in response.results:
    #         result={
    #             "text":item.text,
    #             "link":item.url,
    #         }
    #         results.append(result)
    #     return results
    
    # def search_exa_competitor(self):
    #     """Search for AI/ML Trends using Exa's API."""
    #     exa = Exa(api_key=EXA_API_KEY)
    #     query = f"Competitors Analysis and Strategies in {self.industry} industry for {self.company} Company focusing on {self.specific_market}"
    #     response = exa.search_and_contents(query,type='neural',use_autoprompt=True,num_results=10,text=True,category='company',summary=True)
    #     results=[]
    #     for item in response.results:
    #         result={
    #             "text":item.text,
    #             "link":item.url,
    #         }
    #         results.append(result)
    #     return results
    
    # def search_exa_market(self):
    #     """Search for Market Research Trends using Exa's API."""
    #     exa = Exa(api_key=EXA_API_KEY)
    #     query = f"Market Research Trends in {self.industry} industry for {self.company} Company focusing on {self.specific_market}"
    #     response = exa.search_and_contents(query,type='neural',use_autoprompt=True,num_results=10,text=True,category='company',summary=True)
    #     results=[]
    #     for item in response.results:
    #         result={
    #             "text":item.text,
    #             "link":item.url,
    #         }
    #         results.append(result)
    #     return results
        
    # def search_serper(self):
    #     """Search for competitor analysis using Serper's API."""
    #     url = "https://google.serper.dev/search"
    #     headers = {'X-API-KEY': SERPER_API_KEY,'Content-Type': 'application/json'}
    #     query = f"Competitor analysis in {self.industry} industry for {self.company} Company"
    #     payload=json.dumps({"q": query,"gl":"in"})
    #     response = requests.request("POST",url,headers=headers, data=payload)
    #     results=[]
    #     for item in response.get("organic", []):
    #         result={
    #             "title":item['title'],
    #             "link":item['link'],
    #             "snippet":item['snippet'],
    #             "sitelinks":item['sitelinks']
    #         }
    #         results.append(result)
    #     return results

    def perform_search(self):
        """Perform searches and combine results."""
        # Collecting search results from each API
        market_trends = self.search_tavily_market()
        competitor_analysis = self.search_tavily_competitor()
        ai_ml_trends = self.search_tavily_ml()
        
        # Extracting and cleaning content from each result
        def clean_text(text):
            return " ".join(text.split())

        market_trends_text = "\n".join([clean_text(item["content"]) for item in market_trends])
        competitor_analysis_text = "\n".join([clean_text(item["content"]) for item in competitor_analysis])
        ai_ml_trends_text = "\n".join([clean_text(item["content"]) for item in ai_ml_trends])
        
        # Combining all results into a single text
        combined_text = f"Market Trends:\n{market_trends_text}\n\n"
        combined_text += f"Competitor Analysis:\n{competitor_analysis_text}\n\n"
        combined_text += f"AI/ML Trends:\n{ai_ml_trends_text}"
        
        return combined_text


    def run(self):
        combined_text = self.perform_search()
        if not combined_text.strip():
            return "No data found for the given industry and company."
        # Summarize the combined text
        # summarized_output = self.summarize_text(combined_text)
        # Display or return the combined text
        return combined_text

# Example usage
if __name__ == "__main__":
    # Get user input or use defaults
    industry = input("Enter the industry to search (e.g., Retail, Healthcare) [default: Retail]: ") or "Retail"
    company = input("Enter the company name (e.g., Example Inc.) [default: Example Retail Inc.]: ") or "Reliance Digital"
    specific_market = input("Enter any specific market focus area (e.g., Customer Experience) [default: Customer Satisfaction]: ") or "Customer Satisfaction"

    # Instantiate and run the agent
    market_agent = MarketResearchAgent(industry=industry, company=company, specific_market=specific_market)
    research_output = market_agent.run()
    print("Market Research Output:\n", research_output)
