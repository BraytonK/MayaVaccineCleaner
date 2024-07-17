import shutil
import sys
import os
import json
import time
import threading

import maya.standalone
import maya.cmds as cmds
import maya.utils as utils

# Define a function to handle the timeout
def timeout_handler(signum, frame):
    raise TimeoutError("checkVirus function timed out")

def nomalizeCleanMeNames(rootDir):
    print("Normalizing Names")
    # Go through all folders in root directory
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            if file.endswith("_CLEANME.mb") or file.endswith("_CLEANME.ma"):
                mayaFile = os.path.join(root, file).replace("\\", "/")
                print("Checking: " + mayaFile)
                movePath = mayaFile
                normalized = False
                while normalized == False:
                    mayaFile = movePath
                    # Check if file is a maya file
                    if mayaFile.endswith("_CLEANME.mb"):
                        movePath = mayaFile.replace("_CLEANME.mb", ".mb")
                        shutil.move(mayaFile, movePath)
                    elif mayaFile.endswith("_CLEANME.ma"):
                        movePath = mayaFile.replace("_CLEANME.ma", ".ma")
                        shutil.move(mayaFile, movePath)
                    else:
                        normalized = True
                    print("File is normalized")

def swapDuplicateFiles(rootDir, dupDir):
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            if file.endswith(".mb") or file.endswith(".ma"):
                mayaFile = os.path.join(root, file).replace("\\", "/")
                oldPath = mayaFile
                #remove path from file
                oldFile = os.path.basename(oldPath)
                print("Checking: " + oldFile)
                for root, dirs, files in os.walk(dupDir):
                    for file in files:
                        if file.endswith(".mb") or file.endswith(".ma"):
                            mayaFile = os.path.join(root, file).replace("\\", "/")
                            newFile = os.path.basename(mayaFile)
                            print("Checking against: " + newFile)
                            if newFile == oldFile:
                                print("File is a duplicate")
                                if mayaFile.endswith(".mb"):
                                    #ask user if they want to swap files
                                    print("Duplicate found: " + oldFile + " and " + newFile)
                                    print("Do you want to swap files? y/n")
                                    if input() == "y":
                                        print("Duplicate ! Moving: " + mayaFile + " to " + movePath)
                                        movePath = oldPath.replace(".mb", "_DUPLICATE.mb")
                                        shutil.move(mayaFile, movePath)
                                        shutil.move(oldPath, mayaFile)
                                elif mayaFile.endswith(".ma"):
                                    print("Duplicate found: " + oldFile + " and " + newFile)
                                    print("Do you want to swap files? y/n")
                                    if input() == "y":
                                        movePath = oldPath.replace(".ma", "_DUPLICATE.ma")
                                        print("Duplicate ! Moving: " + mayaFile + " to " + movePath)
                                        shutil.move(mayaFile, movePath)
                                        shutil.move(oldPath, mayaFile)
                                print("File is a duplicate")
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
                if mayaFile.endswith("_CLEANED.mb") or mayaFile.endswith("_INFECTED.mb") or mayaFile.endswith("_OK.mb") or mayaFile.endswith("_MOCKCLEANED.mb"):
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
                        elif mayaFile.endswith("_MOCKCLEANED.mb"):
                            movePath = movePath.replace("_MOCKCLEANED.mb", ".mb")
                            shutil.move(mayaFile, movePath)
                        else:
                            normalized = True
                        print("File is normalized")
            elif file.endswith(".ma"):
                mayaFile = os.path.join(root, file).replace("\\", "/")
                print("Checking: " + mayaFile)
                movePath = mayaFile
                if mayaFile.endswith("_CLEANED.ma") or mayaFile.endswith("_INFECTED.ma") or mayaFile.endswith("_OK.ma") or mayaFile.endswith("_MOCKCLEANED.ma"):
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
                        elif mayaFile.endswith("_MOCKCLEANED.ma"):
                            movePath = movePath.replace("_MOCKCLEANED.ma", ".ma")
                            shutil.move(mayaFile, movePath)
                        else:
                            normalized = True
                        print("File is normalized")

