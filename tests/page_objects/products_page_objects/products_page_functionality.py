
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

    def user_can_add_product_to_cart(self):
        self.scroll_into_view(product_elements.women_section_xpath)
        time.sleep(5)
        self.base_click(product_elements.women_section_xpath)
        time.sleep(5)
        self.base_click(product_elements.dresses_section_xpath)
        time.sleep(5)
        self.base_click(product_elements.evening_dresses_section_xpath)
        time.sleep(5)
        self.filter_dresses()
        self.select_dress()

    def filter_dresses(self):
        # self.action_click(product_elements.medium_xpath)
        # time.sleep(5)
        self.action_click(product_elements.pink_xpath)
        time.sleep(5)
        self.scroll_into_view(product_elements.range_xpath)
        self.slide_the_price_slider(product_elements.slider_xpath)
        time.sleep(10)

    def select_dress(self):
        self.base_click(selector=product_elements.more_xpath)
        time.sleep(5)
        self.scroll_into_view(product_elements.quantity_label_xpath)
        self.base_send_keys(product_elements.quantity_xpath, test_data.quantity)
        time.sleep(3)
        self.select_item_in_dropdown(product_elements.size_select_xpath, "M")
        time.sleep(3)
        self.action_click(selector=product_elements.select_pink_xpath)
        time.sleep(3)
        self.click_button("Add to cart")

   
