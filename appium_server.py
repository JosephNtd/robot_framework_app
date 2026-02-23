import subprocess
import requests
import time
from PyQt5.QtCore import pyqtSignal, QObject
from requests.exceptions import ConnectionError

class AppiumServer(QObject):

    progress_signal = pyqtSignal(int)
    server_started = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.appium_process = None

    def start_server(self) -> bool:
        if self.is_appium_server_alive():
            print("Server already running")
            self.server_started.emit()
            return True

        self.appium_process = subprocess.Popen(
            ["cmd", "/c", "appium"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            shell=True
        )

        start_time = time.time()

        progress = 0

        while progress < 90:
            progress += 1

            self.progress_signal.emit(progress)
            time.sleep(0.07)

        while True:
            if self.is_appium_server_alive():
                print("Appium server is alive and running.")
                self.progress_signal.emit(100)
                self.server_started.emit()
                return True
            
            if time.time() - start_time > 10:
                print("Appium server is not running or not responsive.")
                return False

            
            time.sleep(0.5)


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