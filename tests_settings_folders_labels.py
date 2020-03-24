import os

import pytest
from selenium import webdriver


from pages import *


def log_test_headline(msg):
    logging.info('='*40)
    logging.info(msg.upper())
    logging.info('='*40)


def report_fail(msg, driver=None, screenshot=''):
    logging.warning('Test failed: ')
    logging.warning(msg)
    if driver:
        if not os.path.exists(Config.DATA_DIR):
            os.mkdir(Config.DATA_DIR)
        screenshot = os.path.join(Config.DATA_DIR, screenshot)
        driver.save_screenshot(screenshot)
    # TODO create snapshot
    assert False, msg


@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome(Config.CHROME_PATH)
    logging.info('Webdriver initialized')
    login_page = LoginPage(driver)
    login_page.login()
    driver.get(SettingsFoldersPage.URL)
    _ = WebDriverWait(driver, 5).until(EC.title_is(SettingsFoldersPage.TITLE))
    yield driver


class TestsFoldersLabels:
    """
    Tests for Settings: Folders/Labels
    Preconditions: no Labels or Folders created
    """

    @pytest.mark.parametrize("foldername,color", [("folder1", ColorsLocators.get_random())])
    def test_add_folder(self, driver, foldername, color):
        log_test_headline('Test add folder')
        logging.info(f'Parameters: foldername={foldername}, color={color} ')

        settings_page = SettingsFoldersPage(driver)
        settings_page.add_folder(foldername, getattr(ColorsLocators, color))
        driver.implicitly_wait(1)

        if not settings_page.item_is_displayed(foldername):
            report_fail('Created folder is not displayed', driver, 'test_add_folder_display.png')
        if not settings_page.item_color_is_correct(foldername, getattr(ColorsMap, color)):
            report_fail('Color of new folder is not correct', driver, 'test_add_folder_color.png')

    @pytest.mark.parametrize("foldername, new_foldername, new_color",
                             [('folder1', 'folder1_modified', ColorsLocators.get_random())])
    def test_edit_folder(self, driver, foldername, new_foldername, new_color):
        log_test_headline('Test edit folder')
        logging.info(f'Parameters: foldername={foldername}, new_foldername={new_foldername}, new_color={new_color} ')

        settings_page = SettingsFoldersPage(driver)
        settings_page.edit_folder(foldername, new_foldername, getattr(ColorsLocators, new_color))
        driver.implicitly_wait(1)

        if not settings_page.item_is_displayed(new_foldername):
            report_fail('Modified folder is not displayed', driver, 'test_edit_folder_display.png')
        if not settings_page.item_color_is_correct(new_foldername, getattr(ColorsMap, new_color)):
            report_fail('Color of modified folder is not correct', driver, 'test_edit_folder_color.png')

    @pytest.mark.parametrize("foldername", ['folder1_modified'])
    def test_delete_folder(self, driver, foldername):
        log_test_headline('Test delete folder')
        logging.info(f'Parameters: foldername={foldername}')

        settings_page = SettingsFoldersPage(driver)
        settings_page.delete_folder(foldername)
        driver.implicitly_wait(2)

        if settings_page.item_is_displayed(foldername):
            report_fail('Folder is not deleted', driver, 'test_delete_folder.png')


def init_logging():
    logging.basicConfig(level=logging.INFO, filename='../log.log')
    logging.getLogger().addHandler(logging.StreamHandler())


def main():

    print(Config.PASSWORD)

    # driver = webdriver.Chrome(Config.CHROME_PATH)
    # logging.info('Webdriver initialized')
    # login_page = LoginPage(driver)
    # login_page.login()
    # driver.get(SettingsFoldersPage.URL)
    # _ = WebDriverWait(driver, 5).until(EC.title_is(SettingsFoldersPage.TITLE))
    #
    # t = TestsFoldersLabels()
    # # t.setup()
    # t.test_delete_folder(driver, 'folder1_modified')
    # # t.test_edit_folder('label1', 'label1_modified', 'blue')
    # # l = LoginPage()
    # # l.login()

    # print('Press any key..')
    # a = input()


if __name__ == '__main__':
    init_logging()
    main()
