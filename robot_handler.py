import subprocess
from robot.api import TestSuiteBuilder, ExecutionResult

class RobotHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_test_cases_result(self):
        result = ExecutionResult('report/output.xml')
        return {t.name: t.status for t in result.suite.all_tests}

    def get_test_cases_name(self):
        suite = TestSuiteBuilder().build(self.file_path)
        test_cases = [test.name for test in suite.tests]
        return test_cases
    
    def run_robot_file(self, test_names=None):
        cmd = ["robot", "-d", "report"]

        if test_names:
            names = [test_names] if isinstance(test_names, str) else test_names
            for name in names:
                cmd += ["-t", name]

        cmd.append(self.file_path)

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        return process
