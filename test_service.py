import threading
from PyQt5.QtCore import Qt, QObject, pyqtSignal

class TestService(QObject):
    test_case_started = pyqtSignal(str)
    test_case_waiting = pyqtSignal(str)
    test_case_finished = pyqtSignal(str, str)
    test_suite_finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.processes = []

    def run_selected_tests(self):
        selected_tests = []
        root = self.parent.model.invisibleRootItem()
        suite_item = root.child(0, 0)

        for i in range(suite_item.rowCount()):
            test_name_item = suite_item.child(i, 0)
            if test_name_item.checkState() == Qt.Checked:
                self.test_case_waiting.emit(test_name_item.text())
                selected_tests.append(test_name_item.text())
        
        if selected_tests:
            self.parent.btn_run_selected.setEnabled(False)
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

            if "|" not in line and line:
                self.test_case_started.emit(line)

            if "|" in line and ("PASS" in line or "FAIL" in line):
                parts = line.split("|")
                if len(parts) >= 2:
                    test_name = parts[0].strip()
                    status = parts[1].strip()
                    self.test_case_finished.emit(test_name, status)
        
        process.wait()
        if process in self.processes:
            self.processes.remove(process)

        self.test_suite_finished.emit() # Báo main thread test đã chạy xong