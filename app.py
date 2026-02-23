import threading
import time
from PyQt5.QtWidgets import QMainWindow, QTreeView, QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from robot_handler import RobotHandler
from event import Event
from test_service import TestService
from appium_server import AppiumServer

class AutomationTestApp(QMainWindow):
    def __init__(self, robot_file=None):
        super().__init__()

        self.runner = None
        if robot_file:
            self.runner = RobotHandler(robot_file)

        self.appium = AppiumServer()
        self.event = Event(self)
        self.test_service = TestService(self)

        self.create_app_interface()

    def event_handler(self):
        self.tree.clicked.connect(self.event.on_clicked_row_tree)
        self.model.itemChanged.connect(self.event.on_item_changed)

    def run_server(self):
        self.progressBar.setValue(0)

        thread = threading.Thread(
            target=self.appium.start_server,
            daemon=True,
            name='Start appium'
        )
        thread.start()

    def create_app_interface(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Automation test")
        self.resize(400,300)

        self.layout = QVBoxLayout(central_widget)

        self.progressBar = QProgressBar()
        self.btn_start_appium = QPushButton("Start Appium")

        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(self.btn_start_appium)

        self.btn_start_appium.clicked.connect(self.run_server)
        self.appium.progress_signal.connect(self.progressBar.setValue)
        self.appium.server_started.connect(self.after_connect_server)

        self.test_service.test_case_waiting.connect(self.update_test_cases_waiting)
        self.test_service.test_case_started.connect(self.update_test_cases_running)
        self.test_service.test_case_finished.connect(self.update_test_cases_finished)
        self.test_service.test_suite_finished.connect(self.update_test_suite_finished)

    def after_connect_server(self):
        self.layout.removeWidget(self.progressBar)
        self.layout.removeWidget(self.btn_start_appium)

        self.progressBar.deleteLater()
        self.btn_start_appium.deleteLater()

        self.progressBar = None
        self.btn_start_appium = None
        
        self.tree = self.create_tree_view()

        self.btn_run_selected = QPushButton("Run Selected Test")
        self.btn_run_selected.clicked.connect(self.test_service.run_selected_tests)

        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.btn_run_selected)

        self.create_navigation_bar()
        self.event_handler()

    def create_tree_view(self) -> QTreeView:
        self.tree = QTreeView()
        self.model = QStandardItemModel()
        self.tree.setModel(self.model)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Test Setting", "Status"])

        if self.runner:
            root_item = self.model.invisibleRootItem()

            suite_item = QStandardItem("Test Suite")
            suite_item.setCheckable(True)
            suite_item.setEditable(False)

            suite_status = QStandardItem()
            root_item.appendRow([suite_item, suite_status])

            test_names = self.runner.get_test_cases_name()

            for name in test_names:
                item_name = QStandardItem(name)
                item_name.setCheckable(True)
                item_name.setEditable(False)

                item_status = QStandardItem()
                item_status.setEditable(False)

                suite_item.appendRow([item_name, item_status])

            self.tree.expandAll()
            self.tree.header().setStretchLastSection(True)
        return self.tree

    def create_navigation_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        file_action = file_menu.addAction("Open File")
        file_action.triggered.connect(self.show_dialog)

    def show_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose file",
            "",
            "All Files (*);;Robot Files (*.robot);;Python Files (*.py);;Text Files (*.txt)"
        )

        if file_path:
            self.runner =RobotHandler(file_path)
            self.reload_new_tree()
            self.setWindowTitle(f"Automation test - {file_path}")

    def reload_new_tree(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Test Setting", "Status"])

        root_item = self.model.invisibleRootItem()

        suite_item = QStandardItem("Test Suite")
        suite_item.setCheckable(True)
        suite_item.setEditable(False)

        suite_status = QStandardItem()
        root_item.appendRow([suite_item, suite_status])

        test_names = self.runner.get_test_cases_name()

        for name in test_names:
            item_name = QStandardItem(name)
            item_name.setCheckable(True)
            item_name.setEditable(False)

            item_status = QStandardItem()
            item_status.setEditable(False)

            suite_item.appendRow([item_name, item_status])

        self.tree.expandAll()
        self.tree.header().setStretchLastSection(True)

    def update_test_cases_waiting(self, test_name):
        root_item = self.model.invisibleRootItem()
        suite_item = root_item.child(0, 0)
        if not suite_item:
            return

        for i in range(suite_item.rowCount()):
            item_name = suite_item.child(i, 0)
            item_status = suite_item.child(i, 1)

            if item_name.text() == test_name:
                item_status.setText("Waiting...")
                item_status.setForeground(QColor("gray"))

    def update_test_cases_running(self, test_name):
        root_item = self.model.invisibleRootItem()
        suite_item = root_item.child(0, 0)
        if not suite_item:
            return

        for i in range(suite_item.rowCount()):
            item_name = suite_item.child(i, 0)
            item_status = suite_item.child(i, 1)

            if item_name.text() == test_name:
                item_status.setText("Running...")
                item_status.setForeground(QColor("blue"))

    def update_test_cases_finished(self, test_name, status):
        root_item = self.model.invisibleRootItem()
        suite_item = root_item.child(0, 0)
        if not suite_item:
            return

        for i in range(suite_item.rowCount()):
            item_name = suite_item.child(i, 0)
            item_status = suite_item.child(i, 1)

            if item_name.text() == test_name:
                item_status.setText(status)

                if status == "PASS":
                    item_status.setForeground(QColor("green"))
                elif status == "FAIL":
                    item_status.setForeground(QColor("red"))
    
    def update_test_suite_finished(self):
        self.btn_run_selected.setEnabled(True)

    def closeEvent(self, event):
        self.appium.stop_server()
        event.accept()
