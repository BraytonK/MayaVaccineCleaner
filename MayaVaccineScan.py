import shutil
import sys
import os
import json

import maya.standalone
import maya.cmds as cmds
import maya.utils as utils

# This function will return all renamed files back to their original names
def normalizeNames(rootDir):
    print("Normalizing Names")
    # Go through all folders in root directory
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            if file.endswith(".mb"):
                mayaFile = os.path.join(root, file).replace("\\", "/")
                print("Checking: " + mayaFile)
                movePath = mayaFile
                if mayaFile.endswith("_CLEANED.mb") or mayaFile.endswith("_INFECTED.mb") or mayaFile.endswith("_OK.mb"):
                    normalized = False
                    while not normalized:
                        mayaFile = movePath
                        # Check if file is a maya file
                        if mayaFile.endswith("_CLEANED.mb"):
                            movePath = movePath.replace("_CLEANED.mb", ".mb")
                            shutil.move(mayaFile, movePath)
                        elif mayaFile.endswith("_INFECTED.mb"):
                            movePath = movePath.replace("_INFECTED.mb", ".mb")
                            shutil.move(mayaFile, movePath)
                        elif mayaFile.endswith("_OK.mb"):
                            movePath = movePath.replace("_OK.mb", ".mb")
                            shutil.move(mayaFile, movePath)
                        else:
                            normalized = True
                        print("File is normalized")
            elif file.endswith(".ma"):
                mayaFile = os.path.join(root, file).replace("\\", "/")
                print("Checking: " + mayaFile)
                movePath = mayaFile
                if mayaFile.endswith("_CLEANED.ma") or mayaFile.endswith("_INFECTED.ma") or mayaFile.endswith("_OK.ma"):
                    normalized = False
                    while not normalized:
                        mayaFile = movePath
                        # Check if file is a maya file
                        if mayaFile.endswith("_CLEANED.ma"):
                            movePath = movePath.replace("_CLEANED.ma", ".ma")
                            shutil.move(mayaFile, movePath)
                        elif mayaFile.endswith("_INFECTED.ma"):
                            movePath = movePath.replace("_INFECTED.ma", ".ma")
                            shutil.move(mayaFile, movePath)
                        elif mayaFile.endswith("_OK.ma"):
                            movePath = movePath.replace("_OK.ma", ".ma")
                            shutil.move(mayaFile, movePath)
                        else:
                            normalized = True
                        print("File is normalized")

# Scans through all maya files in a given directory
def scanFunc(rootDir, quarantinePrefix):
    # Go through all folders in root directory
    for root, dirs, files in os.walk(rootDir):
        # Check if file is a maya file
        for file in files:
            # TODO, support .ma files
            if file.endswith(".mb") and not file.endswith("_OK.mb") and not file.endswith("_CLEANED.mb")and not file.endswith("_INFECTED.mb"):
                # Check if file is a maya file
                # use forwardslash for maya
                print("Scanning: " + file)
                # print full path
                print(os.path.join(root, file))
                mayaFile = os.path.join(root, file).replace("\\", "/")
                checkVirus(mayaFile, rootDir, quarantinePrefix)
            
            if file.endswith(".ma") and not file.endswith("_OK.ma") and not file.endswith("_CLEANED.ma")and not file.endswith("_INFECTED.ma"):
                print("Scanning: " + file)
                # print full path
                print(os.path.join(root, file))
                mayaFile = os.path.join(root, file).replace("\\", "/")
                checkVirus(mayaFile, rootDir, quarantinePrefix)

