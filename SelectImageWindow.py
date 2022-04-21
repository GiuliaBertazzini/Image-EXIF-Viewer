import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt

class SelectImageWindow(object):

    def setupUI(self, MainWindow):

        self.centralwidget = QWidget(MainWindow)

        #create a button and set its style
        self.selectImgButton = QPushButton()
        self.selectImgButton.setText('Click here to open an image')
        self.selectImgButton.setIcon(QIcon('Images/Icons/add-image.png'))
        self.selectImgButton.setIconSize(QSize(130, 130))
        self.selectImgButton.setFont(QFont('Segoe', 20))
        self.selectImgButton.setStyleSheet('''QPushButton
                             {
                             border: 2px solid black;
                             color: #ffffff;
                             background-color: #313131;
                             padding: 30px;
                             border-radius: 20px;
                                           
                             }
                                           QPushButton:hover {background-color: #BB86FC;}

                                           ''')


        #set the layout of the window
        grid_layout = QGridLayout(MainWindow)
        grid_layout.addWidget(self.selectImgButton, 0, 0, -1, -1)
        grid_layout.setAlignment(Qt.AlignCenter)

        self.centralwidget.setLayout(grid_layout)
        MainWindow.setCentralWidget(self.centralwidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SelectImageWindow()
    app.exec_()
