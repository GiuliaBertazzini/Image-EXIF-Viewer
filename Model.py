from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import time
import os

#list of most common tags according to this table: https://www.vcode.no/web/resource.nsf/ii2lnug/642.html
baseline_exif_tag = [1, 2, 254, 255, 256, 257, 258, 259, 262, 263, 264, 265, 266, 270, 271, 272, 273, 274, 277, 278, 279, 280, 281, 282, 283, 284, 288, 289, 290, 291, 296, 305, 306, 315, 316, 320, 338, 33432]

#model to manage data, indipendent of the UI
class Model:
    def __init__(self):
        #list of images
        self.list_of_images = list()
        #current image
        self.current_image = None
        #general image info
        self.image_info = dict()
        #most common tags
        self.baselineTagDict = dict()
        #other exif tags (= all tags without the most common ones)
        self.tagDict = dict()
        #gps info
        self.gpsDict = dict()


    #open a new list images
    def openNewImages(self, images):
        self.list_of_images = images
        self.current_image = images[0]

    #add new images to the other ones previously opened
    def addNewImages(self, images):
        self.list_of_images += images
        self.current_image = images[0]

    #close only the current image
    def closeCurrentImage(self):
        index = self.list_of_images.index(self.current_image)
        del self.list_of_images[index]
        if(len(self.list_of_images)>0):
            self.current_image = self.list_of_images[index-1]
        else:
            self.current_image = None

    #close all the images
    def closeAllImages(self):
        self.list_of_images.clear()
        self.current_image = None

    #switch to the next image in the list
    def nextImage(self):
        index = self.list_of_images.index(self.current_image)
        index += 1
        if (index == len(self.list_of_images)):
            index = 0
        self.current_image = self.list_of_images[index]

    #switch to the previous image in the list
    def previousImage(self):
        index = self.list_of_images.index(self.current_image)
        index -= 1
        if (index == -1):
            index = len(self.list_of_images) - 1
        self.current_image = self.list_of_images[index]

    #get the general info of the image
    def getImageInfo(self, image):
        image = Image.open(image)
        if image:
            self.image_info['Filename'] = image.filename.rsplit("/", 1)[1]
            self.image_info['Creation Date'] = time.ctime(os.path.getctime(image.filename))
            self.image_info['Modification Date'] = time.ctime(os.path.getmtime(image.filename))
            self.image_info['Format'] = image.format
            self.image_info['Size'] = image.size
            self.image_info['Mode'] = image.mode
        return self.image_info

    #get the EXIF Tags of the image, dividing them in basic tag, other tag and gps tag
    def getEXIFTags(self, image):
        self.tagDict.clear()
        self.baselineTagDict.clear()
        self.gpsDict.clear()

        image_info = Image.open(image)._getexif() #gets TAG as codes
        for tag, value in image_info.items():
            decoded = TAGS.get(tag,tag)
            if tag in baseline_exif_tag:
                self.baselineTagDict[decoded] = value
            else:
                self.tagDict[decoded] = value

        if('GPSInfo' in self.tagDict.keys()): #check if the selected image contains GPS tag
            for key in self.tagDict['GPSInfo'].keys():
                decode = GPSTAGS.get(key, key)
                self.gpsDict[decode] = self.tagDict['GPSInfo'][key]


        return self.baselineTagDict, self.tagDict, self.gpsDict

    #convert coordinates in degrees
    def gpsCoordsConverter(self):
        gps_latitude = self.gpsDict['GPSLatitude']
        gps_longitude = self.gpsDict['GPSLongitude']
        latitude = gps_latitude[0]+(gps_latitude[1]/float(60))+(gps_latitude[2]/float(3600))
        longitude = gps_longitude[0]+(gps_longitude[1]/float(60))+(gps_longitude[2]/float(3600))
        return latitude, longitude




