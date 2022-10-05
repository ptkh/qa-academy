import allure
from framework.api.status_codes import StatusCode
from framework.models.user import User
from framework.models.post import Post
from tests.testData.testData import TestData


class TestAPI(object):
    def test_api(self, api):
        with allure.step("Send GET Request to get all posts (/posts)."):
            response = api.get_posts()
            assert api.get_status_code(response) == StatusCode.OK, f"Response status code {response.status_code}"
            assert api.response_body_is_json(response), "Response format is not JSON"
            assert api.is_sorted_asc_by_id(response), "Response is not sorted ascending by id"

        with allure.step("Send GET request to get post with id=99 (/posts/99)."):
            response = api.get_post_by_id(TestData.existent_post_id)
            assert api.get_status_code(response) == StatusCode.OK, f"Response status code {response.status_code}"
            post_from_response = Post(**response.json())
            assert post_from_response.userId == TestData.existent_post_user_id \
                   and post_from_response.id == TestData.existent_post_id \
                   and post_from_response.title != '' \
                   and post_from_response.body != '', f"Post information is not correct:\n{post_from_response}"

        with allure.step("Send GET request to get post with id=150 (/posts/150)."):
            response = api.get_post_by_id(TestData.absent_post_id)
            assert api.get_status_code(response) == StatusCode.NOT_FOUND, f"Response status code {response.status_code}"
            assert response.json() == {}, f"Response is not empty:\n{response.json()}"

        post_from_test_data = Post(**TestData.post)
        with allure.step("Send POST request to create post with userId=1 and random body and random title (/posts)."):
            response = api.create_post(post_from_test_data)
            assert api.get_status_code(response) == StatusCode.CREATED, f"Response status code {response.status_code}"
            post_from_response = Post(**response.json())
            assert post_from_response == post_from_test_data, "Post from response doesn't match post from test data"

        user_from_test_data = User(**TestData.user)
        with allure.step("Send GET request to get users (/users)."):
            response = api.get_users()
            assert api.get_status_code(response) == StatusCode.OK, f"Response status code {response.status_code}"
            assert api.response_body_is_json(response), "Response format is not JSON"
            user_from_response = api.get_user_from_list_by_param(response, TestData.ID, TestData.user_id)
            assert user_from_response == user_from_test_data, "User from response doesn't match user from test data"

        user_from_previous_response = user_from_response
        with allure.step("Send GET request to get user with id=5 (/users/5)."):
            response = api.get_user_by_id(TestData.user_id)
            assert api.get_status_code(response) == StatusCode.OK, f"Response status code {response.status_code}"
            user_from_response = User(**response.json())
            assert user_from_response == user_from_previous_response, "User from response doesn't match user from test data"
