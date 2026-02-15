import threading
from PyQt5.QtCore import Qt
from appium_server import AppiumServer

class TestService():
    def __init__(self, parent):
        self.parent = parent
        self.appium_server = AppiumServer()
        self.processes = []

    def run_selected_tests(self):
        selected_tests = []
        root = self.parent.model.invisibleRootItem()
        suite_item = root.child(0, 0)

        for i in range(suite_item.rowCount()):
            child = suite_item.child(i, 0)
            if child.checkState() == Qt.Checked:
                selected_tests.append(child.text())
        
        if selected_tests:
            self.execute_test(selected_tests)
        else:
            print("No tests selected.")

    def execute_test(self, test_names=None):
        process = self.parent.runner.run_robot_file(test_names)

        self.processes.append(process)

        threading.Thread(
            target=self.read_process_output,
            args=(process,),
            daemon=True
        ).start()

    def read_process_output(self, process):
        for line in process.stdout:
            print(line.strip())
        
        process.wait()
        if process in self.processes:
            self.processes.remove(process)
