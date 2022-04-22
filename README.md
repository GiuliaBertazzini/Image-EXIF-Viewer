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







