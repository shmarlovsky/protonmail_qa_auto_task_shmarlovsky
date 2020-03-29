import os
import logging
import pytest
from selenium import webdriver

from protonmail_auto.pages import SettingsFoldersPage, LoginPage
from protonmail_auto.config import Config
from protonmail_auto.locators import ColorsLocators, ColorsMap


class SetupException(Exception):
    pass


def log_test_headline(msg):
    """
    fancy logging for test headline
    :param msg:
    :return:
    """
    logging.info('=' * 40)
    logging.info(f"\t\t\t{msg.upper()}")
    logging.info('=' * 40)


def report_fail(msg, driver=None, screenshot_name=''):
    """
    Log message in case of failed test.
    If driver and screenshot specified - save screenshot too
    :param msg: message to log
    :param driver: selenium.WebDriver
    :param screenshot_name: screenshot name
    :return:
    """
    logging.warning('Test failed: ')
    logging.warning(msg)
    if driver:
        make_screenshot(driver, screenshot_name)
    assert False, msg


def make_screenshot(driver, screenshot_name):
    """
    save screenshot to Config.DATA_DIR
    :param driver: selenium.webdriver
    :param screenshot_name:
    :return: None
    """
    if not os.path.exists(Config.DATA_DIR):
        os.mkdir(Config.DATA_DIR)
    screenshot = os.path.join(Config.DATA_DIR, screenshot_name)
    driver.save_screenshot(screenshot)


@pytest.fixture(scope="class")
def driver():
    """
    pytest fixture used by tests.
    Open browser, login, got to Settings Folder/Labels page
    :return:
    """
    logging.info('\t\t Initializing "driver" fixture')
    driver = webdriver.Chrome(Config.CHROME_PATH)
    logging.info('Webdriver initialized')
    login_page = LoginPage(driver)
    logged_in = login_page.login()
    if logged_in:
        settings_page = SettingsFoldersPage(driver)
        settings_page.go_to_settings_page()
        yield driver
    else:
        raise SetupException('Failed to log in')


@pytest.fixture(scope='function')
def teardown_fixture(driver):
    settings_page = SettingsFoldersPage(driver)
    settings_page.close_modal_dialog()
    yield


