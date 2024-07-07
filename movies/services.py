import os
import requests
from requests.auth import HTTPBasicAuth
import urllib3


urllib3.disable_warnings()


class MovieAPIService:
    def __init__(self):
        self.username = os.getenv('MOVIE_API_USERNAME')
        self.password = os.getenv('MOVIE_API_PASSWORD')
        self.auth = HTTPBasicAuth(self.username, self.password)

    def fetch_movies(self, page=1):
        url = f"https://demo.credy.in/api/v1/maya/movies/?page={page}"
        response = self._make_request(url)
        if response:
            return response.json()
        return None

    def _make_request(self, url, retries=3):
        for _ in range(retries):
            try:
                response = requests.get(url, auth=self.auth, timeout=5, verify=False)
                if response.status_code == 200:
                    return response
            except requests.RequestException as e:
                print(f"Request failed: {e}")
        return None
