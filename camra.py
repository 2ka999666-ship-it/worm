import sys
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore
from camera import Camera
app = QApplication(sys.argv)
def start():
    global camera
    camera = Camera()
    camera.show()
class Dummy:
    def start(self):
        start()
app.requestPermission(QtCore.QCameraPermission(), None, Dummy().start)
sys.exit(app.exec())

