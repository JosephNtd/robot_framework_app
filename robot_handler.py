from robot.api import TestSuiteBuilder
from PyQt5.QtCore import QProcess
class RobotHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_test_cases_name(self):
        suite = TestSuiteBuilder().build(self.file_path)
        test_cases = [test.name for test in suite.tests]
        return test_cases
    
    def run_robot_file(self, parent, test_name=None):
        process = QProcess(parent)

        cmd = ["-d", "report"]

        if test_name:
            cmd += ["-t", test_name]
        
        cmd.append(self.file_path)
        
        return process, cmd