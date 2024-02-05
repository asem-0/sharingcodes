import sys
from datetime import datetime

from PySide2.QtCore import QThread, Signal
from PySide2.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,QTextEdit,QLabel,
                               QHBoxLayout,QPushButton,QWidget)


class MainWindow(QMainWindow):
    splash_text_signal = Signal(str)
    """Main window class, the main window of the application."""
    def __init__(self):
        """Initializes the main window object."""
        super().__init__()
        # Set the window title and size
        self.setWindowTitle("Thread Test")
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        # Create the main widget and set the layout

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Thread test"))

        panel_layout = QHBoxLayout()
        self.toggle_button = QPushButton("Start")
        self.toggle_button.clicked.connect(self.toggle_thread)

        panel_layout.addWidget(self.toggle_button)
        main_layout.addLayout(panel_layout)

        self.text_widget = QTextEdit()
        self.text_widget.setReadOnly(True)

        main_layout.addWidget(self.text_widget)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.show()

        # Create the thread worker object and the thread
        self.worker_object = Worker()
        self.worker_object.text_signal.connect(self.update_text)

        self.thread_operator = QThread()
        self.worker_object.moveToThread(self.thread_operator)
        
        # We link the starting of the thread to the run function
        ### WARNING: This cannot be done manually, if you do it manually, the threads will lock up
        ### you can try this by commenting the following line, then uncommenting the line in toggle_thread
        self.thread_operator.started.connect(self.worker_object.run)


    def toggle_thread(self):
        # Check if the thread is running
        if self.thread_operator.isRunning():
            # If it is running, stop it
            self.worker_object.stop()
            self.thread_operator.quit()
            self.toggle_button.setText("Start")
        else:
            self.thread_operator.start()
            ### Uncomment this line to see the threads lock up
            #self.thread_operator.run()
            self.toggle_button.setText("Stop")
    
    def update_text(self, text):
        self.text_widget.append(text)

class Worker(QThread):
    text_signal = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True

    def run(self):
        self.running = True
        while self.running:
            self.text_signal.emit(f"Time is: {datetime.now()}")
            self.sleep(1)

    def stop(self):
        self.running = False


app = QApplication([])
window = MainWindow()
sys.exit(app.exec_())