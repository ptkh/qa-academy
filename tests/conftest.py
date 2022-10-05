import pytest
from tests.config.urls import Urls
from tests.api.api_requests import CustomAPI


@pytest.fixture
def api():
    return CustomAPI(base_url=Urls.TEST_URL)

