import os
import csv
from shutil import copyfile
from distutils.dir_util import copy_tree
import imgkit
import constants as ct

def print_to_file(resultsList, classname, filepath, filepathtemplate):
    print("Copying", filepathtemplate, " to ", filepath)
    copyfile(filepathtemplate, filepath)
    fc = open(filepath, "r")
    contents = fc.readlines()

    indexes = [i for i, s in enumerate(contents) if '<table>' in s]

    if len(indexes) > 0:
        index = indexes[0]
    else:
        return

    contents.insert(index, '<h3>Top 10 i {name}-klassen</h3>'.format(name=classname))
    index += 1
    for i in range(10):
        if i < len(resultsList):
            index += 1
            contents.insert(index, '<tr><td class="number">{pos}</td><td class="name">{name}</td></tr>\n'.format(pos=(i+1), name=resultsList[i][ct.COL_NAME]))

    fc = open(filepath, "w")
    contents = "".join(contents)
    fc.write(contents)
    fc.close()

def copy_template_images_to_output(imagesFolderPath, outputPath):
    copy_tree(imagesFolderPath, os.path.join(outputPath, 'images/'))


def generate_results():
    gtefilename = 'GTETable.html'
    hpdfilename = 'HPDTable.html'
    lmp1filename = 'LMP1Table.html'

    gteimagename = 'GTE.jpg'
    hpdimagename = 'HPD.jpg'
    lmp1imagename = 'LMP1.jpg'

    here = os.path.dirname(os.path.abspath(__file__))

    resultsfilepath = os.path.join(here, 'results.csv') # results file should be in "root"
    templatefilepath = os.path.join(here, 'template.html') # template file should be in "root"

    output = os.path.join(here, 'output/') # All output in the output folder

    print("Output:", output)

    gtefilepath = os.path.join(output, gtefilename)
    if os.path.isfile(gtefilepath):
        os.remove(gtefilepath)

    hpdfilepath = os.path.join(output, hpdfilename)
    if os.path.isfile(hpdfilepath):
        os.remove(hpdfilepath)

    lmp1filepath = os.path.join(output, lmp1filename)
    if os.path.isfile(lmp1filepath):
        os.remove(lmp1filepath)

    print("Lmp1filepath:", lmp1filepath)
    with open(resultsfilepath) as csvfile:
        #Skip first three lines (for regular race, TODO league races)
        csvfile.readline()
        csvfile.readline()
        csvfile.readline()

        results = csv.DictReader(csvfile, delimiter=',', quotechar='"')

        lmp1List = []
        hpdList = []
        gteList = []
        for row in results:
            if row[ct.COL_CAR_CLASS_ID] == ct.CLASS_ID_LMP1:
                lmp1List.append(row)
            elif row[ct.COL_CAR_CLASS_ID] == ct.CLASS_ID_HPD:
                hpdList.append(row)
            elif row[ct.COL_CAR_CLASS_ID] == ct.CLASS_ID_GTE:
                gteList.append(row)

        print("LMP1 list count: ", len(lmp1List))
        print("HPD list count: ", len(hpdList))
        print("GTE list count: ", len(gteList))

        copy_template_images_to_output(os.path.join(here, 'images/'), output)

        print_to_file(lmp1List, "LMP1", lmp1filepath, templatefilepath)

        print_to_file(hpdList, "HPD", hpdfilepath, templatefilepath)

        print_to_file(gteList, "GTE", gtefilepath, templatefilepath)

        imgkit.from_file(lmp1filepath, os.path.join(output, lmp1imagename))
        imgkit.from_file(hpdfilepath, os.path.join(output, hpdimagename))
        imgkit.from_file(gtefilepath, os.path.join(output, gteimagename))

if __name__ == '__main__':
    generate_results()