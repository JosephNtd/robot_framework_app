from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

class TestSummaryBottomLayout(QWidget):
    """
    Bottom layout contain test case summary infomation
    Update info at every test cases finished
    """
    TOTAL_TEST_COUNT    = "Total Test: "
    PASSED_TEST_COUNT   = "Test Passed: "
    FAILED_TEST_COUNT   = "Test Failed: "

    def __init__(self):
        super().__init__()

        self.total_count = 0
        self.pass_count = 0
        self.fail_count = 0

        self.init_bottom_layout()

    def init_bottom_layout(self):
        """
        Initialize main layout
        """
        bottom_layout = QHBoxLayout()

        self.setLayout(bottom_layout)

        bottom_layout.setAlignment(Qt.AlignVCenter)

        self.total_test = QLabel(f"{self.TOTAL_TEST_COUNT}{self.total_count}")
        self.passed_test = QLabel(f"{self.PASSED_TEST_COUNT}{self.pass_count}")
        self.failed_test = QLabel(f"{self.FAILED_TEST_COUNT}{self.fail_count}")

        bottom_layout.addWidget(self.total_test)
        bottom_layout.addWidget(self.passed_test)
        bottom_layout.addWidget(self.failed_test)


    def reset_summary(self, total):
        """
        Reset the summary when new suite being executed
        """
        self.total_count = total
        self.pass_count = 0
        self.fail_count = 0

        self.total_test.setText(f"{self.TOTAL_TEST_COUNT}{self.total_count}")
        self.passed_test.setText(f"{self.PASSED_TEST_COUNT}{self.pass_count}")
        self.failed_test.setText(f"{self.FAILED_TEST_COUNT}{self.fail_count}")

    def update_summary_result(self, test_status):
        """
        Update test case status:
            Waiting:    Test case waiting to be execute
            Running:    Current test case executing
            Pass:       Test case that pass
            Failed:     Test case that failed
        """
        if test_status == "PASS":
            self.pass_count += 1
            self.passed_test.setText(f"{self.PASSED_TEST_COUNT}{self.pass_count}")

        elif test_status == "FAIL":
            self.fail_count += 1
            self.failed_test.setText(f"{self.FAILED_TEST_COUNT}{self.fail_count}")
