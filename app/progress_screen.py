import threading
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QPushButton
from PyQt5.QtCore import Qt

class ProgressScreen(QWidget):
    """
    Progress Screen starter to run appium server then goes into main app
    """
    SERVER_START            = "Đang khởi động ứng dụng..."
    SERVER_CONNECT_FAILED   = "Kết nối thất bại...\nVui lòng thử lại"
    RETRY_BUTTON_TEXT       = "Thử lại"

    def __init__(self, main_window, appium):
        super().__init__()
        self.main_window = main_window
        self.appium = appium # Appium server class -> start/ stop/ check server
        self.create_progress_splashscreen()

    def create_progress_splashscreen(self):
        """ Initialize splash screen when started app"""
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("Loading....")
        self.setFixedSize(900, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget{
                background-color: #191970;
                border-radius: 5px
            }
            QLabel {
                color: white;
                font-size: 35px;
            }
            QProgressBar {
                height: 6px;
                border-radius: 3px;
                background: #ECEFF1;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
            QPushButton{
                color: black;
                font-size: 20px;
                background-color: #FFF2E1
            }
        """)


        self.label = QLabel(self.SERVER_START)
        self.label.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        # self.layout.addStretch()

        self.retry_button = QPushButton(self.RETRY_BUTTON_TEXT)
        self.retry_button.setFixedSize(100, 40)
        self.retry_button.setVisible(False)
        self.retry_button.clicked.connect(self.retry_server)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.retry_button, alignment=Qt.AlignCenter)

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
        """ Open main window when connect appium sucessfully"""
        self.progress_bar.setRange(0, 1)
        self.main_window.show()
        self.close()

    def connect_server_failed(self):
        """ View a re-connect button for user to connect to server again when connect failed"""
        self.progress_bar.setRange(0, 1)
        self.label.setText(self.SERVER_CONNECT_FAILED)
        self.retry_button.setVisible(True)
        self.progress_bar.setVisible(False)

    def retry_server(self):
        """ Interface interaction when connect to appium failed"""
        self.retry_button.setEnabled(True)
        self.progress_bar.setRange(0, 0)
        self.label.setText(self.SERVER_START)
        self.progress_bar.setVisible(True)
        self.run_server()
        self.retry_button.setVisible(False)
