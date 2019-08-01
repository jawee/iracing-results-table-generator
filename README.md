# iRacing Results Table Generator

Generates result images for top 10 for each class in ilms

## Usage
1. Place a file named ```'results.csv'``` in the ```app``` directory
2. run ```docker-compose up```
3. Files are placed in the ```'app/output/'``` directory, named LMP1.jpg, GTE.jpg, HPD.jpg

## Customization
Make changes in template.html for styling and static text.

***IMPORTANT***: do not remove the ```<table>``` element.

Place any images in the images folder, this is then copied over by the program to the output directory.

## Technology
* Python
* Docker
* imgkit
