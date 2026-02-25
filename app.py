"""
Main app
"""
from PyQt5.QtWidgets import QMainWindow, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import Qt
from robot_handler import RobotHandler
from event import Event
from test_service import TestService

class AutomationTestApp(QMainWindow):
    """
    Main app UI interaction
    """
    # Constants for UI strings
    WINDOW_TITLE = "Automation test"
    WINDOW_SIZE = (900, 900)
    BUTTON_RUN_SELECTED = "Run Selected Test"
    BUTTON_START_APPIUM = "Start Appium"
    MENU_FILE = "File"
    MENU_FOLDER = "Folder"
    MENU_ACTION_OPEN_FOLDER = "Open Folder"
    MENU_ACTION_OPEN_FILE = "Open File"
    DIALOG_FILE_TITLE = "Choose file"
    DIALOG_FOLDER_TITLE = "Choose Folder"
    FILE_FILTER = "All Files (*);;Robot Files (*.robot);;Python Files (*.py);;Text Files (*.txt)"
    COLUMN_HEADERS = ["Test Setting", "Status"]

    # Constants for status display
    STATUS_STYLE = {
        "WAITING": ("Waiting...", "gray"),
        "RUNNING": ("Running...", "blue"),
        "PASS": ("PASS", "green"),
        "FAIL": ("FAIL", "red"),
    }
    def __init__(self,robot_file=None):
        super().__init__()

        # Assign .robot file to RobotHandler class
        self.runner = None
        if robot_file:
            self.runner = RobotHandler(robot_file)

        self.event = Event(self) # Event class -> click expand/ contract/ check box
        self.test_service = TestService(self)  # handle run test case, read ouput, return signal

        self.init_ui()

    def init_ui(self):
        """
        Main UI contain top and botton layout
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(*self.WINDOW_SIZE)

        self.main_layout = QVBoxLayout(central_widget)
        
        self.main_layout.addLayout(self.init_top_layout())
        self.main_layout.addLayout(self.init_bottom_layout())

        self.create_navigation_bar()
        self.event_handler()

    def init_bottom_layout(self) -> QVBoxLayout:
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignVCenter)

        self.total_test = QLabel("Total Test: 0")
        self.passed_test = QLabel("Test Passed: 0")
        self.failed_test = QLabel("Test Failed: 0")

        bottom_layout.addWidget(self.total_test)
        bottom_layout.addWidget(self.passed_test)
        bottom_layout.addWidget(self.failed_test)

        return bottom_layout

    def init_top_layout(self) -> QVBoxLayout:
        """
        Top layout contain test cases name and test cases status
        """
        layout = QVBoxLayout()

        self.tree = self.create_tree_view()

        self.btn_run_selected = QPushButton(self.BUTTON_RUN_SELECTED)

        layout.addWidget(self.tree)
        layout.addWidget(self.btn_run_selected)

        return layout

    def create_tree_view(self) -> QTreeView:
        """
        Create tree view to display test suite
        """
        tree = QTreeView()
        self.model = QStandardItemModel()
        tree.setModel(self.model)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.COLUMN_HEADERS)

        self._build_test_tree_items()
        return tree

    def _build_test_tree_items(self):
        """Build and populate test tree items from test cases"""
        if not self.runner:
            return

        self.tree.setColumnWidth(0, 750)
        self.tree.setColumnWidth(1, 100)

        root_item = self.model.invisibleRootItem()
        suite = self.runner.get_suite()

        self._add_suite_to_tree(suite, root_item)

        self.tree.expandAll()
        self.tree.header().setStretchLastSection(True)
    
    def _add_suite_to_tree(self, suite, parent_item):

        suite_item = QStandardItem(suite.name)
        suite_item.setCheckable(True)
        suite_item.setEditable(False)

        suite_status = QStandardItem()
        suite_status.setEditable(False)

        parent_item.appendRow([suite_item, suite_status])

        for test in suite.tests:
            test_item = QStandardItem(test.name)
            test_item.setCheckable(True)
            test_item.setEditable(False)

            test_status = QStandardItem()
            test_status.setEditable(False)

            suite_item.appendRow([test_item, test_status])

        for child_suite in suite.suites:
            self._add_suite_to_tree(child_suite, suite_item)

    def reload_new_tree(self):
        """
        Reload new tree, new test suites, test cases when select .robot file in dialog
        """
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.COLUMN_HEADERS)

        self._build_test_tree_items()

    def event_handler(self):
        """
        Handle:
            User interaction with app interface
            All signal interaction from test case run background
        """
        self.tree.clicked.connect(self.event.on_clicked_row_tree)
        self.model.itemChanged.connect(self.event.on_item_changed)

        self.btn_run_selected.clicked.connect(self.test_service.run_selected_tests)

        self.test_service.test_case_waiting.connect(self.update_test_cases_item)
        self.test_service.test_case_started.connect(self.update_test_cases_item)
        self.test_service.test_case_finished.connect(self.update_test_cases_item)
        self.test_service.test_suite_finished.connect(self.update_test_suite_finished)

    def create_navigation_bar(self):
        """
        Main app navigation bar
        """
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu(self.MENU_FILE)
        folder_menu = menu_bar.addMenu(self.MENU_FOLDER)

        file_action = file_menu.addAction(self.MENU_ACTION_OPEN_FILE)
        file_action.triggered.connect(self.show_file_dialog)

        folder_action = folder_menu.addAction(self.MENU_ACTION_OPEN_FOLDER)
        folder_action.triggered.connect(self.show_folder_dialog)

    def show_file_dialog(self):
        """
        Dialog show when select File on navigation bar
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.DIALOG_TITLE,
            "",
            self.FILE_FILTER
        )

        if file_path:
            self.runner =RobotHandler(file_path)
            self.reload_new_tree()
            self.setWindowTitle(f"{self.WINDOW_TITLE} - {file_path}")

    def show_folder_dialog(self):
        """
        Dialog show when select Folder on navigation bar
        """
        folder_path = QFileDialog.getExistingDirectory(
            self,
            self.DIALOG_FOLDER_TITLE,
            ""
        )

        if folder_path:
            self.runner = RobotHandler(folder_path)
            self.reload_new_tree()
            self.setWindowTitle(f"{self.WINDOW_TITLE} - {folder_path}")

    def update_test_cases_item(self, test_name, test_status, color):
        """
        Update test case status:
            Waiting:    Test case waiting to be execute
            Running:    Current test case executing
            Pass:       Test case that pass
            Failed:     Test case that failed
        """
        root_item = self.model.invisibleRootItem()
        suite_item = root_item.child(0, 0)
        if not suite_item:
            return

        for i in range(suite_item.rowCount()):
            item_name = suite_item.child(i, 0)
            item_status = suite_item.child(i, 1)

            if item_name.text() == test_name:
                item_status.setText(test_status)
                item_status.setForeground(QColor(color))

    def update_test_suite_finished(self):
        """
        Enable button run test case when every test cases is done executed
        """
        self.btn_run_selected.setEnabled(True)
