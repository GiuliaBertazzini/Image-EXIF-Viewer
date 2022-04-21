import sys
import SelectImageWindow as sw
import EXIFWindow as ew
import Model as model

from PyQt5.QtWidgets import QApplication, QMainWindow, QStyleFactory
from PyQt5.Qt import QFileDialog
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.selectImageWindow = sw.SelectImageWindow()
        self.exifWindow = ew.EXIFWindow()
        self.model = model.Model()

        self.start_select_image_window()
        #set the style of the Main Window
        self.setStyleSheet("background-color: #181818;")
        self.setWindowTitle("EXIF Viewer")
        self.setMinimumSize(1100, 800)
        self.setWindowIcon(QIcon("Images/Icons/details.png"))


    #start and setup the first window (with a button to choose one or more images)
    def start_select_image_window(self):
        self.selectImageWindow.setupUI(self)
        self.selectImageWindow.selectImgButton.clicked.connect(self.start_exif_window)
        self.show()

    #open a default folder showing only image files and, once selected one or more images, start and show the second window
    def start_exif_window(self):
        dialog = QFileDialog()
        images = dialog.getOpenFileNames(self, "Open Images",
                                            "C:/Users/giuli/OneDrive/Desktop/Fotografia/Foto",
                                            "Images (*.png *.xpm *.jpg)")
        images = images[0] #images is a tuple (paths, filetypes), it takes only the paths
        if(images!=[]):
            self.model.list_of_images = images
            self.model.current_image = images[0]
            self.exifWindow.setupUI(self, self.model.list_of_images)

    #properly resize the central image based on window dimensions
    def resizeEvent(self, event):
        if(hasattr(self.exifWindow, 'pixmap')):
            if(self.exifWindow.pixmap.width()>=self.exifWindow.pixmap.height()):
                if(self.exifWindow.window_width!=self.width()):
                    if(self.exifWindow.update):
                        self.exifWindow.window_width = self.width()
                        new_width = int(self.width()*5/7)
                        self.exifWindow.updateImage(new_width)
            else:
                if (self.exifWindow.window_height != self.height()):
                    if (self.exifWindow.update):
                        self.exifWindow.window_height = self.height()
                        new_height = int(self.height() * 5 / 7)
                        self.exifWindow.updateImage(new_height)

        QMainWindow.resizeEvent(self, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    w = MainWindow()
    sys.exit(app.exec_())