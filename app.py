import sys
from PyQt5.QtWidgets import QApplication, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from robot_handler import RobotHandler
from ui_component import ActionButton

class TreeView(QWidget):
    def __init__(self, robot_file):
        super().__init__()
        self.runner = RobotHandler(robot_file)
        self.processes = []

        self.init_ui()
        self.build_tree()

    def init_ui(self):
        self.setWindowTitle("Automation test")
        self.resize(400,300)
        layout = QVBoxLayout(self)

        self.tree = QTreeView() 
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Test Setting", "Action"])
        self.tree.setModel(self.model)
        self.tree.setColumnWidth(0, 250)
        self.tree.setColumnWidth(1, 100)

        layout.addWidget(self.tree)
        
    def add_tree_row(self, parent_item, lable, test_name):
        item_name = QStandardItem(lable)
        item_name.setEditable(False)

        action_item = QStandardItem()
        parent_item.appendRow([item_name, action_item])
        
        btn_text = "Run All" if test_name is None else "Run"
        btn_widget = ActionButton(btn_text, lambda: self.execute_test(test_name))

        self.tree.setIndexWidget(self.model.indexFromItem(action_item), btn_widget)

    def execute_test(self, test_name):
        proc, cmd = self.runner.run_robot_file(self, test_name)
        self.processes.append(proc)

        proc.readyReadStandardOutput.connect(
            lambda p=proc: print(p.readAllStandardOutput().data().decode())
        )
        proc.finished.connect(
        lambda _, p=proc: self.processes.remove(p) if p in self.processes else None
        )

        proc.start("robot", cmd)

    def build_tree(self):
        root_item = self.model.invisibleRootItem()

        suite_item = QStandardItem("Test Suite")
        suite_action = QStandardItem()
        root_item.appendRow([suite_item, suite_action])

        all_btn = ActionButton("Run All", lambda: self.execute_test(None))

        suite_index = self.model.indexFromItem(suite_action)
        self.tree.setIndexWidget(suite_index, all_btn)

        test_names = self.runner.get_test_cases_name()

        for name in test_names:
            self.add_tree_row(suite_item, name, name)

        self.tree.expandAll()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TreeView("test_setting.robot")
    window.show()
    sys.exit(app.exec_())