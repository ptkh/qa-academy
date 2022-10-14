import requests
from framework.models.post import Post
from framework.utils.logger import Logger


class APIRequests:

    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    @staticmethod
    def get_status_code(response):
        return response.status_code

    def get(self, sub_url):
        url = f"{self.base_url}{sub_url}"
        Logger.info(f"Creating get request with url: {url}")
        response = requests.get(url, headers=self.headers)
        Logger.info(f"Response status code: {response.status_code} for get request: \n{url}")
        return response

    def post(self, sub_url, post: Post):
        url = f"{self.base_url}{sub_url}"
        data = {}
        for key, value in post.__dict__.items():
            if key == 'id':
                continue
            data.update({key: value})
        Logger.info(f"Creating post request with url: \n{url}\nRequest body: \n{data}")
        response = requests.post(url, json=data)
        Logger.info(f"Response status code: {response.status_code} for get request: \n{url}")
        return response
    