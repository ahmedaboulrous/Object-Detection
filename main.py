import sys

from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from yolo import yolo_images
from yolo_video import yolo_videos


class MainWindow:
    def __init__(self):
        designer_file = QFile("window.ui")
        designer_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(designer_file)
        designer_file.close()
        self.setup_connections()
        self.window.setWindowTitle("Object Detection and Recognition")

    def setup_connections(self):
        self.window.pushButton_start.clicked.connect(self.start_recognition)
        self.window.pushButton_start.pressed.connect(self.processing_input)
        self.window.pushButton_input.clicked.connect(self.select_input_file)
        self.window.pushButton_output.clicked.connect(self.select_output_directory)
        self.window.pushButton_detector.clicked.connect(self.select_detector_directory)

    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileUrl(self.window)
        file_path = file_path.toString().replace('file:///', '')
        if file_path == '':
            self.window.lineEdit_input.setStyleSheet("background-color: rgb(255, 196, 176);")
            self.window.lineEdit_input.setText("")
        else:
            self.window.lineEdit_input.setStyleSheet("")
            self.window.lineEdit_input.setText(file_path)

    def select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectoryUrl(self.window, options=QFileDialog.ShowDirsOnly)
        dir_path = dir_path.toString().replace('file:///', '')
        if dir_path == '' and self.window.lineEdit_output.text() == '':
            self.window.lineEdit_output.setStyleSheet("background-color: rgb(255, 196, 176);")
            self.window.lineEdit_output.setText("")
        else:
            self.window.lineEdit_output.setStyleSheet("")
            self.window.lineEdit_output.setText(dir_path)

    def select_detector_directory(self):
        dir_path = QFileDialog.getExistingDirectoryUrl(self.window)
        dir_path = dir_path.toString().replace('file:///', '')
        if dir_path == '' and self.window.lineEdit_detector.text() == '':
            self.window.lineEdit_detector.setStyleSheet("background-color: rgb(255, 196, 176);")
            self.window.lineEdit_detector.setText("")
        else:
            self.window.lineEdit_detector.setStyleSheet("")
            self.window.lineEdit_detector.setText(dir_path)

    def show(self):
        self.window.show()

    def processing_input(self):
        self.window.lineEdit_process.setStyleSheet("background-color: rgb(255, 149, 56);")
        self.window.lineEdit_process.setText("[ LOADING ]  Detecting Objects")

    def start_recognition(self):
        file_type = self.window.comboBox_input_type.currentIndex()
        detector = self.window.comboBox_detector.currentIndex()
        confidence = self.window.doubleSpinBox_confidence.value()
        threshold = self.window.doubleSpinBox_threshold.value()
        detector_path = self.window.lineEdit_detector.text()
        input_path = self.window.lineEdit_input.text()
        output_path = self.window.lineEdit_output.text()

        if detector_path == '' or input_path == '' or output_path == '':
            self.window.lineEdit_process.setStyleSheet("background-color: rgb(170, 170, 255);")
            self.window.lineEdit_process.setText("[ INFO ]  Fill in the Red boxes first")
            if detector_path == '':
                self.window.lineEdit_detector.setStyleSheet("background-color: rgb(255, 196, 176);")
            if input_path == '':
                self.window.lineEdit_input.setStyleSheet("background-color: rgb(255, 196, 176);")
            if output_path == '':
                self.window.lineEdit_output.setStyleSheet("background-color: rgb(255, 196, 176);")
        else:
            if file_type == 0:  # image
                self.start_image_recognition(detector, confidence, threshold, detector_path, input_path, output_path)
            elif file_type == 1:  # video
                self.start_video_recognition(detector, confidence, threshold, detector_path, input_path, output_path)

    def start_image_recognition(self, detector, confidence, threshold, detector_path, input_path, output_path):
        time = yolo_images(confidence, threshold, detector_path, input_path, output_path)
        self.window.lineEdit_process.setText(time)
        self.window.lineEdit_process.setStyleSheet("background-color: rgb(170, 255, 127);")

    def start_video_recognition(self, detector, confidence, threshold, detector_path, input_path, output_path):
        time = yolo_videos(confidence, threshold, detector_path, input_path, output_path)
        self.window.lineEdit_process.setText(time)
        self.window.lineEdit_process.setStyleSheet("background-color: rgb(170, 255, 127);")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
