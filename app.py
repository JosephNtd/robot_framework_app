from PyQt5.QtWidgets import QTreeView, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from robot_handler import RobotHandler
from event import Event
from test_service import TestService
from appium_server import AppiumServer

class TreeView(QWidget):
    def __init__(self, robot_file):
        super().__init__()
        self.appium = AppiumServer()
        self.appium.start_server()
        self.runner = RobotHandler(robot_file)
        self.event = Event(self)
        self.test_service = TestService(self)

        self.init_ui()
        self.build_tree()

    def init_ui(self):
        self.setWindowTitle("Automation test")
        self.resize(400,300)
        layout = QVBoxLayout(self)


        self.tree = QTreeView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Test Setting"])
        self.tree.setModel(self.model)
        self.tree.setColumnWidth(0, 250)

        layout.addWidget(self.tree)

        btn_run_selected = QPushButton("Run Selected Test")
        btn_run_selected.clicked.connect(self.test_service.run_selected_tests)
        layout.addWidget(btn_run_selected)

        self.tree.clicked.connect(self.event.on_clicked_row_tree)

        self.model.itemChanged.connect(self.event.on_item_changed)

    def build_tree(self):
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

    def closeEvent(self, event):
        self.appium.stop_server()   
        event.accept()