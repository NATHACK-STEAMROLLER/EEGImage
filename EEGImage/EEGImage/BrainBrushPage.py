from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt6.QtGui import QMovie
from PyQt6.uic import loadUi
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        loadUi('BrainBrushPage.ui', self)

        # Assuming you have a QLabel in your UI for displaying the GIF
        self.label = QLabel(self.centralWidget())
        self.label.setGeometry(0, 0, 800, 600)  # Set the dimensions as per your requirements


        # Start the movie
        #self.movie.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
