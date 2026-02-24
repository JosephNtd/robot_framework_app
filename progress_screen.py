import threading
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QApplication
from PyQt5.QtCore import Qt

class ProgressScreen(QWidget):
    """
    Progress Screen starter to run appium server then goes into main app
    """
    def __init__(self, main_window, appium):
        super().__init__()
        self.main_window = main_window
        self.appium = appium # Appium server class -> start/ stop/ check server
        self.create_progress_splashscreen()

    def create_progress_splashscreen(self):
        self.setWindowTitle("Loading....")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Đang khởi động ứng dụng...")
        self.label.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)

        self.run_server()

        self.appium.server_started.connect(self.open_main)
    
    def run_server(self):
        """
        Create a thread to run appium server
        """
        thread = threading.Thread(
            target=self.appium.start_server,
            daemon=True,
            name='Start appium'
        )
        thread.start()

    def open_main(self):
        self.progress_bar.setRange(0, 1)
        self.main_window.show()
        self.close()