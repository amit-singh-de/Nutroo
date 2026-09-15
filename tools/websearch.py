from tavily import TavilyClient


class WebSearch:
    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str):
        """Perform a web search using the Tavily client."""
        return self.client.search(query)