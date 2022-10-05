from framework.api.api_requests import APIRequests
from framework.models.post import Post
from framework.models.user import User
from framework.utils.logger import Logger
from tests.testData.testData import TestData
import requests


class CustomAPI(APIRequests):
    def get_posts(self):
        Logger.info("get_posts method called")
        return self.get(TestData.POSTS)

    def get_users(self):
        Logger.info("get_users method called")
        return self.get(TestData.USERS)

    def get_post_by_id(self, id_):
        Logger.info("get_post_by_id method called with argument %ds" % id_)
        return self.get(f"{TestData.POSTS}/{id_}")

    def get_user_by_id(self, id_):
        Logger.info("get_user_by_id method called with argument %ds" % id_)
        return self.get(f"{TestData.USERS}/{id_}")

    def get_post_by_userid(self, userid):
        Logger.info("get_post_by_userid method called with argument %ds" % userid)
        return self.get(f"{TestData.POSTS}/?userId={userid}")

    def create_post(self, post: Post):
        Logger.info(f"create_post method called with argument \n{post.__dict__}")
        return self.post(TestData.POSTS, post)

    @staticmethod
    def response_body_is_json(response):
        Logger.info(f"response_body_is_json method called with response {response}")
        try:
            response.json()
            return True
        except requests.exceptions.JSONDecodeError:
            Logger.info(f"Provided response is not in json format. \nResponse: {response}")
            return False

    @staticmethod
    def is_sorted_asc_by_id(response):
        Logger.info(f"is_sorted_asc_by_id method called with response {response}")
        counter = 1
        for item in response.json():
            if item['id'] != counter:
                return False
            counter += 1
        return True

    @staticmethod
    def get_user_from_list_by_param(response, param, value):
        for data in response.json():
            if data[param] == value:
                return User(**data)
