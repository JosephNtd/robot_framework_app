import subprocess
import requests
from PyQt5.QtCore import pyqtSignal, QObject
from requests.exceptions import ConnectionError

class AppiumServer(QObject):

    progress_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.appium_process = None

    def start_server(self):
        process = subprocess.Popen(
            ["cmd", "/c", "appium"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True
        )

        self.progress_signal.emit(30)

        for line in process.stdout:
            print(line.strip())
            if "listener started" in line.lower():
                self.progress_signal.emit(100)
                break

    def stop_server(self):
        subprocess.Popen(
            'taskkill /f /im node.exe',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

    def is_appium_server_alive(self, host='127.0.0.1', port=4723):
        """
        Checks if the Appium server is alive by sending a status request.
        
        Args:
            host: The Appium server host.
            port: The Appium server port.

        Returns:
            True if the server is running and responsive, False otherwise.
        """
        url = f"http://{host}:{port}/status"

        try:
            response = requests.get(url, timeout=5)
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                return True
            else:
                return False
        except ConnectionError:
            # This exception is raised if the server is not reachable
            return False
        except requests.exceptions.RequestException as e:
            # Handle other potential request exceptions
            print(f"An error occurred while checking Appium server status: {e}")
            return False