# This function will check if a virus exists in the maya file
def checkVirus(mayaFile, rootDir, quarantinePrefix):
    movePath = ""
    currentPath = ""

    print("Checking: " + mayaFile)
    data= {}
    # catch errors and move on
    try:
        cmds.file(mayaFile, o=True, f=True)
    except:
        print("Error.. Moving on")

    # Find Virus Nodes
    virusFound = False
    script_nodes = cmds.ls(type="script")
    print(script_nodes)
    for script in script_nodes:
        #Check if virus scripts are in scene
        if "breed" in script or "vaccine" in script or "gene" in script:
            virusFound = True
            break    
    
    if virusFound == True:
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        
        print("File to move : " + mayaFile)
        #replace prefix
        #if a virus exists, take the filepath of the virus and replace the dir prefix with the quarantine prefix
        #currentPath = filepath.replace(filepath, rootDir)
        movePath = mayaFile.replace(rootDir, quarantinePrefix)
        #replace the file extension with _INFECTED.mb
        if mayaFile.endswith(".mb"):
            movePath = movePath.replace(".mb", "_INFECTED.mb")
        elif mayaFile.endswith(".ma"):
            movePath = movePath.replace(".ma", "_INFECTED.ma")
        #move file to quarantine
        print("Current path : " + mayaFile)
        print("Moving file to quarantine path : " + movePath)
        # create directory if it doesn't exist
        if not os.path.exists(os.path.dirname(movePath)):
            os.makedirs(os.path.dirname(movePath))
            shutil.move(mayaFile, movePath)
        # check if file exists
        elif os.path.isfile(movePath):
            # if file exists, delete file
            print("File already exists in path")
        else:
            # if directory exists, move file
            shutil.move(mayaFile, movePath)
    
        #log file
        data = {
            "filename": filename,
            "path": mayaFile
        }
    elif virusFound == False:
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        
        print("File to move : " + mayaFile)
        #replace prefix
        #if a virus exists, take the filepath of the virus and replace the dir prefix with the quarantine prefix
        #currentPath = filepath.replace(filepath, rootDir)
        movePath = mayaFile.replace(rootDir, quarantinePrefix)
        #replace the file extension with _INFECTED.mb
        if mayaFile.endswith(".mb"):
            movePath = movePath.replace(".mb", "_OK.mb")
        elif mayaFile.endswith(".ma"):
            movePath = movePath.replace(".ma", "_OK.ma")
        #move file to quarantine
        # create directory if it doesn't exist
        if not os.path.exists(os.path.dirname(movePath)):
            os.makedirs(os.path.dirname(movePath))
            shutil.move(mayaFile, movePath)
        # check if file exists
        elif os.path.isfile(movePath):
            # if file exists, delete file
            print("File already exists in path")
        else:
            # if directory exists, move file
            shutil.move(mayaFile, movePath)
    
        #log file
        data = {
            "filename": filename,
            "path": filepath
        }

    # Uncomment this if you want to log the files that are scanned

#    #Create json file if it doesn't exist
#    jsonPath = "C:/Users/user/Desktop/scan.json"
#    if not os.path.isfile(jsonPath):
#        with open(jsonPath, "w") as json_file:
#            json.dump(data, json_file)
#        print("JSON file created successfully.")
#    #Append to json if it exists
#    else:
#        with open(jsonPath, 'a') as outfile:
#            outfile.write(json.dumps(data))
#            outfile.write(",")
#            outfile.close()
    
    return virusFound
    
# Given the scan findings, this function will clean the files using the MayaScanner plugin
def cleanFiles(rootDir):
    print("Cleaning Files")
    # Go through all folders in quarantine directory
    for root, dirs, files in os.walk(rootDir):
        # Check if file is a maya file
        for file in files:
            if file.endswith("_INFECTED.mb") or file.endswith("_INFECTED.ma"):
                # use forwardslash for maya
                mayaFile = os.path.join(root, file).replace("\\", "/")
                print("Cleaning: " + mayaFile)
                os.system("maya.exe -batch -file " + "\"" + mayaFile + "\"" + " -command \"evalDeferred (\\\"loadPlugin MayaScanner; MayaScan;\\\")\"")
                #os.system("maya.exe -file -batch " + mayaFile)
                # change file name to _Cleaned.mb
                if mayaFile.endswith(".mb"):
                    cleanedFilepath = mayaFile.replace(".mb", "_CLEANED.mb")
                elif mayaFile.endswith(".ma"):
                    cleanedFilepath = mayaFile.replace(".ma", "_CLEANED.ma")
                # replace file name
                os.rename(mayaFile, cleanedFilepath)

