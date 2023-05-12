
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
        self.scroll_into_view(product_elements.home_page_header_xpath)
        self.base_click(product_elements.home_page_header_xpath)
        self.scroll_into_view(product_elements.best_sellers_header_xpath)
        self.base_click(product_elements.best_sellers_header_xpath)

    def view_all_products(self):
        names = self.base_get_elements(product_elements.all_names_xpath)
        prices = self.base_get_elements(product_elements.all_prices_xpath)
        product_details = []

        for name_elem, price_elem in zip(names, prices):
            name = name_elem.text.strip()
            price = price_elem.text.strip()
            product_details.append((name, price))

        sorted_price_details = sorted(product_details, key=lambda x: float(x[1].replace('$', '')))
        print(sorted_price_details)