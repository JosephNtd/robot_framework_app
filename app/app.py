"""
Main app
"""
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFileDialog
from service.robot_handler import RobotHandler
from service.test_service import TestService
from ui.event import Event
from ui.top_layout import TestTreeTopLayout
from ui.bottom_layout import TestSummaryBottomLayout

class AutomationTestApp(QMainWindow):
    """
    Main app UI interaction
    """
    # Constants for UI strings
    WINDOW_TITLE            = "Automation test"
    WINDOW_SIZE             = (900, 900)
    MENU_FILE               = "File"
    MENU_FOLDER             = "Folder"
    MENU_ACTION_OPEN_FOLDER = "Open Folder"
    MENU_ACTION_OPEN_FILE   = "Open File"
    DIALOG_FILE_TITLE       = "Choose file"
    DIALOG_FOLDER_TITLE     = "Choose Folder"
    FILE_FILTER             = "All Files (*);;Robot Files (*.robot);;Text Files (*.txt)"

    def __init__(self,robot_file=None):
        super().__init__()

        # Assign .robot file to RobotHandler class
        self.runner = None
        self.test_service = None

        if robot_file:
            self.runner = RobotHandler(robot_file)

        self.test_service = TestService(self.runner.path if self.runner else None)

        self.event = Event(self) # Event class -> click expand/ contract/ check box
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

        self.top_layout = TestTreeTopLayout(self.runner)
        self.botom_layout = TestSummaryBottomLayout()

        self.main_layout.addWidget(self.top_layout)
        self.main_layout.addWidget(self.botom_layout)

        self.create_navigation_bar()
        self.event_handler()

    def event_handler(self):
        """
        Handle:
            User interaction with app interface
            All signal interaction from test case run background
        """
        self.top_layout.tree.clicked.connect(self.event.on_clicked_row_tree)
        self.top_layout.model.itemChanged.connect(self.event.on_item_changed)

        self.top_layout.btn_run_selected.clicked.connect(
            lambda: self.test_service.run_selected_tests(self.top_layout.model.invisibleRootItem())
        )

        self.test_service.test_suite_started.connect(self.botom_layout.reset_summary)
        self.test_service.test_suite_started.connect(self.top_layout.update_button_test_suite_started)
        self.test_service.test_case_waiting.connect(self.top_layout.update_test_cases_item)
        self.test_service.test_case_started.connect(self.top_layout.update_test_cases_item)
        self.test_service.test_case_finished.connect(self.top_layout.update_test_cases_item)
        self.test_service.test_case_finished.connect(
            lambda name, status, color: self.botom_layout.update_summary_result(status))
        self.test_service.test_suite_finished.connect(self.top_layout.update_test_suite_finished)

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
            self.DIALOG_FILE_TITLE,
            "",
            self.FILE_FILTER
        )

        if file_path:
            self.runner =RobotHandler(file_path)
            self.test_service.set_path(self.runner.path)
            self.top_layout.set_runner(self.runner)
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
            self.test_service.set_path(self.runner.path)
            self.top_layout.set_runner(self.runner)
            self.setWindowTitle(f"{self.WINDOW_TITLE} - {folder_path}")
