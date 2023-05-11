"""This file reads information from the config.ini file
"""
import configparser

config = configparser.RawConfigParser()
config.read("../tests/configurations/config.ini")

class ReadConfig:
    """Methods to retrieve information from the config file
    """

    @staticmethod
    def get_application_url():
        """Method retrieves the URL from the config file
        """
        url = config.get('Common required information', 'practice_url')
        return url
    
    @staticmethod
    def get_application_landing_title():
        """Method to get the landing title
        """
        page_landing_title = config.get(
            'Common required information', 'page_title'
        )
        return page_landing_title
