"""
Module to create thread
Reading the output
"""
import threading
from robot import run
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from listener.robot_listener import QtRobotListener
from model.test_status import TestStatus

class TestService(QObject):
    """
    Processing on run test case
    Update test case status to main app
    Get the robotframework ouput
    """
    test_suite_started  = pyqtSignal(int)
    test_case_started   = pyqtSignal(str, str, str)
    test_case_waiting   = pyqtSignal(str, str, str)
    test_case_finished  = pyqtSignal(str, str, str)
    test_suite_finished = pyqtSignal()

    def __init__(self, robot_path: str = None):
        super().__init__()
        self.robot_path = robot_path
        self.current_thread = None

    def set_path(self, robot_path):
        """
        Update robot file or folder path when select new path.
        """
        self.robot_path = robot_path

    def run_selected_tests(self, root) -> None:
        """
        1. Get the checked test cases name and append it to a list
        2. Send signal Waiting for test case not currently running
        3. Disabled the run test button
        4. Send list of selected test cases name to execute_test()
        """

        # Create a list to contain all test cases name
        selected_tests = []

        # Get the names from the root parent
        self._collect_checked_test(root, selected_tests)

        if selected_tests:
            self.test_suite_started.emit(len(selected_tests))

            for test_name in selected_tests:
                state = TestStatus.WAITING
                self.test_case_waiting.emit(test_name, state.status, state.color)

            self.current_thread = threading.Thread(
                target=self._run_robot,
                args=(selected_tests,),
                daemon=True
            )
            self.current_thread.start()
        else:
            print("No tests selected.")

    def _collect_checked_test(self, item, selected_item):
        for row in range(item.rowCount()):
            child = item.child(row, 0)

            if child.rowCount() == 0 and child.checkState() == Qt.Checked:
                selected_item.append(child.data(Qt.UserRole))

            self._collect_checked_test(child, selected_item)

    def _run_robot(self, test_names):
        listener = QtRobotListener(self)

        run(
            self.robot_path,
            test=test_names,
            outputdir="report",
            listener=listener
        )

        self.test_suite_finished.emit()
