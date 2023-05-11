import time
from tests.page_objects.base_page import BasePage
from tests.page_objects.login_page_objects.login_functionality import LoginPageFunctionality
from selenium.common.exceptions import TimeoutException
from tests.utilities.custom_logger import LogGen
from tests.utilities.read_properties import ReadConfig
from selenium import webdriver
from tests.page_objects.login_page_objects.login_element import LoginPageElements as loc

logger = LogGen.loggen()

class LoginUser(BasePage):
    """This class logs in a user
    """

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)

    def login(self):
        """Method to login a user
        """
        login_form = LoginPageFunctionality(self.driver)
        self.star_log("Logging in to the system")
        self.check_sign_header_label()
        self.base_click(loc.login_link_xpath)
        time.sleep(5)
        login_form.login()
    
    def check_sign_header_label(self):
        assert self.compare_text_to_element(
            loc.sign_header_xpath, "Sign in")
