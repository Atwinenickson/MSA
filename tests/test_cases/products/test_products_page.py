import time
import pytest
from ...utilities.read_properties import ReadConfig
from ...utilities.login import LoginUser
from tests.test_cases.test_base import BaseTest

from ...page_objects.products_page_objects.products_page_functionality import ProductFunctionality


class TestProductFixtures(BaseTest):
    """This class contains the fixtures needed for the Staff Test Scripts to run"""

    def check_page_title(self):
        page_title = self.driver.title
        assert page_title == ReadConfig.get_application_landing_title()

    def check_product_title(self):
        product_page_title = self.driver.title
        assert product_page_title == ReadConfig.get_product_page_title()

    @pytest.fixture
    def test_navigate_to_product_page(self):
        """This fixture verifies that the user can navigate to products page Successfully"""

        # Instantiation
        product_page = ProductFunctionality(self.driver)

        login_page = LoginUser(self.driver)
        login_page.login()
        self.check_page_title()
        time.sleep(3)

        product_page.star_log("Test Case 01")
        product_page.star_log("Navigate to Product Page")
        product_page.navigate_to_product_page()
        self.check_product_title()
        product_page.star_log("Successfully navigated to Product Page")

class TestUserViewProducts(TestProductFixtures):

    def test_user_can_view_all_products(self, test_navigate_to_product_page):
        """This test verifies that the user can view all products"""

        # Instantiation
        product_page = ProductFunctionality(self.driver)
        test_navigate_to_product_page

        product_page.star_log("Test Case 01")
        product_page.star_log("View All Products")
        product_page.view_all_products()
        product_page.star_log("Successfully viewed all products")

    def test_user_can_add_product_to_carts(self, test_navigate_to_product_page):
        """This test verifies that the user can view all products"""

        # Instantiation
        product_page = ProductFunctionality(self.driver)
        test_navigate_to_product_page

        product_page.star_log("Test Case 02")
        product_page.star_log("Add Product to card")
        product_page.user_can_add_product_to_cart()
        product_page.star_log("Successfully added product to cart")
