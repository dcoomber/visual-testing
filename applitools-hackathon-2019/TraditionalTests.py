import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

# _url = "https://demo.applitools.com/hackathon.html"
_url = 'https://demo.applitools.com/hackathonV2.html'


class TraditionalTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_login_page_elements(self):
        self.browser.get(_url)
        WebDriverWait(self.browser, 15).\
            until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@class='auth-header']")))

        # Login logo
        is_displayed = self.browser.find_element(By.XPATH, "//img[contains(@src,'logo')]").is_displayed()
        self.assertTrue(is_displayed, "Logo was not displayed")

        # Login title
        is_displayed = self.browser.find_element(By.CLASS_NAME, "auth-header").is_displayed()
        self.assertTrue(is_displayed, "Login title was not displayed")

        # Username input
        is_displayed = self.browser.find_element(By.XPATH, "//*[@id='username']").is_displayed()
        self.assertTrue(is_displayed, "Username entry was not displayed")

        # Password input
        is_displayed = self.browser.find_element(By.XPATH, "//*[@id='password']").is_displayed()
        self.assertTrue(is_displayed, "Password entry was not displayed")

        # Login button
        is_displayed = self.browser.find_element(By.XPATH, "//*[@id='log-in']").is_displayed()
        self.assertTrue(is_displayed, "Login button was not displayed")

        # Remember me checkbox
        is_displayed = self.browser.find_element(By.XPATH, "//*[@class='form-check-input']").is_displayed()
        self.assertTrue(is_displayed, "Remember Me checkbox was not displayed")

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

        for login in credentials:
            # Credentials input
            self.browser.find_element(By.XPATH, "//*[@id='username']").send_keys(login["username"])
            self.browser.find_element(By.XPATH, "//*[@id='password']").send_keys(login["password"])
            self.browser.find_element(By.XPATH, "//*[@id='log-in']").click()

            # Evaluate
            is_displayed = self.browser.find_element(By.XPATH, login["validation_element"]).is_displayed()
            self.assertTrue(is_displayed, "Login warning alert not displayed")

            self.browser.refresh()

    def test_sort_amount_column(self):
        self.browser.get(_url)
        WebDriverWait(self.browser, 15).\
            until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@class='auth-header']")))

        # Login
        # Credentials input
        self.browser.find_element(By.XPATH, "//*[@id='username']").send_keys("David")
        self.browser.find_element(By.XPATH, "//*[@id='password']").send_keys("super secret password")
        self.browser.find_element(By.XPATH, "//*[@id='log-in']").click()

        is_displayed = self.browser.find_element(By.XPATH, "//*[@id='transactionsTable']").is_displayed()
        self.assertTrue(is_displayed, "Data table is not displayed")

        # Before snapshots
        column_status_before = self.browser.find_elements(
            By.XPATH,
            "//*[@id='transactionsTable']//td[@class='nowrap']")

        column_description_before = self.browser.find_elements(
            By.XPATH,
            "//*[@id='transactionsTable']//td[@class='cell-with-media']")

        column_amount_before = self.browser.find_elements(
            By.XPATH,
            "//*[@id='transactionsTable']//td[@class='text-right bolder nowrap']")

        # Sort data table by amount
        self.browser.find_element(By.XPATH, "//*[@id='amount']").click()

        # After snapshots
        column_status_after = self.browser.find_elements(
            By.XPATH,
            "//*[@id='transactionsTable']//td[@class='nowrap']")

        column_description_after = self.browser.find_elements(
            By.XPATH,
            "//*[@id='transactionsTable']//td[@class='cell-with-media']")

        column_amount_after = self.browser.find_elements(
            By.XPATH,
            "//*[@id='transactionsTable']//td[@class='text-right bolder nowrap']")

        # Is data table sorted ascending by amount?
        for item in range(len(column_amount_after) - 1):
            this_item = float(
                column_amount_after[item].text.replace(" USD", "").replace(" ", "").replace(",", "")
            )
            next_item = float(
                column_amount_after[item + 1].text.replace(" USD", "").replace(" ", "").replace(",", "")
            )
            self.assertGreater(next_item, this_item)

        # Does data table intact after sorting?
        for before_item in range(len(column_description_before) - 1):
            for after_item in range(len(column_description_before) - 1):
                if column_description_before[before_item].text == column_description_after[after_item].text:
                    self.assertEquals(column_status_before[before_item].text,
                                      column_status_after[after_item].text)
                    self.assertEquals(column_amount_before[before_item].text,
                                      column_amount_after[after_item].text)

    def test_canvas_chart(self):
        # Cannot validate chart contents; only able to validate that chart is displayed

        self.browser.get(_url)
        WebDriverWait(self.browser, 15).\
            until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@class='auth-header']")))

        # Login
        # Credentials input
        self.browser.find_element(By.XPATH, "//*[@id='username']").send_keys("David")
        self.browser.find_element(By.XPATH, "//*[@id='password']").send_keys("super secret password")
        self.browser.find_element(By.XPATH, "//*[@id='log-in']").click()

        # Open expenses chart
        self.browser.find_element(By.XPATH, "//*[@id='showExpensesChart']").click()

        is_displayed = self.browser.find_element(By.XPATH, "//*[@id='canvas']").is_displayed()
        self.assertTrue(is_displayed, "Canvas chart is not displayed")

    def test_dynamic_content(self):
        self.browser.get(_url + "?showAd=true")
        WebDriverWait(self.browser, 15).\
            until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@class='auth-header']")))

        # Login
        # Credentials input
        self.browser.find_element(By.XPATH, "//*[@id='username']").send_keys("David")
        self.browser.find_element(By.XPATH, "//*[@id='password']").send_keys("super secret password")
        self.browser.find_element(By.XPATH, "//*[@id='log-in']").click()

        # Are adverts displayed?
        is_displayed = self.browser.find_element(By.XPATH, "//*[@id='flashSale']/img").is_displayed()
        self.assertTrue(is_displayed, "First advert is not displayed")

        is_displayed = self.browser.find_element(By.XPATH, "//*[@id='flashSale2']/img").is_displayed()
        self.assertTrue(is_displayed, "Second advert is not displayed")


if __name__ == "__main__":
    unittest.main()