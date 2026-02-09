import sys
from PyQt5.QtWidgets import QApplication, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QProcess
from robot.api import TestSuiteBuilder

def get_test_cases_name(file_path):
    suite = TestSuiteBuilder().build(file_path)
    test_cases = [test.name for test in suite.tests]
    return test_cases

class TreeView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automation test")
        self.resize(400,300)

        layout = QVBoxLayout(self)

        self.tree = QTreeView()
        layout.addWidget(self.tree)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Test Setting", "Action"])

        self.tree.setModel(self.model)
        self.tree.setColumnWidth(0, 250)
        self.tree.setColumnWidth(1, 100)

        self.build_tree()
        self.tree.expandAll()
        
    def build_tree(self):
        parent = QStandardItem("Test suite")
        parent.setEditable(False)

        parent_action_btn = QStandardItem()
        self.model.appendRow([parent, parent_action_btn])

        parent_index = self.model.indexFromItem(parent_action_btn)
        self.tree.setIndexWidget(
            parent_index,
            self.button("Run All", None)
        )

        test_names = get_test_cases_name("test_setting.robot")

        for name in test_names:
            childen = QStandardItem(name)
            childen.setEditable(False)

            children_action_btn = QStandardItem()
            parent.appendRow([childen, children_action_btn])

            child_index = self.model.indexFromItem(children_action_btn)
            self.tree.setIndexWidget(
                child_index,
                self.button("Run", name)
            )

    def button(self, text, test_name):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        btn = QPushButton(text)
        btn.setFixedWidth(80)
        btn.clicked.connect(
            lambda _, t=test_name: self.run_robot_file(t)
        )

        layout.addWidget(btn)
        layout.setAlignment(Qt.AlignCenter)
        return widget

    def run_robot_file(self, test_name=None):
        cmd = ["robot"]

        if test_name:
            cmd += ["-t", test_name]
        
        cmd.append("test_setting.robot")
        
        process = QProcess(self)

        process.readyReadStandardOutput.connect(
            lambda: print(process.readAllStandardOutput().data().decode())
        )
        process.finished.connect(
            lambda: print(f"Kết thúc: {test_name if test_name else 'All'}")
        )

        process.start("robot", cmd[1:])
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TreeView()
    window.show()
    sys.exit(app.exec_())