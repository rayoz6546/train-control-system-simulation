import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt
import os


class ImagePopup(QMainWindow):
    def __init__(self, popup_time=10):
        super().__init__()

        # Create a QLabel to display the image
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 300, 300)

        # Load the list of image files
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.image_files = [
            dir_path + "\coca_cola.jpg",
            dir_path + "\irioncitybeer.jpg",
            dir_path + "\marathon.jpg",
            dir_path + "\penmac.jpg",
            dir_path + "\pens.jpg",
            dir_path + "\pepsi.jpg",
            dir_path + "\pgh.jpg",
            dir_path + "\pirates.jpg",
            dir_path + "\steelers.jpg",
            dir_path + "\yinzer.jpg",
            dir_path + "\meme.jpg",
            dir_path + "\metalpipe.jpg"]

            # Set the window properties
        self.setWindowTitle("Advertisements")
        self.resize(300, 300)
        self.setGeometry(200, 100, 300, 300)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Set the QTimer to schedule the pop-up window
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_random_image)
        self.popup_time = popup_time * 1000  # Convert to milliseconds
        self.timer.start(self.popup_time)

    def show_random_image(self):
        # Choose a random image file from the list
        image_file = random.choice(self.image_files)

        # Load the image file using QPixmap
        pixmap = QPixmap(image_file)

        # Set the pixmap to the QLabel
        self.label.setPixmap(pixmap)

        # Show the window
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    popup = ImagePopup(popup_time=5)
    app.exec_()
