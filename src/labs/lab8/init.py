import pandas as pd
from shared.services.relative_to_absolute_path import absolute
from labs.lab8.dal.SettingsModel import SettingsModel
from config.settings_paths import settings_path_lab8
from labs.lab8.bll.Controller import Controller
from labs.lab8.ui.UserInterface import UserInterface

def main():
    settings = SettingsModel(settings_path_lab8)
    relative_activity_path = settings.get_activity_file_path()
    relative_sleep_path = settings.get_sleep_file_path()
    activity_path = absolute(relative_activity_path)
    sleep_path = absolute(relative_sleep_path)
    activity = pd.read_csv(activity_path)
    sleep = pd.read_csv(sleep_path)
    controller = Controller(settings, activity, sleep)
    user_interface = UserInterface(controller)
    user_interface.show()


if __name__ == "__main__":
    main()
