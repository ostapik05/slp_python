from dotenv import load_dotenv
load_dotenv()
from labs.lab7.bll.Controller import Controller
import os
from labs.lab7.dal.JsonpickeHandler import handle
from labs.lab7.bll.GoogleBooksAPI import GoogleBooksAPI
from labs.lab7.ui.UserInterface import UserInterface
from labs.lab7.dal.SettingsModel import SettingsModel
from labs.lab7.dal.HistoryModel import HistoryModel
from labs.lab7.dal.UserSettingsModel import UserSettingsModel
from config.settings_paths import settings_path_lab7
from shared.services.relative_to_absolute_path import absolute
import logging


def set_up_logging(file_path):
    # Create a file handler
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.INFO)

    # Create a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)

    # Set the logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Configure the root logger
    logging.basicConfig(level=logging.DEBUG,
                        handlers=[file_handler, stream_handler])

def set_up_models():
    settings = SettingsModel(settings_path_lab7)
    relative_history_path = settings.get_history_path()
    relative_user_settings_path = settings.get_user_settings_path()
    results_to_save = settings.get_results_to_save()
    history_path = absolute(relative_history_path)
    user_settings_path = absolute(relative_user_settings_path)
    history = HistoryModel(history_path, results_to_save)
    user_settings = UserSettingsModel(user_settings_path)
    return settings, history, user_settings


def main():
    handle()
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    api = GoogleBooksAPI(api_key)
    settings, history, user_settings = set_up_models()
    logger_path = settings.get_logger_path()
    # Configure logging with the logger path from settings
    controller = Controller(settings, history, user_settings, api)
    logger_path = controller.get_logger_path()
    set_up_logging(logger_path)
    ui = UserInterface(controller)
    ui.show()