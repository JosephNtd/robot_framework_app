from PyQt5.QtWidgets import QMainWindow, QTreeView, QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from robot_handler import RobotHandler
from event import Event
from test_service import TestService

class AutomationTestApp(QMainWindow):
    """
    Main app UI interaction
    """
    # Constants for UI strings
    WINDOW_TITLE = "Automation test"
    WINDOW_SIZE = (400, 300)
    BUTTON_RUN_SELECTED = "Run Selected Test"
    BUTTON_START_APPIUM = "Start Appium"
    MENU_FILE = "File"
    MENU_ACTION_OPEN = "Open File"
    DIALOG_TITLE = "Choose file"
    FILE_FILTER = "All Files (*);;Robot Files (*.robot);;Python Files (*.py);;Text Files (*.txt)"
    COLUMN_HEADERS = ["Test Setting", "Status"]
    SUITE_ITEM_NAME = "Test Suite"

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

        self.create_app_interface()

    def create_app_interface(self):
        """
        Main UI when open app
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(*self.WINDOW_SIZE)

        self.layout = QVBoxLayout(central_widget)

        self.tree = self.create_tree_view()

        self.btn_run_selected = QPushButton(self.BUTTON_RUN_SELECTED)

        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.btn_run_selected)

        self.create_navigation_bar()
        self.event_handler()

    def create_tree_view(self) -> QTreeView:
        self.tree = QTreeView()
        self.model = QStandardItemModel()
        self.tree.setModel(self.model)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.COLUMN_HEADERS)

        self._build_test_tree_items()
        return self.tree

    def _build_test_tree_items(self):
        """Build and populate test tree items from test cases"""
        if not self.runner:
            return
        
        root_item = self.model.invisibleRootItem()

        suite_item = QStandardItem(self.SUITE_ITEM_NAME)
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

    def create_navigation_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu(self.MENU_FILE)

        file_action = file_menu.addAction(self.MENU_ACTION_OPEN)
        file_action.triggered.connect(self.show_dialog)

    def show_dialog(self):
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

    def reload_new_tree(self):
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

    def update_test_cases_item(self, test_name, test_status, color):
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
        self.btn_run_selected.setEnabled(True)
