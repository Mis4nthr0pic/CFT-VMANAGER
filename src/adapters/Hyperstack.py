import src.log as log
import requests

logger = log.get_logger(__name__)

class HyperStack:
    def __init__(self, api_key, base_url="https://infrahub-api.nexgencloud.com/v1/core/"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'api_key': self.api_key,
            'Content-Type': 'application/json'
        }

    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)
        return self.handle_response(response)

    def post(self, endpoint, data):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        return self.handle_response(response)

    def handle_response(self, response):
        if response.status_code in [200, 201]:
            return response.json()
        else:
            response.raise_for_status()
