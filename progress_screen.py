import threading
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QPushButton
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
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("Loading....")
        self.setFixedSize(900, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget{
                background-color: #2c3e50;
                border-radius: 5px
            }
            QLabel {
                color: white;
                font-size: 35px;
            }
            QProgressBar {
                height: 6px;
                border-radius: 3px;
                background: #34495e;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """)


        self.label = QLabel("Đang khởi động ứng dụng...")
        self.label.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        self.retry_button = QPushButton("Thử lại")
        self.retry_button.setVisible(False)
        self.retry_button.clicked.connect(self.retry_server)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.retry_button)

        self.run_server()

        self.appium.server_started.connect(self.open_main)
        self.appium.server_failed.connect(self.connect_server_failed)

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

    def connect_server_failed(self):
        self.progress_bar.setRange(0, 1)
        self.label.setText("Kết nối thất bại...\nVui lòng thử lại")
        self.retry_button.setVisible(True)

    def retry_server(self):
        self.retry_button.setEnabled(True)
        self.progress_bar.setRange(0, 0)
        self.label.setText("Đang khởi động ứng dụng...")
        self.run_server()
        self.retry_button.setVisible(False)