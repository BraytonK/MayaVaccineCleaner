import shutil
import sys
import os
import json

import maya.standalone
import maya.cmds as cmds
import maya.utils as utils

def normalizeNames():
    print("Normalizing Names")
    # Go through all folders in root directory
    for root, dirs, files in os.walk("X:/WayminderReloaded/Like"):
        for file in files:
            if file.endswith(".mb"):
                mayaFile = os.path.join(root, file).replace("\\", "/")
                movePath = mayaFile
                if mayaFile.endswith("_CLEANED.mb") or mayaFile.endswith("_INFECTED.mb"):
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
                        else:
                            normalized = True
                        print("File is normalized")
#WIP Logic to scan for scripts embeded into maya scene break up into seperate functions later
def scanFunc():
    # Root Directory for scanning
    rootDir = "X:/WayminderReloaded/Like"
   # rootDir = "X:/WayminderReloaded/Like/sequences/D"
    # Go trhough all folders in root directory
    for root, dirs, files in os.walk(rootDir):
        # Check if file is a maya file
        for file in files:
            # TODO, support .ma files
            if file.endswith(".mb") and not file.endswith("_OK.mb") and not file.endswith("_CLEANED.mb") and not file.endswith("_INFECTED.mb"):
                # Check if file is a maya file
                # use forwardslash for maya
                mayaFile = os.path.join(root, file).replace("\\", "/")
                checkVirus(mayaFile, True)
                #mayaFile = testDir
    
def checkVirus(testDir, quarantineIfVirus):
    quarantinePrefix = "X:/WayminderReloaded/Like"
    rootDir = "X:/WayminderReloaded/Like"
    movePath = ""
    currentPath = ""

    print("Checking: " + testDir)
    data= {}
    cmds.file(testDir, o=True, f=True)   
    # Find Virus Nodes
    virusFound = False
    print("TEST-----------------------------------------------------------------------------------")
    script_nodes = cmds.ls(type="script")
    print(script_nodes)
    for script in script_nodes:
        #Check if virus scripts are in scene
        if "breed" in script or "vaccine" in script or "gene" in script:
            virusFound = True
            break    
    
    if virusFound and quarantineIfVirus:
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        
        print("File to move : " + filepath)
        #replace prefix
        #if a virus exists, take the filepath of the virus and replace the dir prefix with the quarantine prefix
        #currentPath = filepath.replace(filepath, testDir)
        movePath = testDir.replace(rootDir, quarantinePrefix)
        #replace the file extension with _INFECTED.mb
        if filepath.endswith(".mb"):
            movePath = movePath.replace(".mb", "_INFECTED.mb")
        elif filepath.endswith(".ma"):
            movePath = movePath.replace(".ma", "_INFECTED.ma")
        #move file to quarantine
        print("Current path : " + testDir)
        print("Moving file to quarantine path : " + movePath)
        # create directory if it doesn't exist
        if not os.path.exists(os.path.dirname(movePath)):
            os.makedirs(os.path.dirname(movePath))
            shutil.move(filepath, movePath)
        # check if file exists
        elif os.path.isfile(movePath):
            # if file exists, delete file
            print("File already exists in quarantine")
        else:
            # if directory exists, move file
            shutil.move(filepath, movePath)
            print("File moved to quarantine")
    
        #log file
        data = {
            "filename": filename,
            "path": filepath
        }
    elif virusFound == False:
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        
        print("File to move : " + filepath)
        #replace prefix
        #if a virus exists, take the filepath of the virus and replace the dir prefix with the quarantine prefix
        #currentPath = filepath.replace(filepath, testDir)
        movePath = testDir.replace(rootDir, quarantinePrefix)
        #replace the file extension with _INFECTED.mb
        if filepath.endswith(".mb"):
            movePath = movePath.replace(".mb", "_OK.mb")
        elif filepath.endswith(".ma"):
            movePath = movePath.replace(".ma", "_OK.ma")
        #move file to quarantine
        print("Current path : " + testDir)
        print("Moving file to quarantine path : " + movePath)
        # create directory if it doesn't exist
        if not os.path.exists(os.path.dirname(movePath)):
            os.makedirs(os.path.dirname(movePath))
            shutil.move(filepath, movePath)
        # check if file exists
        elif os.path.isfile(movePath):
            # if file exists, delete file
            print("File already exists in quarantine")
        else:
            # if directory exists, move file
            shutil.move(filepath, movePath)
            print("File moved to quarantine")
    
        #log file
        data = {
            "filename": filename,
            "path": filepath
        }
    #Create json if it doesn't exist
    jsonPath = "C:/Users/user/Desktop/scan.json"
    if not os.path.isfile(jsonPath):
        with open(jsonPath, "w") as json_file:
            json.dump(data, json_file)
        print("JSON file created successfully.")
    #Append to json if it exists
    else:
        with open(jsonPath, 'a') as outfile:
            outfile.write(json.dumps(data))
            outfile.write(",")
            outfile.close()
    
    return virusFound
    

