"""
use to manage status string value
"""
from enum import Enum

class TestStatus(Enum):
    """
    Contain test status constraint to use in test_service, robot_listener
    """
    WAITING = ("Waiting...", "gray")
    RUNNING = ("Running...", "blue")
    PASS = ("PASS", "green")
    FAIL = ("FAIL", "red")

    @property
    def status(self):
        """ Return test status"""
        return self.value[0]

    @property
    def color(self):
        """ Retur status color """
        return self.value[1]
