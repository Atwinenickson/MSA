import pytest
from tests.utilities.login import LoginUser, LogoutUser

@pytest.mark.usefixtures("setup")
class BaseTest:

    def login(self, user):
        page = LoginUser(self.driver)
        page.login()