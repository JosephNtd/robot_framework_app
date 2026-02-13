import time
import subprocess

class AppiumServer():
    def __init__(self):
        self.appium_process = None

    def start_server(self):
        subprocess.Popen(
            'start "Appium broker" cmd.exe /c appium',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

    def stop_server(self):
        subprocess.Popen(
            'taskkill /f /im node.exe',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