# Scans through all maya files in a given directory
def scanFunc(rootDir, quarantinePrefix):
    # Set the timeout duration in seconds
    timeout_duration = 3*60

    # Set the signal handler for the timeout

    # Go through all folders in root directory
    for root, dirs, files in os.walk(rootDir):
        # Check if file is a maya file
        for file in files:
            if file.endswith(".mb") and not file.endswith("_OK.mb") and not file.endswith("_CLEANED.mb")and not file.endswith("_INFECTED.mb") and not file.endswith("_TIMEOUT.mb") and not file.endswith("_CLEANME.mb"):
                # Check if file is a maya file
                # use forwardslash for maya
                print("Scanning: " + file)
                # print full path
                print(os.path.join(root, file))
                mayaFile = os.path.join(root, file).replace("\\", "/")

                # create thread for checkVirus function with parameters
                checkVirusThread = threading.Thread(target=checkVirus, args=(mayaFile, rootDir, quarantinePrefix))
                # try to run checkVirus function, if it takes too long then move on

                checkVirusThread.start()
                checkVirusThread.join(timeout_duration)

                if checkVirusThread.is_alive():
                    print("checkVirus function timed out. Moving on...")
                    movePath = ""
                    currentPath = ""
                    filepath = cmds.file(q=True, sn=True)
                    filename = os.path.basename(filepath)
                    
                    print("File to move : " + mayaFile)
                    #replace prefix
                    #if a virus exists, take the filepath of the virus and replace the dir prefix with the quarantine prefix
                    #currentPath = filepath.replace(filepath, rootDir)
                    movePath = mayaFile.replace(rootDir, quarantinePrefix)
                    #replace the file extension with _INFECTED.mb
                    if mayaFile.endswith(".mb"):
                        movePath = movePath.replace(".mb", "_TIMEOUT.mb")
                    elif mayaFile.endswith(".ma"):
                        movePath = movePath.replace(".ma", "_TIMEOUT.ma")
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
            
            if file.endswith(".ma") and not file.endswith("_OK.ma") and not file.endswith("_CLEANED.ma")and not file.endswith("_INFECTED.ma") and not file.endswith("_TIMEOUT.ma") and not file.endswith("_CLEANME.ma"):
                print("Scanning: " + file)
                # print full path
                print(os.path.join(root, file))
                mayaFile = os.path.join(root, file).replace("\\", "/")

                # create thread for checkVirus function with parameters
                checkVirusThread = threading.Thread(target=checkVirus, args=(mayaFile, rootDir, quarantinePrefix))
                # try to run checkVirus function, if it takes too long then move on
                checkVirusThread.start()
                checkVirusThread.join(timeout_duration)

                if checkVirusThread.is_alive():
                    print("checkVirus function timed out. Moving on...")
                    movePath = ""
                    currentPath = ""
                    filepath = cmds.file(q=True, sn=True)
                    filename = os.path.basename(filepath)
                    
                    print("File to move : " + mayaFile)
                    #replace prefix
                    #if a virus exists, take the filepath of the virus and replace the dir prefix with the quarantine prefix
                    #currentPath = filepath.replace(filepath, rootDir)
                    movePath = mayaFile.replace(rootDir, quarantinePrefix)
                    #replace the file extension with _INFECTED.mb
                    if mayaFile.endswith(".mb"):
                        movePath = movePath.replace(".mb", "_TIMEOUT.mb")
                    elif mayaFile.endswith(".ma"):
                        movePath = movePath.replace(".ma", "_TIMEOUT.ma")
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

# This function will check if a virus exists in the maya file
def checkVirus(mayaFile, rootDir, quarantinePrefix):
        movePath = ""
        currentPath = ""
        validFile = True
        print("Looking for virus: " + mayaFile)
        data= {}
        # catch errors and move on
        try:
            cmds.file(mayaFile, o=True, f=True)
        except:
            validFile = False

        if validFile == True:
            # Find Virus Nodes
            virusFound = False
            script_nodes = cmds.ls(type="script")
            isComplete = False
            for script in script_nodes:
                #Check if virus scripts are in scene
                if "breed" in script or "vaccine" in script or "gene" in script:
                    virusFound = True
                    break    

            if virusFound == True:
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
            
            elif virusFound == False:
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

        else:
            print("Error.. Please Check this File Manually")
            movePath = ""
            currentPath = ""
            
            print("Labeling : " + mayaFile + " as CleanMe")
            #replace prefix
            #if a virus exists, take the filepath of the virus and replace the dir prefix with the quarantine prefix
            #currentPath = filepath.replace(filepath, rootDir)
            movePath = mayaFile.replace(rootDir, quarantinePrefix)
            #replace the file extension with _INFECTED.mb
            if mayaFile.endswith(".mb"):
                movePath = movePath.replace(".mb", "_CLEANME.mb")
            elif mayaFile.endswith(".ma"):
                movePath = movePath.replace(".ma", "_CLEANME.ma")
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
        
        return virusFound
    
# Given the scan findings, this function will clean the files using the MayaScanner plugin
def cleanFiles(rootDir):
    print("Cleaning Files")
    # Go through all folders in quarantine directory
    for root, dirs, files in os.walk(rootDir):
        # Check if file is a maya file
        for file in files:
            if file.endswith("_INFECTED.mb") or file.endswith("_INFECTED.ma") or file.endswith("_CLEANME.mb") or file.endswith("_CLEANME.ma"):
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

