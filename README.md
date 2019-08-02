# iRacing Results Table Generator

![Kiku](example_image_doc.jpg)

Generates result images for top 10 for each class in the results csv file, classes is based on an input list, can be seen in the main-method in ```app/app.py```

The input variables to the ```generate_results```-method should be in the form of (example below is for iRacing Le Mans Series):
```python
class_list = [
         {'classID': ct.CLASS_ID_LMP1},
         {'classID': ct.CLASS_ID_HPD},
         {'classID': ct.CLASS_ID_GTE}
    ]
results_file_name = 'results.csv'
```
Where the class id for each class is pulled from the ```app/constants.py``` file.
The results file can be named something else than ```results.csv```, but then the ```results_file_name``` input variable needs to be changed. 

## Basic Usage
1. Place a file named ```results.csv``` in the ```app``` directory
2. Add car classes in the main-method in ```app/app.py``` to the class_list.
3. Run ```docker-compose up```
4. Files are placed in the ```app/output/``` directory, named after the car class, as defined in ```app/constants.py```

## Customization
Make changes in template.html for styling and static text.

***IMPORTANT***: do not remove the ```<table>``` element.

Place any images in the images folder, this is then copied over by the program to the output directory.

## Technology
* Python
    * imgkit
* Docker


### TODO-list
* Handle single car league races better
* Handle team events
* More car classes to constants
