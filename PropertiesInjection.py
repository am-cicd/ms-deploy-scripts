import sys
import argparse
from . import YAMLReplacer
from . import JarUnpacker

def loadCommandArg(args):
    #Load our command line arguments
    parser=argparse.ArgumentParser()
    parser.add_argument('-e', '--environmentProperties', required=True, help='Path to the environment properties YAML file containing the values to be injected')
    parser.add_argument('-j', '--jarFile', required=True, help='Path to the jar/zip file of the application/domain requiring property injection')
    parser.add_argument('-p', '--propertiesType', required=False, help='Type of properties file within the app - Accepted values are yaml/properties', default='yaml')
    parser.add_argument('-a', '--artifactType', required=False, help='Type of Artifact', default='app')
    args=parser.parse_args()
    return args


commandArg = loadCommandArg()
propertiesType = commandArg.propertiesType
jarFile = commandArg.jarFile
environmentProperties = commandArg.environmentProperties
artifactType = commandArg.artifactType

#Define the default location of our placeholder and resulting configuration files
#extension is .yaml or .properties from --propertiesType
if propertiesType == 'properties':
    CONFIG_PLACEHOLDERS_PATH="classes/config/configuration-placeholders." + propertiesType
    CONFIG_FILE_PATH="classes/config/configuration." + propertiesType
    LOG4J_PLACEHOLDERS_PATH="classes/log4j2-placeholders.xml"
    LOG4J_PATH="classes/log4j2.xml"
else:
    CONFIG_PLACEHOLDERS_PATH="config/configuration-placeholders." + propertiesType
    CONFIG_FILE_PATH="config/configuration." + propertiesType
    LOG4J_PLACEHOLDERS_PATH="log4j2-placeholders.xml"
    LOG4J_PATH="log4j2.xml"

#Perform replacement on YAML/Properties properties file
JarUnpacker.unpackSingleFile(jarFile,CONFIG_PLACEHOLDERS_PATH)
missingPlaceholders = YAMLReplacer.replaceValues(environmentProperties, CONFIG_PLACEHOLDERS_PATH, CONFIG_FILE_PATH)
JarUnpacker.repackSingleFile(jarFile,CONFIG_FILE_PATH)
JarUnpacker.deleteFile(CONFIG_PLACEHOLDERS_PATH)
JarUnpacker.deleteFile(CONFIG_FILE_PATH)
if(len(missingPlaceholders) >= 1):
    print("Warning - The following property placeholders were found with no corresponding values:")
    for key in missingPlaceholders:
        print("- " + str(key))
    raise Exception('Failed to inject properties, placeholders were found with no corresponding values. See above log entries for missing placeholder list')


#For apps - perform replacement on log4j2-placeholders.xml if it exists otherwise try on log4j2.xml
if artifactType == "app":
    try:
        JarUnpacker.unpackSingleFile(jarFile,LOG4J_PLACEHOLDERS_PATH)
        missingPlaceholders = YAMLReplacer.replaceValues(environmentProperties, LOG4J_PLACEHOLDERS_PATH, LOG4J_PATH)
        JarUnpacker.repackSingleFile(jarFile,LOG4J_PATH)
        JarUnpacker.deleteFile(LOG4J_PLACEHOLDERS_PATH)
        JarUnpacker.deleteFile(LOG4J_PATH)
    except FileNotFoundError:
        print("Warning - did not find a log4j2-placeholders.xml file, attempting to replace values in log4j2.xml instead")
        JarUnpacker.unpackSingleFile(jarFile,LOG4J_PATH)
        missingPlaceholders = YAMLReplacer.replaceValues(environmentProperties, LOG4J_PATH, LOG4J_PATH)
        JarUnpacker.repackSingleFile(jarFile,LOG4J_PATH)
        JarUnpacker.deleteFile(LOG4J_PATH)

    #Check for missing placeholders in the log4j replacement
    if(len(missingPlaceholders) >= 1):
        print("Warning - The following property placeholders were found IN THE LOG4J CONFIG with no corresponding values:")
        for key in missingPlaceholders:
            print("- " + str(key))
            raise Exception('Failed to inject properties into log4j config, placeholders were found with no corresponding values. See above log entries for missing placeholder list')
else:
    print ("Artifact is a domain - skipping placeholder replacement log4j2.xml")

print("Completed Property Injection")
sys.exit(0)
