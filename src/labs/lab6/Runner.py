from config.settings_paths import current_dir
from shared.interfaces.RunnerInterface import RunnerInterface
from tests.Calculator_lab2_bll_test import CalculatorBllTest
from os import path
import unittest
import subprocess

TIMEOUT = 10
def run_in_new_terminal():
    test_path = path.join('tests', 'Calculator_lab2_bll_test.py')
    # parent_dir = path.abspath(path.join(current_dir, '../../'))

    command = f'python {test_path} & timeout /t {TIMEOUT} & exit'
    subprocess.Popen(['start', 'cmd', '/C', command], shell=True, cwd=current_dir)

class Runner(RunnerInterface):
    @staticmethod
    def run():
        run_in_new_terminal()

