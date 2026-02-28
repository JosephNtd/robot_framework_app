import sys
from PyQt5.QtWidgets import QApplication
from app.app import AutomationTestApp
from app.progress_screen import ProgressScreen
from service.appium_server import AppiumServer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    appium = AppiumServer()

    main = AutomationTestApp(None)
    window = ProgressScreen(main, appium)

    app.aboutToQuit.connect(appium.stop_server)

    window.show()

    sys.exit(app.exec_())
