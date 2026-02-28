from PyQt5.QtWidgets import QTreeView, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import Qt

class TestTreeTopLayout(QWidget):
    """
    Bottom layout contain test case name, status infomation
    Update info at every test cases started, finished
    """
    BUTTON_RUN_SELECTED = "Run Selected Test"
    COLUMN_HEADERS      = ["Test Setting", "Status"]

    def __init__(self, runner):
        super().__init__()

        self.runner = runner

        self.tree = QTreeView()
        self.model = QStandardItemModel()
        self.btn_run_selected = QPushButton(self.BUTTON_RUN_SELECTED)

        self.init_top_layout()

    def init_top_layout(self):
        """
        Top layout contain test cases name and test cases status
        """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet("""
            QWidget{
                background-color: #FFF2E1;
            }
            QStandardItemModel{
                background-color: #A79277
            }
            QPushButton{
                color: white;
                background-color: #A79277
            }
        """)

        self.create_tree_view()

        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.btn_run_selected)

    def create_tree_view(self) -> QTreeView:
        """
        Create tree view to display test suite
        """
        self.tree.setModel(self.model)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.COLUMN_HEADERS)

        self._build_test_tree_items()

    def _build_test_tree_items(self):
        """Build and populate test tree items from test cases"""
        if not self.runner:
            return

        self.tree.setColumnWidth(0, 750)
        self.tree.setColumnWidth(1, 100)

        root_item = self.model.invisibleRootItem()
        suite = self.runner.get_suite

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
            test_item.setData(test.longname, Qt.UserRole)
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

    def update_test_cases_item(self, test_name, test_status, color):
        """
        Update test case status:
            Waiting:    Test case waiting to be execute
            Running:    Current test case executing
            Pass:       Test case that pass
            Failed:     Test case that failed
        """
        def update_multi_tree(item):
            for i in range(item.rowCount()):
                item_name = item.child(i, 0)
                item_status = item.child(i, 1)

                # Nếu là test case (leaf node)
                if item_name.rowCount() == 0:
                    if item_name.data(Qt.UserRole) == test_name:
                        item_status.setText(test_status)
                        item_status.setForeground(QColor(color))

                        return True  # tìm thấy rồi -> thoát
                else:
                    # Nếu là suite -> tìm tiếp bên trong
                    if update_multi_tree(item_name):
                        return True

            return False  # chỉ return False sau khi duyệt hết for

        root_item = self.model.invisibleRootItem()
        update_multi_tree(root_item)

    def update_test_suite_finished(self):
        """
        Enable button run test case when every test cases is done executed
        """
        self.btn_run_selected.setEnabled(True)

    def update_button_test_suite_started(self):
        """ Disable when test suite started to prevent click while executing"""
        self.btn_run_selected.setEnabled(False)

    def set_runner(self, runner):
        """ Set new runner path to re-create tree for that path"""
        self.runner = runner
        self.reload_new_tree()
