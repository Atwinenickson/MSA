from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium import webdriver
# from selenium.webdriver.support.select import Select
import os
from datetime import timedelta, date
import datetime
from ..utilities.custom_logger import LogGen
from selenium.webdriver.common.keys import Keys as key
from sys import platform
import random
from time import sleep

"""This class is the parent of all pages"""
"""This contains all fundamental features in navigating in the browser"""

logger = LogGen.loggen()


class BasePage:

    def __init__(self, driver: webdriver.Chrome, debug=False):
        self.driver = driver
        self.debug = debug

    """GENERIC FUNCTIONS"""

    def debug_action(self, msg=None):
        if self.debug:
            print(f"\n{msg}")
            print("Press Enter to Continue")
            input()

    def xpathstr_tuple(self, xpath_string):
        """
        Converts XPath string to tuple
        """
        return (By.XPATH, xpath_string)

    def visible_element(self, locator, driver, wait):
        """
        Returns a visible element.
        """
        return WebDriverWait(driver, wait).until(ec.visibility_of_element_located(locator))

    def existing_element(self, locator, driver, wait):
        """
        Returns an existing element.
        """
        return WebDriverWait(driver, wait).until(ec.presence_of_element_located(locator))

    def invisible_element(self, locator, driver, wait):
        """
        Returns an invisible element.
        """
        return WebDriverWait(driver, wait).until(ec.invisibility_of_element_located(locator))

    def clickable_element(self, locator, driver, wait):
        """
        Returns a clickable element.
        """
        return WebDriverWait(driver, wait).until(ec.element_to_be_clickable(locator))

    def visible_all_elements(self, locator, driver, wait):
        """
        Returns a list of visible elements.
        """
        return WebDriverWait(driver, wait).until(ec.visibility_of_all_elements_located(locator))

    def existing_all_elements(self, locator, driver, wait):
        """
        Returns a list of existing elements.
        """
        return WebDriverWait(driver, wait).until(ec.presence_of_all_elements_located(locator))

    def base_get_element(self, selector, parent=None, ec_type="visi", wait=10):
        """
        Returns an element based on the given selector/xpath.
        """
        if type(selector) is bool:
            return selector

        if type(selector) is not str:
            return self.driver if (selector is None) else selector

        ec_func = {
            "visi": self.visible_element,
            "invi": self.invisible_element,
            "exist": self.existing_element,
            "click": self.clickable_element,
        }

        locator = self.xpathstr_tuple(selector)
        driver = self.base_get_element(parent)

        if ec_type not in ec_func:
            self.error_log(f"EC_TYPE INCORRECT: {ec_type} not found")
            return False
        return ec_func[ec_type](locator=locator, driver=driver, wait=wait)

    def base_get_elements(self, selector, parent=None, ec_type="visi", wait=10):
        """
        Returns a list of elements based on the given selector/xpath.
        """
        if type(selector) is not str:
            self.error_log(
                f"SELECTOR TYPE INCORRECT: {selector} is not string")
            return False

        ec_func = {
            "visi": self.visible_all_elements,
            "exist": self.existing_all_elements
        }

        locator = self.xpathstr_tuple(selector)
        driver = self.base_get_element(parent, wait=wait)

        if ec_type not in ec_func:
            self.error_log(f"EC_TYPE INCORRECT: {ec_type} not found")
            return False

        return ec_func[ec_type](locator, driver, wait=wait)

    def base_get_text(self, selector, parent=None, wait=10):
        """
        Returns a string, based on the given selector.
        """
        return self.base_get_element(selector, parent=parent, wait=wait).text

    """CLICK FUNCTIONS"""
    def element_click(self, selector):
        locator = self.xpathstr_tuple(selector)
        element = WebDriverWait(self.driver, 120).until(ec.element_to_be_clickable(locator))
        element.click()

    def base_click(self, selector, parent=None, wait=10):
        """
        Clicks on the given xpath_string or element. 
        """

        self.debug_action(f"Clicking {parent if parent is not None else ''}{selector}")
        parent_condition = parent is not None and type(parent) is str
        if self.base_is_clickable(selector, parent, wait) and self.base_is_visible(selector, parent, wait):
            try:
                element = self.base_get_element(
                    selector, parent=parent, ec_type="click", wait=wait)
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

    def action_click(self, selector, parent=None, wait=10):
        """
        Clicks on the given xpath_string or element. Pointer clicks at the middle of the element.
        """

        self.debug_action(f"Clicking {parent if parent is not None else ''}{selector}")
        parent_condition = parent is not None and type(parent) is str
        if self.base_is_clickable(selector, parent, wait) and self.base_is_visible(selector, parent, wait):
            element = self.base_get_element(selector, parent=parent, ec_type="click", wait=wait)
            ActionChains(self.driver).move_to_element(element).click().perform()
            self.star_log(f"Clicked: {parent if parent_condition else ''}{selector}", decorator=" ")
        else:
            self.error_log(f"CANNOT BE CLICKED: {parent if parent_condition else ''}{selector}")
            raise TimeoutException

    def move_to_element(self, selector, parent=None, wait=10):
        """
        This method moves the cuersor to the element
        """
        actions = ActionChains(self.driver)
        element = self.base_get_element(selector, parent=parent, wait=wait)
        actions.move_to_element(element).perform()

    def script_click(self, selector, parent=None, wait=10):
        """
        Clicks on the given xpath_string or element. Use it for debugging purposes.
        """

        self.debug_action(f"Clicking {parent if parent is not None else ''}{selector}")
        parent_condition = parent is not None and type(parent) is str
        if self.base_is_clickable(selector, parent, wait) and self.base_is_visible(selector, parent, wait):
            element = self.base_get_element(selector, parent=parent, ec_type="click", wait=wait)
            self.driver.execute_script("arguments[0].click();", element)
            self.star_log(f"Clicked: {parent if parent_condition else ''}{selector}", decorator=" ")
        else:
            self.error_log(f"CANNOT BE CLICKED: {parent if parent_condition else ''}{selector}")
            raise TimeoutException

    def click_button(self, button_name, parent=None, wait=10, click_type="BASE"):
        """
        Clicks an element that has the button name.
        """
        button_properties = "normalize-space()='{}'"
        button_xpath = f".//a[{button_properties}] | .//button[{button_properties}]"

        click_functions = {
            "BASE": self.base_click,
            "ACTION": self.action_click,
            "SCRIPT": self.script_click
        }

        if click_type not in click_functions:
            self.error_log("Click type not found")
            return

        click_functions[click_type](button_xpath.format(
            button_name, button_name), parent=parent, wait=wait)

    def base_send_keys(self, selector, text=None, parent=None, clear=True, enter=False, wait=10):
        """
        Inputs text in the input field element based on the given text.
        """

        parent_condition = parent is not None or type(parent) is str
        if self.base_is_visible(selector, parent, wait=wait):
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

    def input_text(self, placeholder, text, enter=False, clear=True, parent=None, wait=10):
        """
        Sends a text to the given input field
        """
        input_tag = ["input", "div", "textarea"]
        tag_size = len(input_tag)
        input_xpath = ""
        for index, tag in enumerate(input_tag):
            input_xpath = f"{input_xpath}.//{tag}[@placeholder='{placeholder}']" + (' | ' if index < tag_size - 1 else '')

        self.base_send_keys(
            input_xpath, text=text, parent=parent, enter=enter, clear=clear, wait=wait
        )

    """BOOLEAN FUNCTIONS"""

    def base_is_visible(self, selector, parent=None, wait=10):
        """
        Returns true if the given xpath/element is visible.
        """
        try:
            return bool(self.base_get_element(selector, parent=parent, wait=wait))
        except TimeoutException:
            self.error_log(f"ELEMENT NOT VISIBLE: {selector}")
            return False

    def base_is_invisible(self, selector, parent=None, wait=10):
        """
        Returns true if the given xpath/element is invisble.
        """
        try:
            return bool(self.base_get_element(selector, parent=parent, ec_type="invi", wait=wait))
        except TimeoutException:
            self.error_log(f"ELEMENT NOT INVISIBLE: {selector}")
            return False

    def base_is_clickable(self, selector, parent=None, wait=10):
        """
        Returns true if the given xpath/element is visible.
        """
        try:
            return bool(self.base_get_element(selector, parent=parent, ec_type="click", wait=wait))
        except TimeoutException:
            self.error_log(f"ELEMENT NOT CLICKABLE: {selector}")
            return False

    def compare_text_to_element(self, selector, text, parent=None, abs_val=False, case_sensitive=False, wait=10):
        """
        Returns true if the given text is found on the given selector.
        """
        self.debug_action(
            f"""
        COMPARE_TEXT_TO_ELEMENT
        TEXT: {text} to
        SELECTOR: {parent if parent is not None else ''}{selector}
            """
        )
        if abs_val:
            return text == self.base_get_text(selector, parent=parent, wait=wait)
        if not case_sensitive:
            return text.lower() in self.base_get_text(selector, parent=parent, wait=wait).lower()
        return text in self.base_get_text(selector, parent=parent)

    def dash_log(self, msg, num=100, decorator="-"):
        """
        Generates an info log with dash characters surrounding the message.
        """
        if self.debug:
            logger.info(f"{msg:{decorator}^{num}}")

    def star_log(self, msg, num=100, decorator="*"):
        """
        Generates an info log with asterisk character surround the message.
        """
        if self.debug:
            logger.info(f"{msg:{decorator}^{num}}")

    def error_log(self, msg, num=99, decorator="!"):
        """
        Generates an error log
        """
        logger.error(f"{msg:{decorator}^{num}}")

    def scroll_into_view(self, selector, scroll_option=None, parent=None):
        """
        Method uses a javascript executor to have a webelement scroll into the view.
        """
        element = self.base_get_element(selector, parent, ec_type="visi")
        if type(element) is not bool and scroll_option is not None:
            self.driver.execute_script(
                f"arguments[0].scrollIntoView({scroll_option});", element)
        if type(element) is not bool and scroll_option is None:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: \"auto\", block: \"center\", inline: \"center\"});", element
            )

    def slide_the_price_slider(self, selector, parent=None, wait=10):
        """
        This method moves the slides the slider to the right.
        """
        sliders = self.base_get_elements(selector, parent=parent, wait=wait)
        left_slider = sliders[0]
        right_slider = sliders[1]
        move = ActionChains(self.driver)
        # Moving the left slider
        move.click_and_hold(left_slider).move_by_offset(0, 0).release().perform()
        # Moving the right slider
        move.click_and_hold(right_slider).move_by_offset(-57, 0).release().perform()

    def select_item_in_dropdown(self, selector, text, parent=None):
        """
        Selects an item in a select type dropdown.
        """
        element = self.driver.find_element(By.ID, selector)
        dropdown_value = Select(element)
        dropdown_value.select_by_value(text)

    def get_all_text_under_div(self, selector):
        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        text_list = [element.text for element in elements]
        return text_list
