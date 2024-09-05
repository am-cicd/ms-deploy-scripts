import zipfile
import os
import shutil
from datetime import datetime


#Takes a jar file location as an input parameter and unpacks it to a
# directory of the same name and path. e.g if you pass in /mydir/myapp.jar
# the resulting directory will be /mydir/myapp
# input deleteSource - True/False indicating whether the original jar should be
#                      deleted on completion of the unzip
# returns the path to the directory
def unpack(jarFile,deleteSource):

    print("Beginning unpack of jar file located at " + jarFile)

    #Store the current working directory so we can change back at the end of the function
    owd = os.getcwd()

    #Jar file is unpacked to a directory named the same without an extension
    destinationDirectory = os.path.splitext(jarFile)[0]

    #Check directory doesn't already contain data
    for dirpath, dirnames, files in os.walk(destinationDirectory):
        if files:
            raise FileExistsError('Destination directory for unpacked jar file ' + destinationDirectory + ' already contains files.')


    os.makedirs(destinationDirectory)

    #Move the original if we are allowed to deleteSource, otherwise copy it to
    #our working directory
    if deleteSource is True:
        os.rename(jarFile, destinationDirectory + "/source.jar")
    else:
        shutil.copy(jarFile, destinationDirectory + "/source.jar")

    #Unpack the jar file to our working directory
    os.chdir(destinationDirectory)
    os.system("jar xf source.jar")

    #Delete the jar file we unpacked and change back to the original directory
    os.remove("source.jar")
    os.chdir(owd)

    print("Completed unpack of jar file ")
    return destinationDirectory


#Takes a jar file and the location of a file relative to the jar file (inside it)
# and extracts it out to the current working directory at the same path
def unpackSingleFile(jarFile,fileLocation):

    print(str(datetime.now()) + " Beginning extract of " + fileLocation + " from jar file located at " + jarFile)

    os.system("jar xf " + jarFile + " " + fileLocation)

    #Delete the jar file we unpacked and change back to the original directory
    print(str(datetime.now()) + " Completed unpack of " + fileLocation + " from jar file located at " + jarFile)


# Takes a directory as an input parameter and packs it to a jar/zip file
# of the name specified in outputFile
#
# returns the path to the directory
def repack(sourceDirectory, outputFile):

    print("Beginning repack of directory " + sourceDirectory + " to " + outputFile)
    owd = os.getcwd()

    #Pack the new jar file
    os.chdir(sourceDirectory)
    os.system("jar cf packed.jar .")

    #Move the new jar file to the actual location the user wanted
    os.chdir(owd)
    os.rename(sourceDirectory + "/packed.jar", outputFile)

    print("Completed repack of directory to jar file")
    return outputFile
    
# Takes a jar file and a file location and adds this file to the jar
#
# returns the location of the jar file
def repackSingleFile(jarFile, fileLocation):

    print(str(datetime.now()) + " Beginning repack of " + fileLocation + " to " + jarFile)

    #Pack the new file
    os.system("jar uf0 " + jarFile + " " + fileLocation)

    print(str(datetime.now()) + " Completed repack of " + fileLocation + " to " + jarFile)
    return jarFile
    
# Takes a file location and removes the file
#
# returns the location of the deleted file    
def deleteFile(fileLocation):
    os.remove(fileLocation)
    return fileLocation
    