def cleanFiles():
    print("Cleaning Files")
    # Go through all folders in quarantine directory
    for root, dirs, files in os.walk("X:/WayminderReloaded/Like"):
        # Check if file is a maya file
        #TODO, support .ma files
        for file in files:
            if file.endswith("_INFECTED.mb"):
                # use forwardslash for maya
                mayaFile = os.path.join(root, file).replace("\\", "/")
                print("Cleaning: " + mayaFile)
                os.system("maya.exe -batch -file " + mayaFile + " -command \"evalDeferred (\\\"loadPlugin MayaScanner; MayaScan;\\\")\"")
                # change file name to _Cleaned.mb
                if mayaFile.endswith(".mb"):
                    cleanedFilepath = mayaFile.replace(".mb", "_CLEANED.mb")
                elif mayaFile.endswith(".ma"):
                    cleanedFilepath = mayaFile.replace(".ma", "_CLEANED.ma")
                # replace file name
                os.rename(mayaFile, cleanedFilepath)

def checkClean():
    print("Unquarantine Files")
    # Go through all folders in quarantine directory
    quarantineDir = "X:/WayminderReloaded/Like"
    for root, dirs, files in os.walk(quarantineDir):
        # Check if file is a maya file
        #TODO, support .ma files
        for file in files:
            if file.endswith("_CLEANED.mb"):
                # use forwardslash for maya
                mayaFile = os.path.join(root, file).replace("\\", "/")
                # Check if file has virus
                print("Checking: " + mayaFile)
                #Use already existing check virus function for this
                cmds.file(mayaFile, o=True, f=True)   
                # Find Virus Nodes
                virusfound = False
                print("TEST-----------------------------------------------------------------------------------")
                script_nodes = cmds.ls(type="script")
                #print(script_nodes)
                for script in script_nodes:
                    #Check if virus scripts are in scene
                    if "breed" in script or "vaccine" in script or "gene" in script:
                        virusfound = True
                        break    
                if checkVirus(mayaFile, False) == False:
                    #move file back to original directory
                    movePath = mayaFile.replace(quarantineDir, "X:/WayminderReloaded/Like")
                    if mayaFile.endswith("_CLEANED.mb"):
                        movePath = movePath.replace("_INFECTED_CLEANED.mb", ".mb")
                    elif mayaFile.endswith("_CLEANED.ma"):
                        movePath = movePath.replace("_INFECTED_CLEANED.ma", ".ma")
                    shutil.move(mayaFile, movePath)
                    print("File is safe")

print("Maya Vaccine Scan")
print("0 = Normalize Names")
print("1 = Scan for virus")
print("2 = Clean virus")
print("3 = Unquarantine virus")
print("4 = Scan, Clean, Unquarantine virus")

#have python command line arguments to run different functions
# print 1 = scan, print 2 = clean, print 3 = unquarantine
# ask for user input
# if input == 1, run scan function
# if input == 2, run clean function
# if input == 3, run unquarantine function
# if input == 4, run all functions

arg = int(input())
if arg == 0:
    normalizeNames()
if arg == 1:
    print("Please check if a Maya Enviroment is running in your Python Console as documented.")
    print("Is Maya Enviroment running? 1 = yes, 0 = no")
    isMayaEnv = int(input())
    if (isMayaEnv == 1):
        #Start up Maya 
        maya.standalone.initialize()

        #Let Maya Load before running script
        utils.executeDeferred(scanFunc())

        maya.standalone.uninitialize()    
    else:
        print("Please start up a Maya Enviroment in your Python Console")
elif arg == 2:
    cleanFiles()
elif arg == 3:
    checkClean()
elif arg == 4:
    print("Please check if a Maya Enviroment is running in your Python Console as documented: y/n??")
    if input() == "y":
        #Start up Maya 
        maya.standalone.initialize()

        #Let Maya Load before running script
        utils.executeDeferred(scanFunc())

        maya.standalone.uninitialize()    
    else:
        print("Please start up a Maya Enviroment in your Python Console")
    #cleanFiles()
    #checkClean()

