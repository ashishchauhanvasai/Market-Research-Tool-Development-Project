import requests
from tavily import TavilyClient
import json
import pandas as pd 
import os
from groq import Groq


# API Keys (replace with your actual API keys)
TAVILY_API_KEY = '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'
SERPER_API_KEY = '72ee7556bc02b61b1df8f1bd6e28b4154c66e51a'
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

        # Combining Serper API results into a single text
        # combined_text_serper = (
        #     "Market Trends (Serper):\n" + "\n".join([f"{item['snippet']} (Link: {item['link']})" for item in market_trends_serper]) + "\n\n" +
        #     "Competitor Analysis (Serper):\n" + "\n".join([f"{item['snippet']} (Link: {item['link']})" for item in competitor_analysis_serper]) + "\n\n" +
        #     "AI/ML Trends (Serper):\n" + "\n".join([f"{item['snippet']} (Link: {item['link']})" for item in ai_ml_trends_serper])
        # )
         # Create a DataFrame for Serper results
        serper_data = {
            "title": [item['title'] for item in market_trends_serper + competitor_analysis_serper + ai_ml_trends_serper],
            "snippet": [item['snippet'] for item in market_trends_serper + competitor_analysis_serper + ai_ml_trends_serper],
            "link": [item['link'] for item in market_trends_serper + competitor_analysis_serper + ai_ml_trends_serper]
        }
        serper_df = pd.DataFrame(serper_data)

        # Save the DataFrame to a CSV file
        serper_df.to_csv("market_research.csv", index=False)

        return combined_text_tavily

    def run(self):
        combined_text_tavily = self.perform_search()
        if not combined_text_tavily.strip() :
            return "No data found for the given industry and company."
        
        # Display the combined text from both APIs
        print("Tavily Output:\n", combined_text_tavily)
        print("\n" + "-"*50 + "\n")

        return combined_text_tavily

class UseCaseGenerationAgent:
    def __init__(self, research_output, emphasis=None):
        self.research_output = research_output
        self.emphasis = emphasis
        self.client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

    def generate_use_cases(self):
        prompt = (
        f"Based on the following Market research output, propose relevant use caseshere the company can leverage GenAI, LLMs, and"
        f"ML technologies along with their applications and cross-functional benefits. "
        f"For each use case, provide the following details:\n"
        f"1. Use Case: A brief description of the use case.\n"
        f"2. Application: How the use case can be applied in the company.\n"
        f"3. Cross-Functional Benefits: The benefits of the use case across different functions of the company.\n\n"
        f"Market Research Output:\n{self.research_output}\n\n"
        )
        
        # Payload for the Groq API
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.2-90b-vision-preview",
        )

        if chat_completion:
            use_cases = [choice.message.content.strip() for choice in chat_completion.choices]
            with open("use_cases.txt", "w") as file:
                for use_case in use_cases:
                    file.write(use_case + "\n\n")
            return use_cases
        else:
            print("Error in generating use cases from Groq API")
            return ["Error in generating use cases from Groq API"]

class ResourceAssetCollectionAgent:
    def __init__(self, use_case_file="use_cases.txt"):
        self.use_case_file = use_case_file
        self.dataset_links = []
        self.use_cases = self.load_use_cases()

    def load_use_cases(self):
        """
        Loads use cases from the specified file.
        """
        use_cases = []
        try:
            with open(self.use_case_file, "r") as file:
                # Read lines and extract each use case title from the file
                for line in file:
                    if line.startswith("**Use Case"):  # Extract only use case titles
                        title = line.split(": ")[1].strip()
                        use_cases.append(title)
        except FileNotFoundError:
            print(f"Error: {self.use_case_file} not found.")
        return use_cases

    def search_datasets_serper(self, query):
        """
        Searches for datasets using the Serper API with the provided use case title as the query.
        """
        url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        
        # Define payload with use case title as query
        payload = json.dumps({
            "q": query + " dataset",
            "gl": "us"
        })
        
        response = requests.post(url, headers=headers, data=payload).json()
        
        # Process search results to extract dataset links
        results = []
        for item in response.get("organic", []):
            results.append({
                "title": item['title'],
                "snippet": item['snippet'],
                "link": item['link']
            })
        return results

    def collect_datasets(self):
        """
        Searches for datasets based on each use case title.
        """
        for use_case in self.use_cases:
            # Search datasets for each use case title using Serper
            results = self.search_datasets_serper(use_case)
            for result in results:
                self.dataset_links.append({
                    "use_case": use_case,
                    "title": result["title"],
                    "snippet": result["snippet"],
                    "link": result["link"]
                })

    def save_to_csv(self, filename="Resource_Links.csv"):
        """
        Save collected dataset links and use cases to a CSV file.
        """
        df = pd.DataFrame(self.dataset_links)
        df.to_csv(filename, index=False)

    def curate_resources(self):
        """
        Run dataset search and save results to CSV.
        """
        self.collect_datasets()
        self.save_to_csv()


# Example usage
if __name__ == "__main__":
    industry = input("Enter the industry to search (e.g., Retail, Healthcare) [default: Retail]: ") or "Retail"
    company = input("Enter the company name (e.g., Example Inc.) [default: Reliance Digital]: ") or "Reliance Digital"
    specific_market = input("Enter any specific market focus area (e.g., Customer Experience) [default: Customer Satisfaction]: ") or "Customer Satisfaction"

    # Instantiate and run the market research agent
    market_agent = MarketResearchAgent(industry=industry, company=company, specific_market=specific_market)
    research_output = market_agent.run()
    print("Market Research Output:\n", research_output)

    # Generate use cases based on the market research output
    use_case_agent = UseCaseGenerationAgent(research_output=research_output, emphasis="Customer Experience")
    use_case_output = use_case_agent.generate_use_cases()
    print("Generated Use Cases:", use_case_output)

    # Resource Asset Collection based on generated use cases from use_cases.txt
    resource_agent = ResourceAssetCollectionAgent(use_case_file="use_cases.txt")
    resource_agent.curate_resources()
    print("Resource links saved to Resource_Links.csv")
