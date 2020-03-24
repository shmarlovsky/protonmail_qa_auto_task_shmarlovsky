import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from config import Config
from locators import *


class BasePage:
    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):
    URL = 'https://beta.protonmail.com/login'

    def login(self):
        logging.info('Login..')
        self.driver.get(self.URL)
        logging.info(f'Go to "{self.URL}"')

        # username_field = self.driver.find_element(*LoginPageLocators.USERNAME_FIELD)
        username_field = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(LoginPageLocators.USERNAME_FIELD))
        username_field.send_keys(Config.USERNAME)
        logging.info(f'Send "{Config.USERNAME}" to username field: {LoginPageLocators.USERNAME_FIELD}')

        password_field = self.driver.find_element(*LoginPageLocators.PASSWORD_FIELD)
        password_field.send_keys(Config.PASSWORD)
        logging.info(f'Send "{Config.PASSWORD}" to password field: {LoginPageLocators.PASSWORD_FIELD}')

        password_field.send_keys(Keys.ENTER)

        # close welcome dialog if exist
        try:
            # welcome_close_btn = self.driver.find_element(*WelcomeDialog.CLOSE_BTN)
            welcome_close_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(WelcomeDialogLocators.CLOSE_BTN))
            welcome_close_btn.click()
            logging.info('Close Welcome dialog..')
            logging.info(f'Click on Close btn: "{WelcomeDialogLocators.CLOSE_BTN}"')
        except (TimeoutException, NoSuchElementException):
            pass


class SettingsFoldersPage(BasePage):
    URL = 'https://beta.protonmail.com/settings/labels'
    TITLE = 'Folders/labels - ProtonMail'

    def _find_item_by_name(self, name):
        """
        get all visible items, find needed by name
        :param name: item name
        :return: WebElement
        """
        all_items = self._get_all_items()
        needed = None
        for item in all_items:
            name_found = False
            try:
                name_found = item.find_element(SettingsFoldersLocators.ITEM_NAME[0],
                                               SettingsFoldersLocators.ITEM_NAME[1].format(name))
                logging.info(f'Found "{name_found.text}"')
            except NoSuchElementException:
                pass
            if name_found:
                needed = item
                break

        return needed

    def _get_all_items(self):
        """
        get all visible items
        :return: list of WebElement
        """
        _ = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            SettingsFoldersLocators.ITEMS_TABLE))

        all_items = self.driver.find_elements(*SettingsFoldersLocators.ITEM_ANY_TYPE)
        return all_items

    def _get_items_count(self):
        """
        get count of all visible items
        :return: int
        """
        items = self._get_all_items()
        return len(items) if items else 0

    def _get_item_index(self, name):
        """
        get all items, find needed by name and return its index.
        used for checking items display
        :param name:
        :return:
        """
        all_items = self._get_all_items()
        index = None
        for i, item in enumerate(all_items):
            name_found = False
            try:
                name_found = item.find_element(SettingsFoldersLocators.ITEM_NAME[0],
                                               SettingsFoldersLocators.ITEM_NAME[1].format(name))
                logging.info(f'Found "{name_found.text}"')
            except NoSuchElementException:
                pass
            if name_found:
                index = i
                break

        return index

    def add_folder(self, name, color):
        """
        Add new folder
        :param name:
        :param color:
        :return: True in case of success
        """
        logging.info(f'Add folder {name} with color {color}')
        add_folder_btn = self.driver.find_element(*SettingsFoldersLocators.ADD_FOLDER_BTN)
        add_folder_btn.click()
        logging.info(f'Click on Add Folder btn: "{SettingsFoldersLocators.ADD_FOLDER_BTN}"')

        folder_name = self.driver.find_element(*SettingsAddItemDialog.ITEM_NAME)
        folder_name.send_keys(name)
        logging.info(f'Send "{name}" to folder name: {SettingsAddItemDialog.ITEM_NAME}')

        color_elem = self.driver.find_element(*color)
        color_elem.click()
        logging.info(f'Click on color: "{color}"')

        submit_btn = self.driver.find_element(*SettingsAddItemDialog.SUBMIT)
        submit_btn.click()
        logging.info(f'Click on Submit: "{SettingsAddItemDialog.SUBMIT}"')

        return True

    def edit_folder(self, name, new_name, new_color):
        """
        Edit existing item
        :param name: curent name
        :param new_name: new name
        :param new_color: new color
        :return: True in case of success
        """
        item = self._find_item_by_name(name)
        if item:
            edit_btn = item.find_element(*SettingsFoldersLocators.EDIT_ITEM_BTN)
            edit_btn.click()
            logging.info(f'Click on Edit btn: {SettingsFoldersLocators.EDIT_ITEM_BTN}')

            folder_name = self.driver.find_element(*SettingsAddItemDialog.ITEM_NAME)
            folder_name.click()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            folder_name.send_keys(Keys.BACKSPACE)
            logging.info(f'Send "{name}" to folder name: {SettingsAddItemDialog.ITEM_NAME}')
            folder_name.send_keys(new_name)

            color_elem = self.driver.find_element(*new_color)
            color_elem.click()
            logging.info(f'Click on color: "{new_color}"')

            submit_btn = self.driver.find_element(*SettingsAddItemDialog.SUBMIT)
            submit_btn.click()
            logging.info(f'Click on Submit: "{SettingsAddItemDialog.SUBMIT}"')

    def delete_folder(self, name):
        """
        Deelte existing item
        :param name: name of item to delete
        :return: True in case of success
        """
        item = self._find_item_by_name(name)

        if item:
            dropdown_btn = item.find_element(*SettingsFoldersLocators.DROPDOWN_OPEN_BTN)
            dropdown_btn.click()
            logging.info(f'Click on Dropdown btn: "{SettingsFoldersLocators.DROPDOWN_OPEN_BTN}"')

        item_index = self._get_item_index(name)
        # can return 0, so need to compare with None
        # noinspection PyComparisonWithNone
        if item_index is None:
            logging.warning(f'Cannot get item index for "{name}"')
            return False
        # get all delete buttons
        delete_buttons = self.driver.find_elements(*SettingsFoldersLocators.DELETE_ITEM_BTN)
        if delete_buttons:
            delete_buttons[item_index].click()
            logging.info(f'Click on Delete btn: "{SettingsFoldersLocators.DELETE_ITEM_BTN}"')

            submit_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(SettingsDeleteItemDialog.SUBMIT))

            # submit_btn = self.driver.find_element(*SettingsDeleteItemDialog.SUBMIT)
            submit_btn.click()
            logging.info(f'Click on Submit btn: "{SettingsDeleteItemDialog.SUBMIT}"')
            return True

        else:
            logging.warning('Cannot get "delete" buttons')
            return False

    def item_is_displayed(self, name):
        item = self._find_item_by_name(name)
        return True if item else False

    def item_color_is_correct(self, name, color):
        item = self._find_item_by_name(name)
        if item:
            item_color = item.find_element(*SettingsFoldersLocators.ITEM_COLOR).get_attribute('style')
            logging.info(f'Item {name} color is {item_color}. Should be {color}')
            if item_color == color:
                return True
            else:
                return False
