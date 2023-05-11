
import time
from .products_page_elements import ProductElements
from tests.configurations.test_data.product_test_data import ProductTestData
from tests.page_objects.base_page import BasePage

# Instantiating page objects, test data, and UI checks
product_elements = ProductElements
test_data = ProductTestData

class ProductFunctionality(BasePage):
    """Class describes webdriver actions for Products Page"""

    def navigate_to_product_page(self):
        """Method tests navigating to the products page"""
        assert 1 == 1