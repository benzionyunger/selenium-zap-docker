from appium.webdriver.common.mobileby import MobileBy as By


class ExamplePage:
    permission_allow_btn = (By.ID, "com.android.packageinstaller:id/permission_allow_button")
    add_user_btn = (By.ID, "com.leadermes.managerapp:id/plus_button")
    machine_container_in_department = (By.ID, "com.leadermes.managerapp:id/container_1")