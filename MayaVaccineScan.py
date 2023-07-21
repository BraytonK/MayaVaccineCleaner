import shutil
import sys
import os
import json

import maya.standalone
import maya.cmds as cmds
import maya.utils as utils


#WIP Logic to scan for scripts embeded into maya scene break up into seperate functions later
def scanFunc():
    # Root Directory for scanning
   # rootDir = "X:/WayminderReloaded/Like/sequences/D"
    logFileCurrentPrefix = "X:/WayminderReloaded/Like"
   # logFileCurrentPrefix = "X:/WayminderReloaded/Like/sequences/D"
    # Go trhough all folders in root directory
    for root, dirs, files in os.walk(logFileCurrentPrefix):
        # Check if file is a maya file
        for file in files:
            if file.endswith(".mb"):
                # Check if file is a maya file
                # use forwardslash for maya
                mayaFile = os.path.join(root, file).replace("\\", "/")
                checkVirus(mayaFile)
                #mayaFile = testDir
    
def checkVirus(testDir):
    logFileNewPrefix = "C:/Users/user/Documents/MayaVaccineScan/LikeScanned"
    quarantinePrefix = "C:/Users/user/Documents/MayaVaccineScan/LikeQuarantine"
    movePath = ""
    currentPath = ""

    print("Checking: " + testDir)
    data= {}
    cmds.file(testDir, o=True, f=True)   
    # Find Virus Nodes
    virusfound = False
    print("TEST-----------------------------------------------------------------------------------")
    script_nodes = cmds.ls(type="script")
    print(script_nodes)
    for script in script_nodes:
        #Check if virus scripts are in scene
        if "breed" in script or "vaccine" in script or "gene" in script:
            virusfound = True
            break    
    
    if virusfound:
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        
        print("File to move : " + filepath)
        #replace prefix
        currentPath = filepath.replace(filepath, logFileNewPrefix)
        movePath = currentPath.replace(logFileNewPrefix, quarantinePrefix)
        #replace the file extension with _INFECTED.mb
        movePath = movePath.replace(".mb", "_INFECTED.mb")
        #move file to quarantine
        print("Current path : " + currentPath)
        print("Moving file to quarantine path : " + movePath)
        # create directory if it doesn't exist
        if not os.path.exists(os.path.dirname(movePath)):
            os.makedirs(os.path.dirname(movePath))
        shutil.move(filepath, movePath)
        print("File moved to quarantine")
    
        #add file name to file
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
    

def cleanFiles():
    print("Cleaning Files")
    #os.system("maya.exe -batch -file" + filepath + " -command \"evalDeferred (\\\"loadPlugin MayaScanner; MayaScan;\")\"")

def unQuarantineFiles():
    print("Unquarantine Files")

print("Maya Vaccine Scan")
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
    unQuarantineFiles()
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
    cleanFiles()
    unQuarantineFiles()

