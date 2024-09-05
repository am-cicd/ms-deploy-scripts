import sys
import os
import re
from ruamel.yaml import YAML
from datetime import datetime

# Performs the parsing of a file containing placeholders and replaces values
# with those defined in sourceFile
# input - sourceFile: the YAML file containing the actual values for properties
# input - placeholderFile: the text file (format can be .yaml or .properties)
# input - destinationFile: the location the resulting file should be placed
# returns - a set (list) of any properties that could not be found in the sourceFile
def replaceValues(sourceFileLocation,placeholderFileLocation,destinationFileLocation):

    print(str(datetime.now()) + " Replacing placeholders in " + placeholderFileLocation + " with values from " + sourceFileLocation)

    yaml = YAML()
    placeholdersNotFound = set([])

    #Check the files we need exist at the paths we have been given
    exists = os.path.isfile(sourceFileLocation)
    if not exists:
        raise FileNotFoundError('Source File containing values does not exist - ' + sourceFileLocation)

    exists = os.path.isfile(placeholderFileLocation)
    if not exists:
        raise FileNotFoundError('Placeholder file containing placeholders to be replaced does not exist - ' + placeholderFileLocation)

    #Open the files, source file as yaml, placeholder file as simple text file
    sourceFile = yaml.load(open(sourceFileLocation))
    placeholderFile = open(placeholderFileLocation,"r").read()

    #Pattern to find all occurences of <<property.name>>
    pattern = re.compile(r'\<\<(?P<property>.*)\>\>')

    #Perform the regex replace
    result = re.sub(pattern, lambda m: (replacePlaceholder(m,sourceFile,placeholdersNotFound)), placeholderFile)

    #Write the processed result to the destinationFile
    destinationFile = open(destinationFileLocation, "w")
    destinationFile.write(result)

    print(str(datetime.now()) + " Wrote new file " + destinationFileLocation + " containing actual property values")

    return placeholdersNotFound


#Function to get the value to replace an occurence of <<property.name>>
def replacePlaceholder(matchobj,sourceFile,placeholdersNotFound):
    property = matchobj.group('property')
    value = getValue(property,sourceFile,placeholdersNotFound)
    return str(value)

# Function to get yaml property using dot notation e.g https.port instead of ['https']['port']
# returning the value
def getValue(property,yamlInput,placeholdersNotFound):
    keys = re.split("\.",property)
    res = yamlInput
    for v in keys:
        if v in res:
            res = res[v]
        else:
            placeholdersNotFound.add(property)
            res = '!!Missing <<'+property+'>>'
            break
    return res
