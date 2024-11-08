from shared.classes.MenuBuilder import MenuBuilder
from labs.lab8.bll.Controller import Controller
from shared.classes.Input import BoolInput
import tkinter as tk
from tkinter import filedialog
import pyautogui

class UserInterface:
    def __init__(self, controller: Controller):
        self.controller = controller

        self.main_menu = self.build_main()

    def show(self):
        self.main_menu.show()

    def build_main(self):
        menu = (MenuBuilder()
                .set_title("Sleep and activity data visualization")
                .add_option("1", "\n1. Steps vs calories", self.steps_vs_calories)
                .add_option("2", "\n2. REM and bed time", self.rem_and_bed_time)
                .add_option("3", "\n3. Sleep and activity relationships", self.sleep_activity_relationships)
                .add_option("4", "\n4. Total steps", self.steps_by_date)
                .add_option("5", "\n5. Total steps by years", self.steps_by_years)
                .add_option("6", "\n6. Sleep duration", self.sleep_duration)
                .add_option("7", "\n7. Correlation heatmap", self.correlation_heatmap)
                .add_option("8", "\n8. Sleep phases distribution", self.sleep_phases_distribution)
                .add_option("9", "\n9. REM sleep vs steps", self.rem_sleep_vs_steps)
                .add_option("10", "\n10. Monthly sleep pattern", self.monthly_sleep_patterns)
                .add_option("11", "\n11. Nap days in month", self.nap_days_per_month)
                .add_stop_options(["0", "Exit", "exit", "e", "q"], "0. Exit")
                .build())
        return menu

    def steps_vs_calories(self):
        self.controller.steps_vs_calories()
        self.want_to_save()

    def rem_and_bed_time(self):
        self.controller.rem_and_bed_time()
        self.want_to_save()

    def sleep_activity_relationships(self):
        self.controller.sleep_activity_relationships()
        self.want_to_save()

    def steps_by_date(self):
        self.controller.steps_by_date()
        self.want_to_save()

    def steps_by_years(self):
        self.controller.steps_by_years()
        self.want_to_save()

    def sleep_duration(self):
        self.controller.sleep_duration()
        self.want_to_save()

    def correlation_heatmap(self):
        self.controller.correlation_heatmap()
        self.want_to_save()

    def sleep_phases_distribution(self):
        self.controller.sleep_phases_distribution()
        self.want_to_save()

    def rem_sleep_vs_steps(self):
        self.controller.rem_sleep_vs_steps()
        self.want_to_save()

    def monthly_sleep_patterns(self):
        self.controller.monthly_sleep_patterns()
        self.want_to_save()

    def nap_days_per_month(self):
        self.controller.nap_days_per_month()
        self.want_to_save()

    def want_to_save(self):
        true_options = ["yes", "y", "+"]
        false_options = ["no", "n", "-"]
        message = "Do you want to save (yes/no)?"
        warning_message = f"There no such option. {",".join(true_options + false_options)} only"
        is_want = BoolInput.input(message, [true_options, false_options],warning_message)
        if is_want:
            self.save()
        else:
            self.controller.show()

    def get_results(self):
        if not self.controller.is_plot_exist():
            return "No plot yet"
        self.controller.show()
        return "Shown"

    def save(self):
        if not self.controller.is_plot_exist():
            print("No plot yet")
            return
        file_path = self.save_file_dialog()
        extensions = ['.png', '.pdf', '.svg']
        if not file_path.endswith(tuple(extensions)):
            print("Invalid file extension!")
            return
        if file_path == "":
            print("Empty filepath!")
        self.controller.save(file_path)

    def save_file_dialog(self):
        root = tk.Tk()
        root.withdraw()
        default_name = self.controller.get_default_file_name()
        default_path = self.controller.get_default_save_dir()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                       ("PDF files", "*.pdf"),
                       ("SVG files", "*.svg")],
            initialfile=default_name,
            initialdir=default_path,
            title="Save. You can choose .png, .pdf or .svg file types. "
        )
        root.destroy()
        return file_path or ""
