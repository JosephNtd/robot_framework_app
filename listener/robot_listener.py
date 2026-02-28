""" robot_listener.py """
from robot.api import logger
from model.test_status import TestStatus
class QtRobotListener:
    """ Handle all test status"""
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, service):
        logger.console("Listener initialized")
        self.service = service

    def start_test(self, data, result):
        """ Sending signal when a test case has started to update tc status to Running..."""
        logger.console(f"Test started: {data.longname}")
        test_name = data.longname
        state = TestStatus.RUNNING
        self.service.test_case_started.emit(test_name, state.status, state.color)

    def end_test(self, data, result):
        """ Sending signal when a test case has finished to update tc status to PASS/ FAILED"""
        logger.console(f"Test ended: {data.longname} - Status: {result.status}")
        test_name = data.longname
        status_key = result.status  # PASS or FAIL
        state = TestStatus[status_key]
        self.service.test_case_finished.emit(test_name, state.status, state.color)

    def end_suite(self, data, result):
        """ Sending signal when a test suite has started to update run tc button to enable"""
        self.service.test_suite_finished.emit()
