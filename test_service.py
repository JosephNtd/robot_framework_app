"""
Module to create thread
Reading the output
"""
import threading
from PyQt5.QtCore import Qt, QObject, pyqtSignal

class TestService(QObject):
    """
    Processing on run test case
    Update test case status to main app
    Get the robotframework ouput
    """
    test_case_started = pyqtSignal(str, str, str)
    test_case_waiting = pyqtSignal(str, str, str)
    test_case_finished = pyqtSignal(str, str, str)
    test_suite_finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.processes = []

    def run_selected_tests(self) -> None:
        """
        1. Get the checked test cases name and append it to a list
        2. Send signal Waiting for test case not currently running
        3. Disabled the run test button
        4. Send list of selected test cases name to execute_test()
        """

        # Create a list to contain all test cases name
        selected_tests = []

        # Get the names from the root parent
        root = self.parent.model.invisibleRootItem()
        suite_item = root.child(0, 0)

        for i in range(suite_item.rowCount()):
            test_name_item = suite_item.child(i, 0)
            if test_name_item.checkState() == Qt.Checked:
                status, color = self.parent.STATUS_STYLE["WAITING"]
                self.test_case_waiting.emit(test_name_item.text(), status, color)
                selected_tests.append(test_name_item.text())

        if selected_tests:
            self.parent.btn_run_selected.setEnabled(False)
            self.execute_test(selected_tests)
        else:
            print("No tests selected.")

    def execute_test(self, test_names=None):
        """
        Excute selected test cases by running run_robot_file() from Appium Server class
        """
        process = self.parent.runner.run_robot_file(test_names)

        self.processes.append(process)

        threading.Thread(
            target=self.read_process_output,
            args=(process,),
            daemon=True
        ).start()

    def read_process_output(self, process):
        """
        Read & print the robotframework output process to cmd
        """
        for line in process.stdout:
            print(line.strip())

            if "|" not in line and line:
                status, color = self.parent.STATUS_STYLE["RUNNING"]
                self.test_case_started.emit(line, status, color)

            if "|" in line and ("PASS" in line or "FAIL" in line):
                parts = line.split("|")
                if len(parts) >= 2:
                    test_name = parts[0].strip()
                    status = parts[1].strip()
                    status, color = self.parent.STATUS_STYLE[status]
                    self.test_case_finished.emit(test_name, status, color)
        
        process.wait()
        if process in self.processes:
            self.processes.remove(process)

        self.test_suite_finished.emit() # Báo main thread test đã chạy xong