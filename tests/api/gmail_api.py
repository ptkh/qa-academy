import allure
from framework.api.api_requests import APIRequests
from framework.utils.logger import Logger
from tests.api.exceptions import MessageNotReceivedException, MessageWaitTimeoutException
from tests.testData.test_data import TestData
import requests
import base64
import re
import time
import datetime


class GmailAPI(APIRequests):
    @property
    def access_token(self):
        with allure.step("Getting access token from refresh token"):
            url = TestData.token_url
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                    "refresh_token": TestData.refresh_token,
                    "client_id": TestData.client_id,
                    "client_secret": TestData.client_secret,
                    "grant_type": "refresh_token"
            }
            Logger.info(f"Sending request to {url} with headers:\n{headers}\nand data:\n{data}")
            response = requests.post(url=url, headers=headers, data=data)
            Logger.info(f"Received response: {response}\n{response.json()}")
            return response.json()["access_token"]

    def __init__(self):
        self.email = None
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {self.access_token}"}
        super().__init__(base_url=TestData.gmail_api_url, headers=headers)

    @property
    def email_headers_list(self):
        with allure.step("Getting email list"):
            Logger.info("Sending request to get email list")
            email_list = self.get(f"/gmail/v1/users/enmatheblack@gmail.com/messages").json()["messages"]
            Logger.info(f"Received response: {email_list}")
            return email_list

    @property
    def number_of_emails(self):
        return len(self.email_headers_list)

    @property
    def email_list(self):
        with allure.step("Getting emails by collected ids"):
            messages = []
            for email in self.email_headers_list:
                Logger.info(f"Sending request to get email: {email}")
                messages.append(self.get(f"/gmail/v1/users/{TestData.email}/messages/{email['id']}").json())
            return messages

    def wait_until_new_email(self):
        with allure.step("Checking email list and waiting until new email is received"):
            email_count = len(self.email_headers_list)
            for i in range(30):
                if len(self.email_headers_list) > email_count:
                    Logger.info(f"New email was received in {i}secs")
                    return
                time.sleep(1)
            raise MessageWaitTimeoutException("New email was not received in 30 seconds")

    def parse_euronews_email(self):
        with allure.step("Parsing email list for euronews email"):
            for email in self.email_list:
                email_dict = {}
                for header in email['payload']['headers']:
                    Logger.info(f"Parsing email header: {header['name']}")
                    if header['name'] == 'Date':
                        email_dict['Date'] = header['value']
                        Logger.info(f"Date saved in dict: {email_dict['Date']}")
                    elif header['name'] == 'From':
                        email_dict['From'] = header['value']
                        Logger.info(f"From saved in dict: {email_dict['From']}")
                    elif header['name'] == 'Subject':
                        email_dict['Subject'] = header['value']
                        Logger.info(f"Subject saved in dict: {email_dict['Subject']}")
                if 'Euronews' in email_dict['From']:
                    Logger.info(f"Current email is from Euronews")
                    current_timestamp = time.time() + time.timezone
                    email_timestamp = time.mktime(datetime.datetime
                                                  .strptime(email_dict['Date'], TestData.time_format).timetuple())
                    if email_timestamp > current_timestamp - 60:
                        Logger.info(f"Current Euronews email was received in last minute at: {email_dict['Date']}")
                        email_dict['data'] = email['payload']['parts'][0]['body']['data']
                        self.email = email_dict
                        return

    @staticmethod
    def decode_html(coded_html_string):
        with allure.step("Decoding email data"):
            return base64.urlsafe_b64decode(coded_html_string).decode('utf-8')

    @staticmethod
    def get_href_from_html(html):
        with allure.step("Parsing html to find confirmation button link"):
            match = re.search(TestData.href_pattern, html)
            if match:
                return match.group(1)

    def confirm_subscription_email_received(self):
        with allure.step("Checking if subscription confirmation email was received"):
            Logger.info("Calling parse_euronews_email method")
            self.parse_euronews_email()
            if 'Euronews' in self.email['From']:
                Logger.info(f"Subscription confirmation email was parsed. Result:\n{self.email}")
                return 'Please Confirm Subscription' in self.email['Subject']
            else:
                Logger.info("Euronews email was not received. Raising exception")
                raise MessageNotReceivedException("Euronews email was not received")

    def extract_confirmation_link_from_email(self):
        with allure.step("Extracting confirmation link from email"):
            html = self.decode_html(self.email['data'])
            return self.get_href_from_html(html)
