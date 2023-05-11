import time
from tests.page_objects.login_page_objects.login_element import LoginPageElements as loc
from tests.configurations.test_data.login_test_data import LoginTestData as login_data
from selenium import webdriver 
from selenium.common.exceptions import TimeoutException
from tests.page_objects.base_page import BasePage


class LoginPageFunctionality(BasePage):

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)

    def login(self):
        self.star_log("Login to user")
        self.check_email_label()
        self.check_password_label()
        self.check_forgot_password_link()
        self.input_email_address()
        self.input_password()
        self.click_sign_in_button()         
        
    def check_email_label(self):
        assert self.compare_text_to_element(
            loc.email_username_label, "Email address"
        )

    def input_email_address(self):
        self.base_send_keys(loc.email_input_xpath, login_data.email)

    def check_password_label(self):
        """ Method tests for password label """
        assert self.compare_text_to_element(
            loc.password_header_xpath, "Password")

    def input_password(self):
        """Input user password"""
        self.base_send_keys(loc.password_input_xpath, login_data.password)

    def check_forgot_password_link(self):
        """ Method tests if forgot password link is enabled """
        assert self.base_is_visible(loc.forgot_password_xpath)

    def click_sign_in_button(self):
        """Click the sign in button"""
        self.base_click(loc.sign_button_xpath)

