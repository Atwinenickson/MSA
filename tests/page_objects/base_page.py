import random
import os
from time import sleep
from sys import platform
import datetime
from datetime import timedelta, date

from selenium import webdriver
from selenium.webdriver.common.keys import Keys as key
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from tests.utilities.custom_logger import LogGen

"""Parent of all pages
    - Contains common methods to be used by all pages
"""

logger = LogGen.loggen()


class BasePage:
    def __init__(self, driver: webdriver.Chrome, debug=False):
        self.driver = driver
        self.debug = debug

    """Generic Functions"""

    def star_log(self, msg, num=100, decorator="*"):
        """Prints a message with stars around it
        """
        if self.debug:
            logger.info(f"{msg:{decorator}^{num}}")

    def base_get_text(self, selector):
        """
        Returns a string, based on the given selector.
        """
        return self.base_get_element(selector).text
    
    def compare_text_to_element(self, selector, text):
        """
        Returns a boolean, based on the given selector and text.
        """
        return text.lower() in self.base_get_text(selector).lower()
    
    def base_get_element(self, selector):
        """
            Returns an element based on the given selector/xpath.
        """
        if type(selector) is bool:
            return selector

        if type(selector) is not str:
            return self.driver if (selector is None) else selector
        
    def base_is_visible(self, selector):
        """
        Returns true if the given xpath/element is visible.
        """
        try:
            return bool(self.base_get_element(selector))
        except TimeoutException:
            self.error_log(f"ELEMENT NOT VISIBLE: {selector}")
            return False
        
    """SEND KEYS FUNCTION"""

    def base_send_keys(self, selector, text=None, parent=None, clear=True, enter=False):
        """
        Inputs text in the input field element based on the given text.
        """

        parent_condition = parent is not None or type(parent) is str
        if self.base_is_visible(selector, parent):
            element = self.base_get_element(selector, parent=parent)

            if clear:
                if platform == 'darwin':
                    element.send_keys(key.COMMAND + "A")
                else:
                    element.send_keys(key.CONTROL + "A")
                element.send_keys(key.BACKSPACE)

            if text is not None and not isinstance(element, bool):
                element.send_keys(text)
                self.star_log(f"INPUT TEXT: {text}", decorator=' ')
                self.star_log("INPUTTED IN: {parent if parent_condition else ''}{selector}", decorator=' ')

            if enter:
                element.send_keys(key.ENTER)
            self.debug_action(f"Inputting {text} to {parent if parent is not None else ''}{selector}")
        else:
            self.error_log(
                f"INPUT FIELD NOT FOUND: {parent if parent_condition else ''}{selector}")
            raise TimeoutException
        
    def base_click(self, selector, parent=None):
        """
        Clicks on the given xpath_string or element.
        """

        self.debug_action(f"Clicking {parent if parent is not None else ''}{selector}")
        parent_condition = parent is not None and type(parent) is str
        if self.base_is_clickable(selector, parent) and self.base_is_visible(selector, parent):
            try:
                element = self.base_get_element(
                    selector, parent=parent, ec_type="click")
                self.scroll_into_view(element)
                element.click()
                self.star_log(
                    f"Clicked: {parent if parent is not None else ''}{selector}", decorator=" ")
            except ElementClickInterceptedException:
                self.error_log(
                    f"BASE CLICK FAIL ON: {parent if parent is not None else ''}{selector}")
        else:
            self.error_log(
                f"CANNOT BE CLICKED: {parent if parent is not None else ''}{selector}")
            raise TimeoutException
        
    def base_is_clickable(self, selector, parent=None):
        """
        Returns true if the given xpath/element is visible.
        """
        try:
            return bool(self.base_get_element(selector))
        except TimeoutException:
            self.error_log(f"ELEMENT NOT CLICKABLE: {selector}")
            return False