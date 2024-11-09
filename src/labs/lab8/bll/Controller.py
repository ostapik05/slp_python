from labs.lab8.bll.Plots import *
from labs.lab8.dal.SettingsModel import SettingsModel
from shared.services.relative_to_absolute_path import absolute
import logging
logger = logging.getLogger(__name__)

class Controller:
    def __init__(self, settings:SettingsModel, activity_data, sleep_data):
        self.settings = settings
        self.activity_data = activity_data
        self.sleep_data = sleep_data
        self.plot = None

    def get_default_save_dir(self):
        save_path = self.settings.get_assets_save_dir()
        path = absolute(save_path)
        return path

    def get_default_file_name(self):
        return self.settings.get_default_file_name()

    def steps_vs_calories(self):
        activity = self.activity_data
        self.plot = plot_steps_vs_calories(activity)

    def rem_and_bed_time(self):
        sleep = self.sleep_data
        self.plot = plot_rem_and_bed_time(sleep)

    def sleep_activity_relationships(self):
        activity = self.activity_data
        sleep = self.sleep_data
        self.plot = plot_sleep_activity_relationships(activity, sleep)

    def steps_by_date(self):
        activity = self.activity_data
        self.plot = plot_steps_by_date(activity)

    def steps_by_years(self):
        activity = self.activity_data
        self.plot = plot_steps_by_years(activity)

    def sleep_duration(self):
        activity = self.activity_data
        sleep = self.sleep_data
        self.plot = plot_sleep_duration(activity, sleep)

    def correlation_heatmap(self):
        activity = self.activity_data
        sleep = self.sleep_data
        self.plot = plot_correlation_heatmap(activity, sleep)

    def sleep_phases_distribution(self):
        sleep = self.sleep_data
        self.plot = plot_sleep_phases_distribution(sleep)

    def rem_sleep_vs_steps(self):
        activity = self.activity_data
        sleep = self.sleep_data
        self.plot = plot_rem_sleep_vs_steps(activity, sleep)

    def monthly_sleep_patterns(self):
        sleep = self.sleep_data
        self.plot = plot_monthly_sleep_patterns(sleep)

    def nap_days_per_month(self):
        sleep = self.sleep_data
        self.plot = plot_nap_days_per_month(sleep)

    def is_plot_exist(self):
        return self.plot is not None

    def show(self):
        self.plot.show()

    def save(self,file_path):
        if file_path:
            self.plot.savefig(file_path)
        self.plot.show()

    def get_logger_path(self):
        path = self.settings.get_logger_path()
        if not path:
            raise KeyError("There no logger path provided!")

        absolute_path = absolute(path)
        return absolute_path