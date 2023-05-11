
import pytest
import os
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from tests.utilities.read_properties import ReadConfig
from tests.utilities.custom_logger import LogGen

logger = LogGen.loggen()

@pytest.fixture(scope='function')
def setup(browser, request):
    """This method runs before every test method."""
    base_url = ReadConfig.get_application_url()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        chrome_prefs = {}
        options.experimental_options["prefs"] = chrome_prefs
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1024")
    elif browser == "edge":
        options = webdriver.EdgeOptions()
    else:
        logger.error(
            "Invalid Browser Driver selected! Try selecting Chrome, Firefox or Edge")
        raise TimeoutException

    driver = get_browser_driver(browser, options)
    request.cls.driver = driver

    implicit_duration = 60

    driver.get(base_url)
    driver.implicitly_wait(implicit_duration)
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.close()

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="selects which browser to use for testing"),
    parser.addoption("--close_driver", action="store", default="true",
                     help="defaults in closing the driver IMMEDIATELY after the test")


@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture()
def close_driver(request):
    return request.config.getoption("--close_driver")


def get_browser_driver(browser, browser_options):
    """Method to identify which browser driver to install"""
    if browser == "chrome":
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=browser_options)
    elif browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(
            GeckoDriverManager().install()), options=browser_options)
    elif browser == "edge":
        driver = webdriver.Edge(service=EdgeService(
            EdgeChromiumDriverManager().install()), options=browser_options)
    else:
        pass

    return driver
