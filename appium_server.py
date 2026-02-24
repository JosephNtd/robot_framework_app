"""
Module use to run appium server
and kill appium server
"""
import subprocess
import time
import requests
from PyQt5.QtCore import QObject, pyqtSignal
from requests.exceptions import ConnectionError

class AppiumServer(QObject):
    """
    Handle interaction with appium server
    """
    server_started = pyqtSignal()

    def start_server(self) -> None:
        """
        Check appium is running or not
        Sending signal to update progress bar in UI
        Create a subprocess to run appium server in cmd
        """
        # If appium is already running -> return
        if self.is_appium_server_alive():
            print("Server already running")
            self.server_started.emit()
            return

        #  If not -> Create a subprocess to run appium server in cmd
        subprocess.Popen(
            ["cmd", "/c", "appium"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            shell=True
        )

        #  Create time to countdown server started, if exceed 10s -> break
        start_time = time.time()

        while True:
            if self.is_appium_server_alive():
                print("Appium server is alive and running.")
                self.server_started.emit()
                break

            if time.time() - start_time > 10:
                print("Appium server is not running or not responsive.")
                break
            time.sleep(0.5)


    def stop_server(self) -> None:
        """
        Turn off appium server by kill node.exe
        """
        subprocess.Popen(
            'taskkill /f /im node.exe',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

    def is_appium_server_alive(self, host='127.0.0.1', port=4723) -> bool:
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
