from appium.webdriver.common.mobileby import MobileBy as By


class HomeSelectors:
    username_field = (By.ID, "name")
    password_field = (By.ID, "password")
    submit_btn = (By.ID, "login")
