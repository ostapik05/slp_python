from dotenv import load_dotenv
load_dotenv()

from labs.lab7.bll.Controller import Controller

import os
from labs.lab7.dal.JsonpickeHandler import handle
from labs.lab7.bll.GoogleBooksAPI import GoogleBooksAPI
from labs.lab7.ui.UserInterface import UserInterface
from labs.lab7.bll.InputParser import InputParser
from labs.lab7.dal.FileHandler import FileHandler
from labs.lab7.dal.SettingsModel import SettingsModel
from labs.lab7.dal.HistoryModel import HistoryModel
from labs.lab7.dal.UserSettingsModel import UserSettingsModel
from config.settings_paths import settings_path_lab7
from shared.services.relative_to_absolute_path import absolute


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
    controller = Controller(settings, history, user_settings, api)
    ui = UserInterface(controller)
    ui.show()