#TODO finish this function
def cleanText(qurantineDir, rootDir):
  for root, dirs, files in os.walk(rootDir):
        # Check if file is a maya file
        # select line if there is no tab
        print("Cleaning Text")
        for file in files:
            if file.endswith(".mb") or file.endswith(".ma"):
                # if line starts with no tab, select line
                mayaFile = os.path.join(root, file).replace("\\", "/")
                if mayaFile.endswith(".mb") or mayaFile.endswith(".ma"):
                    # TODO : go line by line and check if there is no tab. If so, save the line number as start of the node
                        # check for ' vaccine ' or ' breed ' or ' gene ' in the line, until the next line with no tab
                        # if found, goto the next line with no tab and save the line number - 1 as end of the node
                        # select the lines from start to end and delete them
                    print("Cleaning: " + mayaFile)
                    endOfNode = 0
                    startOfNode = 0
                    numberOfLinesDeleted = 0
                    infectedNode = False
                    with open(mayaFile, 'r') as openedFile:
                        lines = openedFile.readlines()
                        lineCount = len(lines)
                        totalLinesDeleted = 0
                        infectedFile = False
                    #    infectedIndexArray = []
                        for i, line in enumerate(lines):
                            numberOfLinesDeleted = 0
                            if not line.startswith('\t'):
                                print('start of node' +  str(i))
                                if infectedNode == True:
                                    print("deleting lines: " + str(startOfNode) + " to " + str(endOfNode))
                                    # TODO, this is not working
                                    print("deleting " + lines[startOfNode] + " to: " + lines[endOfNode]) 
                                    del lines[startOfNode:endOfNode]
                                    numberOfLinesDeleted = endOfNode - startOfNode
                                    totalLinesDeleted = totalLinesDeleted + numberOfLinesDeleted
                                if "vaccine" in line or "breed" in line or "gene" in line:
                                    infectedNode = True
                                    infectedFile = True
                                    print("infected line: " + '(' + str(i) + ')' + line)
                                else:
                                    infectedNode = False
                                #startOfNode = i
                                startOfNode = i - totalLinesDeleted 
                            
                            if line.startswith('\t'):
                                print("midnode found at " + str(i))
                                # check for ' vaccine ' or ' breed ' or ' gene ' in the line, until the next line with no tab
                                #if "vaccine" in line or "breed" in line or "gene" in line:
                                #    infectedNode = True
                                #    print("infected line: " + '(' + str(i) + ')' + line)
                                    # if found, goto the next line with no tab and save the line number - 1 as end of the node
                                    # select the lines from start to end and delete them
                                    #startOfNode = i + 1
                                endOfNode = i - totalLinesDeleted + 1
                #ask user if they want the nodes to be deleted
            #    print("Do you want to delete the infected nodes? y/n")
            #    contDelete = input()
            #    if contDelete == "y":
            #        print(infectedIndexArray)
            #        deletedLines = 0
            #        for index in infectedIndexArray:
            #            deletedLines += index[1] - index[0]
            #            print("deleting lines: " + str(index[0]) + " to " + str(index[1]) + " with " + str(deletedLines) + " lines deleted")
            #            del lines[(index[0]-deletedLines):(index[1] - deletedLines)]
            #        print("Deleting infected nodes")
                    if infectedFile:
                        if mayaFile.endswith(".mb"):
                            # replace file name with _CLEANED.mb
                            cleanedFilepath = mayaFile.replace(".mb", "_INFECTED_CLEANED.mb")
                        elif mayaFile.endswith(".ma"):
                            cleanedFilepath = mayaFile.replace(".ma", "_INFECTED_CLEANED.ma")
                        # replace file name
                    else:
                        if mayaFile.endswith(".mb"):
                            # replace file name with _CLEANED.mb
                            cleanedFilepath = mayaFile.replace(".mb", "_OK.mb")
                        elif mayaFile.endswith(".ma"):
                            cleanedFilepath = mayaFile.replace(".ma", "_OK.ma")
                        # replace file name
                    
                    try:
                        os.rename(mayaFile, cleanedFilepath)
                        print("renamed file!")
                        with open(cleanedFilepath, 'w') as openedFile:
                            openedFile.writelines(lines)
                    except:
                        print("moving on")

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
    #print("Normalizing Names")
    #normalizeNames(InfectedRootDir)
    print("Normalizing CleanMe Names")
    nomalizeCleanMeNames(InfectedRootDir)
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
elif arg == 5:
    print("Enter the directory of the files you want to scan for duplicates:")
    DupRootDir = str(input())
    DupRootDir = DupRootDir.replace("\\", "/")
    swapDuplicateFiles(InfectedRootDir, DupRootDir)
    #checkClean()
elif arg == 6:
    cleanText(QuarantineRootDir, InfectedRootDir)