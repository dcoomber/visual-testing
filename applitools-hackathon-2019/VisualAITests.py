import os
import unittest

from applitools.core.eyes_base import BatchInfo
from applitools.selenium import Eyes
from selenium import webdriver
from selenium.webdriver.common.by import By

# _url = "https://demo.applitools.com/hackathon.html"
_url = 'https://demo.applitools.com/hackathonV2.html'


class FunctionalTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.eyes = Eyes()

        batch = BatchInfo("Applitools Hackathon 2019")
        batch.id = "Applitools Hackathon 2019"
        self.eyes.batch = batch
        self.eyes.branch_name = "applitools-hackathon-2019"

        self.eyes.force_full_page_screenshot = True
        self.eyes.api_key = os.environ["APPLITOOLS_API_KEY"]

    def tearDown(self):
        self.browser.quit()
        self.eyes.close()

    def test_login_page_elements(self):
        self.browser.get(_url)
        self.eyes.open(self.browser, "Applitools_Hackathon_2019", "test_login_page_elements")
        self.eyes.check_window("test_login_page_elements")

    def test_login_page_functionality(self):
        credentials = [
                                {
                                    "scenario": "Empty username and password",
                                    "username": "",
                                    "password": "",
                                    "validation_element": "// div[contains( @ id, 'random_id')]"
                                },
                                {
                                    "scenario": "Empty password",
                                    "username": "username",
                                    "password": "",
                                    "validation_element": "// div[contains( @ id, 'random_id')]"
                                },
                                {
                                    "scenario": "Empty username",
                                    "username": "",
                                    "password": "password",
                                    "validation_element": "// div[contains( @ id, 'random_id')]"
                                },
                                {
                                    "scenario": "Valid login",
                                    "username": "David",
                                    "password": "super secret password",
                                    "validation_element": "//*[@id='showExpensesChart']"
                                }
                            ]

        self.browser.get(_url)
        self.eyes.open(self.browser, "Applitools_Hackathon_2019", "test_login_page_elements")

        for login in credentials:
            self.browser.refresh()

            # Credentials input
            self.browser.find_element(By.XPATH, "//*[@id='username']").send_keys(login["username"])
            self.browser.find_element(By.XPATH, "//*[@id='password']").send_keys(login["password"])
            self.browser.find_element(By.XPATH, "//*[@id='log-in']").click()

            self.eyes.check_window("test_login_page_functionality")

    def test_sort_amount_column(self):
        self.browser.get(_url)
        self.eyes.open(self.browser, "Applitools_Hackathon_2019", "test_sort_amount_column")

        # Login
        # Credentials input
        self.browser.find_element(By.XPATH, "//*[@id='username']").send_keys("David")
        self.browser.find_element(By.XPATH, "//*[@id='password']").send_keys("super secret password")
        self.browser.find_element(By.XPATH, "//*[@id='log-in']").click()

        # Sort data table by amount
        self.browser.find_element(By.XPATH, "//*[@id='amount']").click()

        self.eyes.check_window("test_sort_amount_column")

    def test_canvas_chart(self):
        self.browser.get(_url)
        self.eyes.open(self.browser, "Applitools_Hackathon_2019", "test_canvas_chart")

        # Login
        # Credentials input
        self.browser.find_element(By.XPATH, "//*[@id='username']").send_keys("David")
        self.browser.find_element(By.XPATH, "//*[@id='password']").send_keys("super secret password")
        self.browser.find_element(By.XPATH, "//*[@id='log-in']").click()

        # Open expenses chart
        self.browser.find_element(By.XPATH, "//*[@id='showExpensesChart']").click()
        self.eyes.check_window("test_canvas_chart")
        self.browser.find_element(By.XPATH, "//*[@class='btn btn-warning']").click()
        self.eyes.check_window("test_canvas_chart")

    def test_dynamic_content(self):
        self.browser.get(_url + "?showAd=true")
        self.eyes.open(self.browser, "Applitools_Hackathon_2019", "test_dynamic_content")

        # Login
        # Credentials input
        self.browser.find_element(By.XPATH, "//*[@id='username']").send_keys("David")
        self.browser.find_element(By.XPATH, "//*[@id='password']").send_keys("super secret password")
        self.browser.find_element(By.XPATH, "//*[@id='log-in']").click()

        self.eyes.check_window("test_dynamic_content")


if __name__ == "__main__":
    unittest.main()
