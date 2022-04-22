import sys
import folium
import io
from PyQt5.QtWidgets import QApplication, QAbstractItemView, QPushButton, QLabel, qApp, QWidget, QAction, QHeaderView, QTableWidget, QTableWidgetItem, QGridLayout, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QColor, QTransform, QFont
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView

class EXIFWindow(object):

    #setup for the window which will contains the EXIF tags
    def setupUI(self, MainWindow, images):

        MainWindow.setWindowTitle("EXIF Viewer")
        MainWindow.setWindowIcon(QIcon("Images/Icons/details.png"))

        self.window_width = MainWindow.width()
        self.window_height = MainWindow.height()
        self.update=True

        self.centralwidget = QWidget(MainWindow)
        self.image = images[0]

        #button to switch to next image
        switch_to_next_image = QPushButton(MainWindow)
        switch_to_next_image.setIcon(QIcon('Images/Icons/icons8-right-arrow-64.png'))
        switch_to_next_image.setIconSize(QSize(100, 100))
        switch_to_next_image.clicked.connect(lambda: self.switchImage(MainWindow, grid_layout))

        #button to switch to previous image
        switch_to_previous_image = QPushButton(MainWindow)
        switch_to_previous_image.setIcon(QIcon('Images/Icons/icons8-left-arrow-64.png'))
        switch_to_previous_image.setIconSize(QSize(100, 100))
        switch_to_previous_image.clicked.connect(lambda: self.switchImage(MainWindow, grid_layout, next=False))

        switch_to_previous_image.setStyleSheet('''QPushButton {border: 2px solid black; border-radius: 20px; background-color: #313131; margin: auto 30px;} QPushButton:hover {background-color: #BB86FC;}''')
        switch_to_next_image.setStyleSheet('''QPushButton {border: 2px solid black; border-radius: 20px; background-color: #313131; margin: auto 30px;} QPushButton:hover {background-color: #BB86FC;}''')

        #menuBar with actions: open new images, add new images, rotate 90° (clockwise and counterclockwise), close current image and close all images
        menubar = MainWindow.menuBar()

        #file menu actions
        openAct = QAction('Open new images', MainWindow)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open a new image')
        openAct.setIcon(QIcon("Images/Icons/add_single_image.png"))
        openAct.triggered.connect(lambda: self.open_close_images(MainWindow, grid_layout, action='openNewImages'))

        addImageAct = QAction('Add images', MainWindow)
        addImageAct.setShortcut('Ctrl+N')
        addImageAct.setStatusTip('Add a new image in the list')
        addImageAct.setIcon(QIcon("Images/Icons/add_multiple_images.png"))
        addImageAct.triggered.connect(lambda: self.open_close_images(MainWindow, grid_layout, action='addNewImages'))

        rotateClockwiseAct = QAction('Rotate 90° clockwise', MainWindow)
        rotateClockwiseAct.setShortcut('Ctrl+R')
        rotateClockwiseAct.setStatusTip('Rotate image by 90 degrees clockwise')
        rotateClockwiseAct.setIcon(QIcon("Images/Icons/rotate_clockwise.png"))
        rotateClockwiseAct.triggered.connect(lambda: self.rotateImage(MainWindow, grid_layout))

        rotateCounterClockwiseAct = QAction('Rotate 90° counterclockwise', MainWindow)
        rotateCounterClockwiseAct.setShortcut('Ctrl+T')
        rotateCounterClockwiseAct.setStatusTip('Rotate image by 90 degrees counterclockwise')
        rotateCounterClockwiseAct.setIcon(QIcon("Images/Icons/rotate_counterclockwise.png"))
        rotateCounterClockwiseAct.triggered.connect(lambda: self.rotateImage(MainWindow, grid_layout, clockwise=False))

        closeAct = QAction('Close current image', MainWindow)
        closeAct.setShortcut('Ctrl+Q')
        closeAct.setStatusTip('Close current image')
        closeAct.setIcon(QIcon("Images/Icons/close_image.png"))
        closeAct.triggered.connect(lambda: self.open_close_images(MainWindow, grid_layout, action='closeCurrentImage'))

        closeAllAct = QAction('Close all images', MainWindow)
        closeAllAct.setShortcut('Ctrl+Shift+Q')
        closeAllAct.setStatusTip('Close all images opened')
        closeAllAct.setIcon(QIcon("Images/Icons/close_all_images.png"))
        closeAllAct.triggered.connect(lambda: self.open_close_images(MainWindow, grid_layout, action='closeAllImages'))

        exitAct = QAction('Exit', MainWindow)
        exitAct.setShortcut('Ctrl+E')
        exitAct.setStatusTip('Exit application')
        exitAct.setIcon(QIcon("Images/Icons/exit.png"))
        exitAct.triggered.connect(qApp.quit)

        getExifAct = QAction('View Details', MainWindow)
        getExifAct.triggered.connect(lambda: self.viewDetails(MainWindow))

        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(openAct)
        fileMenu.addAction(addImageAct)
        fileMenu.addAction(rotateClockwiseAct)
        fileMenu.addAction(rotateCounterClockwiseAct)
        fileMenu.addAction(closeAct)
        fileMenu.addAction(closeAllAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)
        menubar.addAction(getExifAct)

        #set menu style
        self.setMenuBarStyle(menubar)

        #creates widgets for geolocalization
        self.webView = QWebEngineView(MainWindow)
        self.gps_label = QLabel(MainWindow)
        self.image_label = QLabel(MainWindow)

        self.table = QTableWidget(MainWindow)

        #creates button to switch to next/previous image
        self.nextPushButton = QPushButton(MainWindow)
        self.previousPushButton = QPushButton(MainWindow)

        #shows image preview and properly scales it
        self.label = QLabel(MainWindow)
        self.pixmap = QPixmap(self.image)
        if(self.pixmap.width()>=self.pixmap.height()):
            self.pixmap = self.pixmap.scaledToWidth(self.window_width*5/7)
        else:
            self.pixmap = self.pixmap.scaledToHeight(self.window_height*5/7)
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.image_rotation = 0

        #set grid layout (which contains: menubar on top, image preview on center and buttons on the sides of image
        grid_layout = QGridLayout(MainWindow)
        grid_layout.addWidget(menubar, 0, 0, 1, -1, alignment=Qt.AlignTop)
        grid_layout.addWidget(switch_to_previous_image, 1, 0, -1, 1, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.label, 1, 1, -1, 5, alignment=Qt.AlignCenter)
        grid_layout.addWidget(switch_to_next_image, 1, 6, -1, 1, alignment=Qt.AlignCenter)

        grid_layout.setAlignment(Qt.AlignTop)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setRowStretch(1,1)

        self.centralwidget.setLayout(grid_layout)
        MainWindow.setCentralWidget(self.centralwidget)

    #updates image dimensions according to the window size
    def updateImage(self, new_dimension):
        self.pixmap = QPixmap(self.image)
        if(self.pixmap.width()>=self.pixmap.height()):
            self.pixmap = self.pixmap.scaledToWidth(new_dimension, Qt.SmoothTransformation)
        else:
            self.pixmap = self.pixmap.scaledToHeight(new_dimension, Qt.SmoothTransformation)
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)

    #switch to the next/previous image in the list, using the model
    def switchImage(self, MainWindow, grid_layout, next=True, scale_to_max_size=False, updateTable=False):
        if(next):
            MainWindow.model.nextImage()
        else:
            MainWindow.model.previousImage()
        self.image = MainWindow.model.current_image
        self.pixmap = QPixmap(self.image)


        if (scale_to_max_size):
            #to have a maximum dimension (width or height) of the image of 512 pixels, except in the first page
            self.pixmap = self.pixmap.scaled(512,512,Qt.KeepAspectRatio)
        else:
            #in the first page, the image preview takes up as much space as possible
            if (self.pixmap.width() >= self.pixmap.height()):
                self.pixmap = self.pixmap.scaledToWidth(MainWindow.width() * 5 / 7)
            else:
                self.pixmap = self.pixmap.scaledToHeight(MainWindow.height() * 5 / 7)


        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.image_rotation = 0

        if (updateTable):
            self.generalInfo(MainWindow, grid_layout)
            grid_layout.addWidget(self.label, 1, 0, 1, 1, alignment=Qt.AlignCenter)

    #rotate image of 90° clockwise or counterclockwise
    def rotateImage(self, MainWindow, grid_layout, clockwise=True):
        self.pixmap = QPixmap(self.image)

        if(clockwise):
            self.image_rotation += 90
        else:
            self.image_rotation -= 90


        self.pixmap = self.pixmap.transformed(QTransform().rotate(self.image_rotation))
        if (self.pixmap.width() >= self.pixmap.height()):
            self.pixmap = self.pixmap.scaledToWidth(MainWindow.width() * 5 / 7)
        else:
            self.pixmap = self.pixmap.scaledToHeight(MainWindow.height() * 5 / 7)
        self.label.setPixmap(self.pixmap)

        self.label.setAlignment(Qt.AlignCenter)
        #grid_layout.addWidget(self.label, 1, 1, -1, 3, alignment=Qt.AlignCenter)

    #open or close images, using the model
    def open_close_images(self, MainWindow, grid_layout, action):
        if(action=='openNewImages'):
            dialog = QFileDialog()
            images = dialog.getOpenFileNames(MainWindow, "Open Images",
                                             "C:/Users/giuli/OneDrive/Desktop/Fotografia/Foto",
                                             "Images (*.png *.xpm *.jpg)")
            images = images[0]
            MainWindow.model.openNewImages(images)
            self.image = images[0]
        elif(action=='addNewImages'):
            dialog = QFileDialog()
            images = dialog.getOpenFileNames(MainWindow, "Open Images",
                                             "C:/Users/giuli/OneDrive/Desktop/Fotografia/Foto",
                                             "Images (*.png *.xpm *.jpg )")
            images = images[0]
            MainWindow.model.addNewImages(images)
            self.image = images[0]

        elif(action=='closeCurrentImage'):
            MainWindow.model.closeCurrentImage()
            self.image = MainWindow.model.current_image
        else: #closeAllImages
            MainWindow.model.closeAllImages()
            self.image = None

        self.pixmap = QPixmap(self.image)
        self.pixmap = self.pixmap.scaled(MainWindow.width()*5/7, MainWindow.height()*5/7, Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        #grid_layout.addWidget(self.label, 1, 1, -1, 3, alignment=Qt.AlignCenter)
        self.image_rotation = 0

    #set the page for when you click on "View details" to see the EXIF tags of the images
    def viewDetails(self, MainWindow):
        MainWindow.setWindowTitle("EXIF Viewer")
        self.centralwidget = QWidget(MainWindow)

        #new menubar for this page
        menubar = MainWindow.menuBar()

        grid_layout = QGridLayout(MainWindow)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(menubar, 0, 0, 1, -1, alignment=Qt.AlignTop)

        #menu actions: general info of the image, basic exif tags, other exif tags and gps info
        generalInfoAct = QAction('General Info', MainWindow)
        generalInfoAct.setStatusTip('Shows the general image info')
        generalInfoAct.triggered.connect(lambda: self.generalInfo(MainWindow, grid_layout))

        basicEXIFAct = QAction('Basic EXIF Tags', MainWindow)
        basicEXIFAct.triggered.connect(lambda: self.basicEXIFTags(MainWindow, grid_layout))

        otherEXIFAct = QAction('Other EXIF Tags', MainWindow)
        otherEXIFAct.triggered.connect(lambda: self.otherEXIFTags(MainWindow, grid_layout))

        gpsInfoAct = QAction('GPS Info', MainWindow)
        gpsInfoAct.triggered.connect(lambda: self.gpsInfo(MainWindow, grid_layout))

        menubar.addAction(generalInfoAct)
        menubar.addAction(basicEXIFAct)
        menubar.addAction(otherEXIFAct)
        menubar.addAction(gpsInfoAct)

        #set menubar style
        self.setMenuBarStyle(menubar)


        #shows a preview of the image (maximum dimensions 512 pixels)
        self.pixmap = QPixmap(self.image)
        self.pixmap = self.pixmap.scaled(512,512,Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('''QLabel {margin: 10px 30px;}''')

        grid_layout.addWidget(self.label, 1, 0, -1, 1)

        self.update=False

        #set buttons to switch to next/previous image
        self.nextPushButton.setText("NEXT")
        self.previousPushButton.setText("PREVIOUS")
        self.nextPushButton.clicked.connect(
            lambda: self.switchImage(MainWindow, grid_layout, scale_to_max_size=True, updateTable=True))
        self.previousPushButton.clicked.connect(
            lambda: self.switchImage(MainWindow, grid_layout, next=False, scale_to_max_size=True, updateTable=True))
        self.setButtonStyle(self.nextPushButton)
        self.setButtonStyle(self.previousPushButton)

        layout_butt = QHBoxLayout(MainWindow)
        layout_butt.addWidget(self.previousPushButton, 1)
        layout_butt.addWidget(self.nextPushButton, 1)

        grid_layout.addLayout(layout_butt, 2, 0, -1, 1, alignment=Qt.AlignTop)

        #get general image info
        image_general_info = MainWindow.model.getImageInfo(self.image)

        #generate the table containing the general info of the image
        self.generateTable(MainWindow, grid_layout, image_general_info, general_info=True)

        grid_layout.addWidget(self.table, 1, 1, 1, -1)

        self.centralwidget.setLayout(grid_layout)
        MainWindow.setCentralWidget(self.centralwidget)


    #generate a table with image info or EXIF tags and set the style
    def generateTable(self, MainWindow, grid_layout, key_value_pairs, general_info=False):

        self.table.setRowCount(len(key_value_pairs))
        self.table.setColumnCount(2)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)

        self.table.setStyleSheet('''QTableWidget {background-color: #313131; margin: 10px 30px;}''')

        if (general_info):
            header_description = QTableWidgetItem('Description')
        else:
            header_description = QTableWidgetItem('TAG Name')

        font = QFont()
        font.setBold(True)
        header_description.setBackground(QColor(187, 134, 252))
        header_description.setFont(font)
        self.table.setHorizontalHeaderItem(0, header_description)

        header_value = QTableWidgetItem('Value')
        header_value.setBackground(QColor(187, 134, 252))
        header_value.setFont(font)
        self.table.setHorizontalHeaderItem(1, header_value)

        for row in range(len(key_value_pairs)):
            vertical_header = QTableWidgetItem(str(row + 1))
            vertical_header.setFont(font)
            vertical_header.setBackground(QColor(187, 134, 252))
            self.table.setVerticalHeaderItem(row, vertical_header)
            key = QTableWidgetItem(str(list(key_value_pairs.keys())[row]))
            value = QTableWidgetItem(str(list(key_value_pairs.values())[row]))
            self.table.setItem(row, 0, key)
            self.table.setItem(row, 1, value)

            key.setBackground(QColor(49, 49, 49))
            key.setForeground(QColor(255, 255, 255))
            value.setBackground(QColor(49, 49, 49))
            value.setForeground(QColor(255, 255, 255))

        self.table.verticalHeader().setStyleSheet("""
            QHeaderView::section {padding: 0 8px; border: 1px solid black; background-color: rgb(187,134,252);}
            """)
        self.table.horizontalHeader().setStyleSheet("""
                    QHeaderView::section {padding: 8px 0; border: 1px solid black; background-color: rgb(187,134,252);}
                    """)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        v_header = self.table.verticalHeader()
        for j in range(len(key_value_pairs)):
            v_header.setSectionResizeMode(j, QHeaderView.Fixed)


        grid_layout.addWidget(self.table, 1, 1, 1, -1)
        self.centralwidget.setLayout(grid_layout)
        MainWindow.setCentralWidget(self.centralwidget)


    #defines the layout of general info action (image preview, buttons to switch and table with general info)
    def generalInfo(self, MainWindow, grid_layout):
        self.webView.hide()

        self.gps_label.hide()
        self.image_label.hide()

        self.label.show()
        self.previousPushButton.show()
        self.nextPushButton.show()

        # get general image info
        image_general_info = MainWindow.model.getImageInfo(self.image)
        self.generateTable(MainWindow, grid_layout, image_general_info, general_info=True)
        self.table.show()


    #defines the layout of basic tags action (central table)
    def basicEXIFTags(self, MainWindow, grid_layout):
        self.label.hide()
        self.webView.hide()
        self.previousPushButton.hide()
        self.nextPushButton.hide()
        self.gps_label.hide()
        self.image_label.hide()


        #get basic EXIF Tags
        basic_tag_dict = MainWindow.model.getEXIFTags(self.image)[0]

        self.generateTable(MainWindow, grid_layout, basic_tag_dict)
        self.table.show()




    #defines the layout of other exif tags action (central table)
    def otherEXIFTags(self, MainWindow, grid_layout):
        self.label.hide()
        self.webView.hide()
        self.previousPushButton.hide()
        self.nextPushButton.hide()
        self.gps_label.hide()
        self.image_label.hide()


        # get the other EXIF tags
        tag_dict = MainWindow.model.getEXIFTags(self.image)[1]

        self.generateTable(MainWindow, grid_layout, tag_dict)
        self.table.show()



    #defines layout for gps info action (if there are not gps info it's a lable with an icon, otherwise a map from google maps centred on gps location)
    def gpsInfo(self, MainWindow, grid_layout):
        self.label.hide()
        self.webView.hide()
        self.previousPushButton.hide()
        self.nextPushButton.hide()
        self.gps_label.hide()
        self.image_label.hide()
        self.table.hide()


        #get gps tags
        gps_dict = MainWindow.model.getEXIFTags(self.image)[2]
        MainWindow.model.gpsDict = gps_dict

        keys = gps_dict.keys()

        #if there is a gps location
        if (gps_dict != {} and 'GPSLatitude' in keys and 'GPSLongitude' in keys):

            self.gps_label.show()
            self.image_label.show()
            self.webView.show()
            #gets the coordinate in degrees, using the model
            coordinate = MainWindow.model.gpsCoordsConverter()

            map = folium.Map(
                zoom_start=20,
                location=coordinate
            )
            folium.Marker([coordinate[0], coordinate[1]], popup=coordinate).add_to(map)
            #save map data to data object
            data = io.BytesIO()
            map.save(data, close_file=False)

            self.webView.setHtml(data.getvalue().decode())

            grid_layout.addWidget(self.webView, 1, 0, -1, -1)
            grid_layout.setRowStretch(1,1)

        else:
            #shows an icon and a text if there are not gps info in the image
            self.gps_label.show()
            self.image_label.show()
            self.webView.hide()
            self.gps_label.setText("Sorry, there are not GPS informations avaible :(")
            self.gps_label.setFont(QFont('Segoe', 14))
            self.gps_label.setStyleSheet("QLabel {color: white;}")

            pixmap = QPixmap("Images/Icons/noGPS.png")
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)

            grid_layout.addWidget(self.image_label, 1, 0, -1, -1)
            grid_layout.addWidget(self.gps_label, 2, 0, -1, -1, alignment=Qt.AlignCenter)

        self.centralwidget.setLayout(grid_layout)
        MainWindow.setCentralWidget(self.centralwidget)


    #set menubar style
    def setMenuBarStyle(self, menubar):
        menubar.setStyleSheet('''QMenuBar 
                                        {
                                        background-color: #313131;                                         
                                        margin:0;
                                        
                                        }
                                        QMenuBar::item {
                                        padding: 10px 10px;
                                        background: transparent;
                                        border-radius: 6px 6px 0 0;
                                        color: #ffffff;
                                        }
                                        QMenuBar::item:selected { 
                                        background: #BB86FC;
                                        color: #000000;
                                        }
                                        
                                        QMenuBar::item:pressed {
                                            background: #888888;
                                        }
                                        QMenu {
                                        background-color: #313131;
                                        }
                                        QMenu::item {
                                        color: #ffffff;
                                         padding: 0 8px;}
                                         
                                        QMenu::item:selected { 
                                        background: #BB86FC;
                                        color: #000000;
                                        }

                                        ''')

    #set button style
    def setButtonStyle(self, button):
        button.setStyleSheet('''QPushButton {
                                background-color: #313131;
                                color: #ffffff;
                                margin: 10px 30px;
                                border-radius: 20px;
                                padding: 20px 0;
                                }
                                QPushButton::hover {
                                background-color: #BB86FC;
                                color: #000000;
                                }
        
        ''')





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EXIFWindow()
    app.exec_()
