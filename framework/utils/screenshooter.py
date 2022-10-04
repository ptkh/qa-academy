# coding=utf-8
import os
import threading
from datetime import datetime
from PIL import Image
from framework.browser.browser import Browser
from framework.constants import screenshots
from framework.utils.datetime_util import DatetimeUtil
from framework.utils.logger import Logger


class Screenshooter:
    __session_dir = None
    __screen_number = screenshots.NUMBER_OF_FIRST_SCREEN
    __screen_dir = os.path.join(os.getcwd(), screenshots.PATH_TO_SCREENSHOTS)

    @staticmethod
    def set_session_screen_dir():
        lock = threading.Lock()
        lock.acquire()
        try:
            if not os.path.exists(Screenshooter.__screen_dir):
                Logger.info("Создание дирректории для хранения скриншотов: " + Screenshooter.__screen_dir)
                os.makedirs(Screenshooter.__screen_dir)

            new_screen_path = os.path.join(
                Screenshooter.__screen_dir,
                "Session_" + DatetimeUtil.get_str_datetime(screenshots.FORMAT_DATETIME_FOR_SCREEN))

            if Screenshooter.__session_dir is None and not os.path.exists(new_screen_path):
                Screenshooter.__session_dir = new_screen_path
            else:
                Screenshooter.__session_dir = new_screen_path + "." + str(datetime.now().microsecond)

            Logger.info("Создание дирректории " + new_screen_path)
            os.makedirs(Screenshooter.__session_dir)
        finally:
            lock.release()

    @staticmethod
    def get_screen_file_name(file_format=screenshots.FILE_FORMAT_PNG):
        scr_number = str(Screenshooter.__screen_number)
        Screenshooter.__screen_number += 1
        return "Screenshot_" + scr_number + file_format

    @staticmethod
    def take_screenshot():
        screen_name = Screenshooter.get_screen_file_name()
        save_screen_path = os.path.join(Screenshooter.__session_dir, screen_name)

        Logger.info("Снятие скриншота экрана в файл " + screen_name)
        Browser.get_browser().get_driver().save_screenshot(save_screen_path)
        result_image = Image.open(save_screen_path)
        # Logger.info(VisualRecord(screen_name, result_image))
