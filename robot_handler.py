"""
Module use to run robotframework test file
subprocess output processing
"""
import subprocess
from robot.api import TestSuiteBuilder

class RobotHandler:
    """
    Handle backend with robot file: 
        + Get test case from robot file
        + Open a subprocess to run robot command to execute test cases
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def get_test_cases_name(self) -> list[str]:
        """
        Get test cases name from robot file to display on app interface
        """
        suite = TestSuiteBuilder().build(self.file_path)
        test_cases = [test.name for test in suite.tests]
        return test_cases

    def run_robot_file(self, test_names=None) -> subprocess.Popen:
        """
        Get test cases name from UI when user tick the checkbox
        Run command: robot -d "report" -t "test case 1" -t "test case n" file_name.robot

        Args:
            -d "directory name": Create directory to put all output file into this directory
            -t "test case name": Run specific test case base on its name
            file_name.robot: last is .robot file name
        """
        # Base command
        cmd = ["robot", "-d", "report"]

        # Append test case name into command
        if test_names:
            names = [test_names] if isinstance(test_names, str) else test_names
            for name in names:
                cmd += ["-t", name]

        # Append .robot file name into command
        cmd.append(self.file_path)

        # Create a subprocess to run command in cmd
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        return process
