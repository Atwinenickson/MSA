import time
from tests.page_objects.base_page import BasePage
from tests.page_objects.login_page_objects.login_functionality import LoginPageFunctionality
from selenium.common.exceptions import TimeoutException
from tests.page_objects.common_objects.pop_up_actions import PopUpActions
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
        login_form.login()
