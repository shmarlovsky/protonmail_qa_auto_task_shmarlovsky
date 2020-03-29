import random

from selenium.webdriver.common.by import By


class LoginPageLocators:
    USERNAME_FIELD = (By.ID, 'username')
    PASSWORD_FIELD = (By.ID, 'password')


class WelcomeDialogLocators:
    CLOSE_BTN = (By.XPATH,
                 "//*/dialog[@class='onboardingModal-container pm-modal']"
                 "/header[@class='pm-modalHeader']/button[@class='pm-modalClose']")


class SettingsFoldersLocators:
    _buttons_div = "//*[@class='container-section-sticky-section']/div[@class='mb1']"
    ADD_FOLDER_BTN = (By.XPATH, f"{_buttons_div}"
                                "/button[@data-test-id='folders/labels:addFolder']")
    ADD_LABEL_BTN = (By.XPATH, f"{_buttons_div}"
                               "/button[@data-test-id='folders/labels:addLabel']")

    ITEMS_TABLE = (By.XPATH, "//*[@class='pm-simple-table orderableTable noborder border-collapse mt1']")
    ITEM_FOLDER_TYPE = (By.XPATH, "//*[@data-test-id='folders/labels:item-type:folder']")
    ITEM_LABEL_TYPE = (By.XPATH, "//*[@data-test-id='folders/labels:item-type:label']")
    ITEM_ANY_TYPE = (By.XPATH, f"{ITEM_LABEL_TYPE[1]} | {ITEM_FOLDER_TYPE[1]}")

    ITEM_NAME = (By.XPATH, ".//span[@data-test-id='folders/labels:item-name' and text()='{}']")
    ITEM_COLOR = (By.XPATH, ".//div/*[@class='icon-16p icon-16p flex-item-noshrink mr1 mtauto mbauto']")

    EDIT_ITEM_BTN = (By.XPATH, ".//button[@data-test-id='folders/labels:item-edit']")
    DROPDOWN_OPEN_BTN = (By.XPATH, ".//button[@data-test-id='dropdown:open']")
    DELETE_ITEM_BTN = (By.XPATH, ".//button[@data-test-id='folders/labels:item-delete']")
    NOTIFICATION_SUCCESS = (By.XPATH, ".//div[contains(@class,'notification-success') and text()='{}']")


class SettingsModalDialogLocators:
    HEADER = (By.XPATH, "//*[@class='pm-modalHeader']")
    ITEM_NAME = (By.XPATH, "//*[@data-test-id='label/folder-modal:name']")
    SUBMIT = (By.XPATH, "//*[@type='submit']")
    CANCEL = (By.XPATH, "//*[@type='reset']")


class ColorsLocators:
    RGB_114_114_167 = (By.XPATH, "//*[@data-test-id='color-selector:#7272a7']")
    RGB_137_137_172 = (By.XPATH, "//*[@data-test-id='color-selector:#8989ac']")
    RGB_207_88_88 = (By.XPATH, "//*[@data-test-id='color-selector:#cf5858']")
    RGB_207_126_126 = (By.XPATH, "//*[@data-test-id='color-selector:#cf7e7e']")
    RGB_194_108_199 = (By.XPATH, "//*[@data-test-id='color-selector:#c26cc7']")
    RGB_199_147_202 = (By.XPATH, "//*[@data-test-id='color-selector:#c793ca']")
    RGB_155_148_209 = (By.XPATH, "//*[@data-test-id='color-selector:#9b94d1']")
    RGB_105_169_209 = (By.XPATH, "//*[@data-test-id='color-selector:#69a9d1']")
    RGB_168_196_213 = (By.XPATH, "//*[@data-test-id='color-selector:#a8c4d5']")
    RGB_94_199_183 = (By.XPATH, "//*[@data-test-id='color-selector:#5ec7b7']")
    RGB_151_201_193 = (By.XPATH, "//*[@data-test-id='color-selector:#97c9c1']")
    RGB_114_187_117 = (By.XPATH, "//*[@data-test-id='color-selector:#72bb75']")
    RGB_157_185_159 = (By.XPATH, "//*[@data-test-id='color-selector:#9db99f']")
    RGB_195_210_97 = (By.XPATH, "//*[@data-test-id='color-selector:#c3d261']")
    RGB_198_205_151 = (By.XPATH, "//*[@data-test-id='color-selector:#c6cd97']")
    RGB_230_192_76 = (By.XPATH, "//*[@data-test-id='color-selector:#e6c04c']")
    RGB_231_210_146 = (By.XPATH, "//*[@data-test-id='color-selector:#e7d292']")
    RGB_230_152_76 = (By.XPATH, "//*[@data-test-id='color-selector:#e6984c']")
    RGB_223_178_134 = (By.XPATH, "//*[@data-test-id='color-selector:#dfb286']")

    @classmethod
    def get_random(cls):
        """
        get random color from all in this class
        :return: string. To get value use getattr()
        """
        all_ = [i for i in cls.__dict__ if not (i.startswith('__') or i.startswith('get'))]
        res = random.choice(all_)
        # res = getattr(cls, res)
        return res


class ColorsMap:
    RGB_114_114_167 = "color: rgb(114, 114, 167);"
    RGB_137_137_172 = "color: rgb(137, 137, 172);"
    RGB_207_88_88 = "color: rgb(207, 88, 88);"
    RGB_207_126_126 = "color: rgb(207, 126, 126);"
    RGB_194_108_199 = "color: rgb(194, 108, 199);"
    RGB_199_147_202 = "color: rgb(199, 147, 202);"
    RGB_155_148_209 = "color: rgb(155, 148, 209);"
    RGB_105_169_209 = "color: rgb(105, 169, 209);"
    RGB_168_196_213 = "color: rgb(168, 196, 213);"
    RGB_94_199_183 = "color: rgb(94, 199, 183);"
    RGB_151_201_193 = "color: rgb(151, 201, 193);"
    RGB_114_187_117 = "color: rgb(114, 187, 117);"
    RGB_157_185_159 = "color: rgb(157, 185, 159);"
    RGB_195_210_97 = "color: rgb(195, 210, 97);"
    RGB_198_205_151 = "color: rgb(198, 205, 151);"
    RGB_230_192_76 = "color: rgb(230, 192, 76);"
    RGB_231_210_146 = "color: rgb(231, 210, 146);"
    RGB_230_152_76 = "color: rgb(230, 152, 76);"
    RGB_223_178_134 = "color: rgb(223, 178, 134);"