# Check if cleaned files are still infected
def checkClean(quarantineDir, rootDir):
    print("Unquarantine Files")
    for root, dirs, files in os.walk(quarantineDir):
        for file in files:
            mayaFile = os.path.join(root, file).replace("\\", "/")
            movePath = mayaFile.replace(quarantineDir, rootDir) 
            if file.endswith("_OK.mb") or file.endswith("_OK.ma"):
                if mayaFile.endswith("_OK.mb"):
                    movePath = movePath.replace("_OK.mb", ".mb")
                elif mayaFile.endswith("_OK.ma"):
                    movePath = movePath.replace("_OK.ma", ".ma")
                shutil.move(mayaFile, movePath)
            elif file.endswith("_CLEANED.mb") or file.endswith("_CLEANED.ma"):
                print("Checking: " + mayaFile)
                #Use already existing check virus function for this
                virusfound = False

                # catch errors and move ono
                try:
                    cmds.file(mayaFile, o=True, f=True)
                except:
                    print("Error.. Moving on")

                print("Virus found: " + str(virusfound))
                # Find Virus Nodes
                script_nodes = cmds.ls(type="script")
                #print(script_nodes)
                for script in script_nodes:
                    #Check if virus scripts are in scene
                    if "breed" in script or "vaccine" in script or "gene" in script:
                        virusfound = True
                        print("Virus found")
                        break    
                print("Virus found: " + str(virusfound))
                if virusfound == False:
                    print("File is clean, moving back to original directory")
                    #move file back to original directory
                    if mayaFile.endswith("_CLEANED.mb"):
                        movePath = movePath.replace("_INFECTED_CLEANED.mb", ".mb")
                    elif mayaFile.endswith("_CLEANED.ma"):
                        movePath = movePath.replace("_INFECTED_CLEANED.ma", ".ma")
                else:
                    print("File is still infected, marking CleanMe")
                    if mayaFile.endswith("_CLEANED.mb"):
                        movePath = movePath.replace("_INFECTED_CLEANED.mb", "_CLEANME.mb")
                    elif mayaFile.endswith("_CLEANED.ma"):
                        movePath = movePath.replace("_INFECTED_CLEANED.ma", "_CLEANME.ma")
                    shutil.move(mayaFile, movePath)
                    print("File is still infected" + movePath)

                if not os.path.exists(os.path.dirname(movePath)):
                    print("Directory does not exist.. Creating directory")
                    os.makedirs(os.path.dirname(movePath))
                    shutil.move(mayaFile, movePath)
        # check if file exists
                elif os.path.isfile(movePath):
            # if file exists, delete file
                    print("File already exists in path")
                else:
                    print("Directory exists.. Moving file")
            # if directory exists, move file
                    shutil.move(mayaFile, movePath)
                print("Done")

print("Maya Vaccine Scan")
print("0 = Normalize Names")
print("1 = Scan for virus and label infected files")
print("2 = Clean virus")
print("3 = Unquarantine virus")
print("4 = Scan, Clean, Unquarantine virus")
arg = int(input())

#have python command line arguments to run different functions
# print 1 = scan, print 2 = clean, print 3 = unquarantine
# ask for user input
# if input == 1, run scan function
# if input == 2, run clean function
# if input == 3, run unquarantine function
# if input == 4, run all functions
print("Please enter the directory of the files you want to scan")
InfectedRootDir = str(input())
InfectedRootDir = InfectedRootDir.replace("\\", "/")
print("Please enter the directory of the quarantine folder (if you don't have one, enter the same directory as the infected files)")
QuarantineRootDir = str(input())
QuarantineRootDir = QuarantineRootDir.replace("\\", "/")
if arg == 0:
    normalizeNames(InfectedRootDir)
if arg == 1:
    print("Please check if a Maya Enviroment is running in your Python Console as documented.")
    print("Is Maya Enviroment running? 1 = yes, 0 = no")
    isMayaEnv = int(input())
    if (isMayaEnv == 1):
        #Start up Maya 
        maya.standalone.initialize()

        #Let Maya Load before running script
        utils.executeDeferred(scanFunc(InfectedRootDir, QuarantineRootDir))

        maya.standalone.uninitialize()    
    else:
        print("Please start up a Maya Enviroment in your Python Console")
elif arg == 2:
    cleanFiles(InfectedRootDir)
elif arg == 3:
        maya.standalone.initialize()

        #Let Maya Load before running script
        utils.executeDeferred(checkClean(InfectedRootDir, QuarantineRootDir))

        maya.standalone.uninitialize() 
    # Once quarantine is done, check if files are still infected
elif arg == 4:
    print("Please check if a Maya Enviroment is running in your Python Console as documented: y/n??")
    if input() == "y":
        #Start up Maya 
        maya.standalone.initialize()

        #Let Maya Load before running script
        utils.executeDeferred(scanFunc(InfectedRootDir, QuarantineRootDir))

        maya.standalone.uninitialize()    
    else:
        print("Please start up a Maya Enviroment in your Python Console")
    #cleanFiles()
    #checkClean()