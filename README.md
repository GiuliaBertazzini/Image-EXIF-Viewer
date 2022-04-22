# Image-EXIF-Viewer
A simple implementation of an Image and EXIF Metadata Viewer in PyQt5.

## System Requirements

<b>Package</b> | <b>Version</b>
--- | ---
Python | 3.8
PyQt5 | 5.15.6
Pillow | 8.4.0 
folium | 0.12.1

## Functionalities
This GUI implements the following features:
- **Visualization of images**: it allows to visualize multiple images (one at a time); once you've selected some images, you can visualize them and if you made a mistake in selecting them, you can open a new list of images, add some images to the already opened ones, close the current image which you're visualizing or close all the images. The GUI also implements controls for switching to next/previous image in the list.  
- **Image rotation**: when you're visualizing your image, you can rotate it of 90 degrees (clockwise or counterclockwise).
- **Rescaling**: if you change the dimension of the window, the image will proprerly scale (and also the tables containing the EXIF tags). 
- **Visualization of image EXIF data**: it allows to proprerly see image EXIF, organized in a table (where there first column contains the tag name and the second one the value for the corresponding tag).
- **Geolocalization**: if an image includes GPS Geolocation Tags in its EXIF tag set, you can visualize a map on the GUI, with a marker centered at the GPS location of the image.


## Usage
Once you've downloaded the project and installed all the packages required, run the following command in your terminal: <br>
`python MainWindow.py`

That's what you see:
<p align="center"><img src=images/MainWindow.png width="60%"></p>

When you click on the button, you will be able to choose your list of images (only images file will be shown). 

<p align="center"><img src=images/ImageViewer.png width="60%"></p>

The GUI will show the first image in the center of the window. You can switch to the next/previous image using the controls on the image sides. If you click on "File", you will be able to choose an action, clicking on it (or you can use the corresponding shortcut): 
- **Open new images**: you can open a completely new list of image, different from the first one you had chosen. The corresponding shortcut is CTRL+O.
- **Add images**: you can add images to the current list. The corresponding shortcut is CTRL+N.
- **Rotate 90° clockwise**: you will be able to rotate your image of 90 degrees clockwise. The corresponding shortcut is CTRL+R.
- **Rotate 90° counterclockwise**: you will be able to rotate your image of 90 degress counterclockwise. The corresponding shortcut is CTRL+T.
- **Close current image**: you can close the current image which you're visualizing. The corresponding shortcut is CTRL+Q.
- **Close all images**: you can close all the images of the list. The corresponding shortcut is CTRL+Shift+Q.
- **Exit**: you can close the GUI. The corresponding shortcut is CTRL+E.

Then, if you are interested on visualizing image EXIF data, you can click on "View Details"; you will be automatically redirected to the following page:

<p align="center"><img src=images/generalInfo.png width="60%"></p>

As you can see, you will have a little preview of the current image on the left, and also two buttons, with lables PREVIOUS and NEXT, if you want to visualize EXIF tags of another image in the list. On the right, you will find a table containg the general information of the image (as the filename, the creation and mofication date, the format, the size and the mode). 









