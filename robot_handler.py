"""
Module use to run robotframework test file
subprocess output processing
"""
from robot.api import TestSuiteBuilder

class RobotHandler:
    """
    Handle backend with robot file: 
        + Get test case from robot file
        + Open a subprocess to run robot command to execute test cases
    """

    def __init__(self, path):
        self.path = path
        self.suite = TestSuiteBuilder().build(path)

    def get_suite(self):
        """
        Get test cases name from robot file to display on app interface
        """
        return self.suite