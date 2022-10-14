import allure
from tests.config.urls import Urls
from tests.pages.confirmation_page import ConfirmationPage
from tests.pages.home_page import HomePage
from tests.pages.newsletters_page import NewslettersPage
from tests.pages.unsubscribe_page import UnsubscribePage
from tests.testData.test_data import TestData


class TestEuronews(object):
    def test_euronews(self, browser, gmail):
        with allure.step("Follow Euronews link"):
            browser.set_url(Urls.EURONEWS_URL)
            home_page = HomePage()
            assert home_page.is_opened(), "Home page did not open"

        with allure.step("Follow the link 'Newsletters'' in the header"):
            home_page.navigate_to_newsletters()
            newsletters_page = NewslettersPage()
            assert newsletters_page.is_opened(), "Newsletters page did not open"

        with allure.step("Choose a random newsletter subscription plan"):
            newsletters_page.choose_random_newsletter()
            assert newsletters_page.email_form_is_displayed(), "Email form was not displayed"

        with allure.step("Enter email, click 'Submit' button"):
            newsletters_page.submit_email(TestData.email)
            gmail.wait_until_new_email()
            assert gmail.confirm_subscription_email_received(), "Confirm subscription email was not received"

        with allure.step("Follow the link received from the letter"):
            browser.set_url(gmail.extract_confirmation_link_from_email())
            confirmation_page = ConfirmationPage()
            assert confirmation_page.confirmation_success_message_is_displayed(), \
                "Email confirmation success message was not displayed"

        with allure.step("Click 'Back to the site'"):
            confirmation_page.click_back_to_the_site()
            assert home_page.is_opened(), "Home page did not open"

        with allure.step("Follow the link 'Newsletters' in the header, "
                         "choose the same newsletter subscription plan as in the step 3, click 'See preview'"):
            home_page.navigate_to_newsletters()
            newsletters_page.click_see_preview_on_chosen_newsletter()
            assert newsletters_page.preview_of_required_plan_is_displayed(), \
                "Preview of required newsletter was not displayed"

        with allure.step("On preview find and get a link to unsubscribe from the mailing list, "
                         "follow this link in the browser"):
            browser.switch_to_frame(newsletters_page.preview_frame_of_chosen_newsletter)
            newsletters_page.follow_unsubscribe_link()
            unsubscribe_page = UnsubscribePage()
            assert unsubscribe_page.is_opened(), "Unsubscribe page did not open"

        with allure.step("Enter email, click 'Submit' button"):
            num_emails_before = gmail.number_of_emails
            unsubscribe_page.enter_email_and_submit(TestData.email)
            assert unsubscribe_page.subscription_cancelled_message_is_displayed(), \
                "Unsubscription message was not displayed"

        with allure.step("Make sure that you haven't received an email "
                         "with a message about canceling your subscription"):
            num_emails_after = gmail.number_of_emails
            assert num_emails_before == num_emails_after, "New email was received"

