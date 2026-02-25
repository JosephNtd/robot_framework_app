# robot_listener.py
from robot.api import logger
class QtRobotListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, service):
        logger.console("Listener initialized")
        self.service = service

    def start_test(self, data, result):
        logger.console(f"Test started: {data.name}")
        test_name = data.name
        status, color = self.service.parent.STATUS_STYLE["RUNNING"]
        self.service.test_case_started.emit(test_name, status, color)

    def end_test(self, data, result):
        logger.console(f"Test ended: {data.name} - Status: {result.status}")
        test_name = data.name
        status_key = result.status  # PASS or FAIL
        status, color = self.service.parent.STATUS_STYLE[status_key]
        self.service.test_case_finished.emit(test_name, status, color)

    def end_suite(self, data, result):
        self.service.test_suite_finished.emit()