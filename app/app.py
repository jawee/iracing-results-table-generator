import os
import csv
from shutil import copyfile
from distutils.dir_util import copy_tree
import imgkit
import constants as ct

def print_to_html_file(results_list, class_name, filepath, filepath_template, single_class=False):
    """ Print to html file

        Parameters:

            results_list -- the list containing the results of the class

            class_name -- the name of the car class

            file_path -- path where html file should be placed

            file_path_template -- path of the html template file

    """
    copyfile(filepath_template, filepath)
    fc = open(filepath, "r")
    contents = fc.readlines()

    indexes = [i for i, s in enumerate(contents) if '<table>' in s]

    if indexes:
        index = indexes[0]
    else:
        return # Did not find table, return

    count = 10
    if len(results_list) < 10:
        count = len(results_list)
    if single_class:
        # If it's a single class, do not write class name
        contents.insert(index, '<h3>Topp {count}</h3>'.format(count=count))
    else:
        contents.insert(index, '<h3>Topp {count} i {name}-klassen</h3>'.format(count=count, name=class_name))
    index += 1
    for i in range(10):
        if i < len(results_list):
            index += 1
            contents.insert(index, '<tr><td class="number">{pos}</td><td class="name">{name}</td></tr>\n'.format(pos=(i+1), name=results_list[i][ct.COL_NAME]))

    fc = open(filepath, "w")
    contents = "".join(contents)
    fc.write(contents)
    fc.close()

def copy_template_images_to_output(imagesFolderPath, outputPath):
    """ Copy the images folder recursively to another path

        Parameters:

            imagesFolderPath: path of the images folder
            outputPath: path of the output folder where the folder should be copied to

    """
    copy_tree(imagesFolderPath, os.path.join(outputPath, 'images/'))

def generate_results_for_class(class_dict, results_file_name, single_class=False):
    """ Generate the results html and image for the class

        Parameters:
            class_dict: dictionary containing the class input
            results_file_name: filename of the results.csv file
            single_class: if there are multiple classes to generate for or not
    """
    class_name = ct.classNames[class_dict['classID']]
    class_file_name_html = '{className}Table.html'.format(className=class_name)
    class_file_name_image = '{className}.jpg'.format(className=class_name)

    #Get current location of app.py, this is our root
    root_path = os.path.dirname(os.path.abspath(__file__))

    #Get the path of the results file
    results_filepath = os.path.join(root_path, results_file_name)
    #Get the path of the template html file
    template_filepath = os.path.join(root_path, 'template.html')

    #Get the output directory path
    output_path = os.path.join(root_path, 'output/')

    #Create path of html file
    class_file_html_path = os.path.join(output_path, class_file_name_html)

    #Create path of image file
    class_file_image_path = os.path.join(output_path, class_file_name_image)

    #Open results file
    with open(results_filepath) as csvfile:
        #Skip first three lines (for regular race, TODO league races)
        csvfile.readline()
        csvfile.readline()
        csvfile.readline()

        #Read as dictionary
        results = csv.DictReader(csvfile, delimiter=',', quotechar='"')

        #Create list to contain the entries
        results_list_for_class = []
        #Loop through results to find all the entires within the class
        for row in results:
            if row[ct.COL_CAR_CLASS_ID] == class_dict['classID']:
                results_list_for_class.append(row)

        print("Entries found: ", len(results_list_for_class))

        #Create the html file
        print_to_html_file(results_list_for_class, class_name, class_file_html_path, template_filepath, single_class)
        #Create the image file
        imgkit.from_file(class_file_html_path, class_file_image_path)

def generate_results(input_list, results_file_name):
    """ Generate the results

        Parameters:

        inputlist: the list containing the dictionaries for each class that results should be generated for
    """
    # Start with copying images folder to the output directory
    here = os.path.dirname(os.path.abspath(__file__))
    output = os.path.join(here, 'output/')
    copy_template_images_to_output(os.path.join(here, 'images/'), output)

    single_class = True
    if len(input_list) > 1:
        single_class = False

    for class_dict in input_list:
        generate_results_for_class(class_dict, results_file_name, single_class)

if __name__ == '__main__':
    # class_list = [
    #     {'classID': ct.CLASS_ID_LMP1},
    #     {'classID': ct.CLASS_ID_HPD},
    #     {'classID': ct.CLASS_ID_GTE}
    # ]
    # results_file_name = 'results.csv'

    class_list = [
        {'classID': ct.CLASS_ID_GT3CUP}
    ]
    results_file_name = 'results.csv'
    generate_results(class_list, results_file_name)