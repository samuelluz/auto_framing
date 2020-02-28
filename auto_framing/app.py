import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFrame, QLabel, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import auto_framing
import os

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):

        # button
        load_frame_button = QPushButton('Carregar moldura', self)
        load_frame_button.clicked.connect(self.load_frame_button_action)
        load_frame_button.move(10, 10)

        open_path_button = QPushButton('Carregar fotos', self)
        open_path_button.clicked.connect(self.open_path_button_action)
        open_path_button.move(10, 60)

        # # image
        image = QPixmap('logo/inloco.png')
        image = image.scaled(320, 240, Qt.KeepAspectRatio, Qt.FastTransformation)

        self.label = QLabel(self)
        self.label.setPixmap(image)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(load_frame_button)
        layout.addWidget(open_path_button)
        self.setLayout(layout)
        self.setWindowTitle('Moldura Automatica')
        self.show()
    

    def open_path_button_action(self):
        auto_framing.emoldurar(self.open_path_dialog())

    def load_frame_button_action(self):
        auto_framing.mold_path = self.open_file_name_dialog()
    
    def open_path_dialog(self):
        path = []
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getExistingDirectory(self,"QFileDialog.getOpenFileNames()")
        if path:
            print(path)
        return path

    def open_file_name_dialog(self):
        path = []
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path, fileType = QFileDialog.getOpenFileName(self, 'Choose Image', os.sep.join((os.path.expanduser('~'), 'Documents')),
                                                 'Image Files (*.png)')
        if path:
            print(path)
            # image
            image = QPixmap(path)
            image = image.scaled(320, 240, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label.setPixmap(image)
        return path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())