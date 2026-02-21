import threading
import time
from PyQt5.QtWidgets import QMainWindow, QTreeView, QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
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

        thread = threading.Thread(target=self.appium.start_server)
        thread.start()

    def create_app_interface(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Automation test")
        self.resize(400,300)

        layout = QVBoxLayout(central_widget)

        self.progressBar = QProgressBar()
        self.btn_start_appium = QPushButton("Start Appium")

        layout.addWidget(self.progressBar)
        layout.addWidget(self.btn_start_appium)

        self.btn_start_appium.clicked.connect(self.run_server)
        self.appium.progress_signal.connect(self.progressBar.setValue)

        check_appium_flag, information_print = self.check_appium_server()
        time.sleep(10)
        if check_appium_flag:
            print(information_print)
            self.tree = self.create_tree_view()

            btn_run_selected = QPushButton("Run Selected Test")
            btn_run_selected.clicked.connect(self.test_service.run_selected_tests)

            layout.addWidget(self.tree)
            layout.addWidget(btn_run_selected)

            self.create_navigation_bar()
            self.event_handler()
        else:
            print(information_print)

    def create_tree_view(self) -> QTreeView:
        self.tree = QTreeView()
        self.model = QStandardItemModel()
        self.tree.setModel(self.model)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Test Setting"])

        if self.runner:
            root_item = self.model.invisibleRootItem()

            suite_item = QStandardItem("Test Suite")
            suite_item.setCheckable(True)
            suite_item.setEditable(False)

            root_item.appendRow([suite_item])

            test_names = self.runner.get_test_cases_name()

            for name in test_names:
                item_name = QStandardItem(name)
                item_name.setCheckable(True)
                item_name.setEditable(False)

                suite_item.appendRow([item_name])

            self.tree.expandAll()

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
        self.model.setHorizontalHeaderLabels(["Test Setting"])

        root_item = self.model.invisibleRootItem()

        suite_item = QStandardItem("Test Suite")
        suite_item.setCheckable(True)
        suite_item.setEditable(False)

        root_item.appendRow([suite_item])

        test_names = self.runner.get_test_cases_name()

        for name in test_names:
            item_name = QStandardItem(name)
            item_name.setCheckable(True)
            item_name.setEditable(False)

            suite_item.appendRow([item_name])

        self.tree.expandAll()

    def check_appium_server(self) -> tuple[bool, str]:
        if self.appium.is_appium_server_alive():
            return True, "Appium server is alive and running."
        else:
            return False, "Appium server is not running or not responsive."

    def closeEvent(self, event):
        self.appium.stop_server()
        event.accept()
