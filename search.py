import requests


class Brave:
    """
    Interact with the Brave Search API.
    """

    def __init__(self, api_key):
        """
        Args:
          api_key (str): Your Brave Search API key.
        """
        self.api_key = api_key
        self.params = {"count": 2, "country": "IN"}
        self.headers = {"X-Subscription-Token": api_key}
        self.base_url = "https://api.search.brave.com/res/v1/"

    def search(self, query, **kwargs):
        """
        Performs a general search query using the Brave Search API.

        Args: query (str): The search query to be executed.
        """

        url = self.base_url + "web/search"
        self.params.update({"q": query, **kwargs})
        
        try:
            response = requests.get(url, params=self.params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error performing search: {e}")

    def news(self, query, **kwargs):
        """
        Performs a news search using the Brave Search API.

        Args: query (str): The news search query to be executed.
        """
        url = self.base_url + "news/search"
        self.params.update({"q": query, **kwargs})

        try:
            response = requests.get(url, params=self.params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching news: {e}")
    
    def videos(self, query, **kwargs):
        """
        Performs a news search using the Brave Search API.

        Args: query (str): The video search to be executed.
        """
        url = self.base_url + "videos/search"
        self.params.update({"q": query, **kwargs})

        try:
            response = requests.get(url, params=self.params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error retrieving videos: {e}")