@pytest.mark.usefixtures("teardown_fixture")
class TestsFoldersLabels:
    """
    Tests for Settings: Folders/Labels
    Preconditions:
    Perfectly it would be great to have predefined test data, but for testing beta
    no Labels or Folders should exist with names folder1, folder1_modified
    label1, label1_modified
    """
    # get random colors to cover more cases
    FOLDER_COLOR1 = ColorsLocators.get_random()
    FOLDER_COLOR2 = ColorsLocators.get_random()
    LABEL_COLOR1 = ColorsLocators.get_random()
    LABEL_COLOR2 = ColorsLocators.get_random()

    @pytest.mark.parametrize("foldername,color", [("folder1", FOLDER_COLOR1)])
    def test_add_folder(self, driver, foldername, color):
        """
        Click on Add Folder, select name and color, click on Submit.
        Check success notification, folder is displayed, color is correct
        :param driver:
        :param foldername:
        :param color:
        :return:
        """
        test_name = 'test_add_folder'
        log_test_headline('Test add folder')
        logging.info(f'Parameters: labelname={foldername}, color={color} ')

        settings_page = SettingsFoldersPage(driver)
        settings_page.add_folder(foldername, getattr(ColorsLocators, color))

        fail_msg = ''
        if not settings_page.success_notification_appeared(f'{foldername} created'):
            make_screenshot(driver, f'{test_name}_notification.png')
            fail_msg += 'No success notification'

        if not settings_page.item_is_displayed(foldername):
            make_screenshot(driver, f'{test_name}_display.png')
            fail_msg += 'Created folder is not displayed'

        if not settings_page.item_color_is_correct(foldername, getattr(ColorsMap, color)):
            make_screenshot(driver, f'{test_name}_color.png')
            fail_msg += 'Color of new item is not correct'

        if fail_msg:
            report_fail(fail_msg)

    @pytest.mark.parametrize("foldername, new_foldername, new_color",
                             [('folder1', 'folder1_modified', FOLDER_COLOR2)])
    def test_edit_folder(self, driver, foldername, new_foldername, new_color):
        """
        Click on Edit Folder, modify name and color, click on Submit.
        Check success notification, folder with new name is displayed, color is correct
        :param driver:
        :param foldername:
        :param new_foldername:
        :param new_color:
        :return:
        """
        test_name = 'test_edit_folder'
        log_test_headline('Test edit folder')
        logging.info(f'Parameters: labelname={foldername}, new_labelname={new_foldername}, new_color={new_color} ')

        settings_page = SettingsFoldersPage(driver)
        settings_page.edit_item(foldername, new_foldername, getattr(ColorsLocators, new_color))

        fail_msg = ''
        if not settings_page.success_notification_appeared(f'{new_foldername} updated'):
            make_screenshot(driver, f'{test_name}_notification.png')
            fail_msg += 'No success notification'

        if not settings_page.item_is_displayed(new_foldername):
            make_screenshot(driver, f'{test_name}_display.png')
            fail_msg += 'Modified folder is not displayed'

        if not settings_page.item_color_is_correct(new_foldername, getattr(ColorsMap, new_color)):
            make_screenshot(driver, f'{test_name}_color.png')
            fail_msg += 'Color of modified item is not correct'

        if fail_msg:
            report_fail(fail_msg)

    @pytest.mark.parametrize("foldername", ['folder1_modified'])
    def test_delete_folder(self, driver, foldername):
        """
        Click on Delete Folder,  click on Submit.
        Check success notification, folder is not displayed
        :param driver:
        :param foldername:
        :return:
        """
        test_name = 'test_delete_folder'
        log_test_headline('Test delete folder')
        logging.info(f'Parameters: labelname={foldername}')

        settings_page = SettingsFoldersPage(driver)
        settings_page.delete_item(foldername)
        fail_msg = ''

        if not settings_page.success_notification_appeared(f'{foldername} removed'):
            make_screenshot(driver, f'test_name_notification.png')
            fail_msg += 'No success notification'

        if settings_page.item_is_displayed(foldername):
            report_fail('Item is not deleted', driver, f'{test_name}.png')

        if fail_msg:
            report_fail(fail_msg)

    @pytest.mark.parametrize("labelname, color", [("label1", LABEL_COLOR1)])
    def test_add_label(self, driver, labelname, color):
        """
        Click on Add Label , select name and color, click on Submit.
        Check success notification, label is displayed, color is correct
        :param driver:
        :param labelname:
        :param color:
        :return:
        """
        test_name = 'test_add_label'
        log_test_headline('Test add label')
        logging.info(f'Parameters: labelname={labelname}, color={color} ')

        settings_page = SettingsFoldersPage(driver)
        settings_page.add_folder(labelname, getattr(ColorsLocators, color))

        fail_msg = ''
        if not settings_page.success_notification_appeared(f'{labelname} created'):
            make_screenshot(driver, f'{test_name}_notification.png')
            fail_msg += 'No success notification'

        if not settings_page.item_is_displayed(labelname):
            make_screenshot(driver, f'{test_name}_display.png')
            fail_msg += 'Created folder is not displayed'

        if not settings_page.item_color_is_correct(labelname, getattr(ColorsMap, color)):
            make_screenshot(driver, f'{test_name}_color.png')
            fail_msg += 'Color of new item is not correct'

        if fail_msg:
            report_fail(fail_msg)

    @pytest.mark.parametrize("labelname, new_labelname, new_color",
                             [('label1', 'label1_modified', LABEL_COLOR2)])
    def test_edit_label(self, driver, labelname, new_labelname, new_color):
        """
        Click on Edit Label, modify name and color, click on Submit.
        Check success notification, label with new name is displayed, color is correct
        :param driver:
        :param labelname:
        :param new_labelname:
        :param new_color:
        :return:
        """
        test_name = 'test_edit_label'
        log_test_headline('Test edit label')
        logging.info(f'Parameters: labelname={labelname}, new_labelname={new_labelname}, new_color={new_color} ')

        settings_page = SettingsFoldersPage(driver)
        settings_page.edit_item(labelname, new_labelname, getattr(ColorsLocators, new_color))

        fail_msg = ''
        if not settings_page.success_notification_appeared(f'{new_labelname} updated'):
            make_screenshot(driver, f'{test_name}_notification.png')
            fail_msg += 'No success notification'

        if not settings_page.item_is_displayed(new_labelname):
            make_screenshot(driver, f'{test_name}_display.png')
            fail_msg += 'Modified folder is not displayed'

        if not settings_page.item_color_is_correct(new_labelname, getattr(ColorsMap, new_color)):
            make_screenshot(driver, f'{test_name}_color.png')
            fail_msg += 'Color of modified item is not correct'

        if fail_msg:
            report_fail(fail_msg)

    @pytest.mark.parametrize("labelname", ['label1_modified'])
    def test_delete_label(self, driver, labelname):
        """
        Click on Delete Label, click on Submit.
        Check success notification, label is not displayed
        :param driver:
        :param labelname:
        :return:
        """
        test_name = 'test_delete_label'
        log_test_headline('Test delete label')
        logging.info(f'Parameters: labelname={labelname}')

        settings_page = SettingsFoldersPage(driver)
        settings_page.delete_item(labelname)
        fail_msg = ''

        if not settings_page.success_notification_appeared(f'{labelname} removed'):
            make_screenshot(driver, f'test_name_notification.png')
            fail_msg += 'No success notification'

        if settings_page.item_is_displayed(labelname):
            report_fail('Item is not deleted', driver, f'{test_name}.png')

        if fail_msg:
            report_fail(fail_msg)

    # # TODO. not covered
    # def test_add_folder_cancel(self):
    #     pass

    # # TODO. not covered
    # def test_edit_folder_cancel(self):
    #     pass

    # # TODO. not covered
    # def test_folder_disable_notifications(self):
    #     pass

    # # TODO. not covered
    # def test_delete_folder_cancel(self):
    #     pass

    # # TODO. not covered
    # def test_folder_enable_notifications(self):
    #     pass

    # # TODO. not covered
    # def test_add_label_cancel(self):
    #     pass

    # # TODO. not covered
    # def test_edit_label_cancel(self):
    #     pass

    # # TODO. not covered
    # def test_delete_label_cancel(self):
    #     pass


def init_logging():
    logging.basicConfig(level=logging.INFO, filename='../log.log')
    logging.getLogger().addHandler(logging.StreamHandler())


def main():
    driver = webdriver.Chrome(Config.CHROME_PATH)
    logging.info('Webdriver initialized')
    login_page = LoginPage(driver)
    login_page.login()
    driver.get(SettingsFoldersPage.URL)
    # _ = WebDriverWait(driver, 5).until(EC.title_is(SettingsFoldersPage.TITLE))

    page = SettingsFoldersPage(driver)
    page.close_modal_dialog()

    # t = TestsFoldersLabels()
    # # t.setup()
    # t.test_delete_folder(driver, 'folder1_modified')
    # # t.test_edit_folder('label1', 'label1_modified', 'blue')
    # l = LoginPage()
    # # l.login()

    # print('Press any key..')
    # a = input()


if __name__ == '__main__':
    init_logging()
    main()
