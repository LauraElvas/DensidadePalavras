# Menu script to facilitate the creation of density plots

# Possible Actions:
# - Create density plots for the 2D data and plot them
# - Visualise previously created data

import os

import DensityPlotCorp2
from DataCreatorCorp2 import loadData
from SquareSpacePlotCorp2 import loadSquareData

# Always print to console
import functools
print = functools.partial(print, flush=True)

# ------------------------------------ CONFIGURATIONS ----------------------------------------------

# Change these variables in order to increase the range and tick step in the color bar. 
maxCB = 20
step  = 5

# ----------------------------------------- CODE ---------------------------------------------------

# Changes in the following code may break it

def validateFunction(choice, type, numbChoices = None):
# Verifies if the value is in accordance with the type of option to be chosen
    # choice      - value of the choice made in the menu
    # type        - type of validation to be made, "option", "dataType", "word" or "dataChoice"
    # numbChoices - number of possible choices in "dataChoice"
    # return      - wether value is valid or not and choice, -1 invalidity of the choice or type

    # Check if choice is empty
    if (not choice):
        return False, -1

    # Verifies input for the option menu
    if (type == "option"):
        validationCondition = (choice == "1") or (choice == "2")

        return validationCondition, -1

    # Verifies input for the dataType menu
    if (type == "dataType"):
        validationCondition = (choice == "global") or (choice == "square")

        return validationCondition, -1

    # Verifies input for the metric
    if (type == "metric"):
        validationCondition = (choice == "cosine") or (choice == "dot") or (choice == "both")

        return validationCondition, choice

    # Verifies input for the word
    if (type == "word"):
        validationCondition = any(x.isnumeric() for x in choice)

        return not validationCondition, choice[0]

    # Verifies input for the dataChoice
    if (type == "dataChoice"):
        if (all(x.isnumeric() for x in choice) and len(choice) == len(set(choice))):
            choice = int(choice[0])
            if(choice > numbChoices or choice < 1):
                return False, -1

            return True, choice
    
    return False, -1

# Loop controling variables
run = True
menu = True

# Menu Loop
while (run):

    # User menu
    if (menu):
        print("What would you like to do?")
        print("1 - Create density plots for the 2D data and plot them")
        print("2 - Visualise previously created data")

        print()
        print("Warning:")
        print("- Creation actions will not show the plots but will save them in the correct folders")
        print("- In order to create the density plots, folders with data must already exist")

        option = input()

        # Validate answer - option
        validationCondition1, _ = validateFunction(option, "option")
        while (not validationCondition1):
            option = input("Input is neither 1, 2. Try again: ")
            validationCondition1, _ = validateFunction(option, "option")

        print()
        print("Density plots for global plots or square plots (\"global\" - global plots, \"square\" - square plots): ")
        dataType = input()

        # Validate answer - dataType
        validationCondition2, _ = validateFunction(dataType, "dataType")

        while (not validationCondition2):
            dataType = input(f"Input not valid, must be a number of those shown. Try again: ")
            validationCondition2, _ = validateFunction(dataType, "dataType")

        print()
        metric = input(f"Input if data created is based on cosine similarity, dot product or both (cosine for cosine similarity, dot for dot product or word \"both\"): ")

        # Validate answer - metric
        validationCondition3, metric = validateFunction(metric, "metric")

        while (not validationCondition3):
            metric = input(f"Input is not valid. Must be cosine, dot or word \"both\". Try again: ")
            validationCondition3, metric = validateFunction(metric, "metric")

        print()
        # Loop for checking word data
        dataExist = False
        while(not dataExist):
            print()
            print("For wich word should data be retrieved: ")
            words = input()

            # Validate answer - words
            words = words.split(",")
            if (len(words) > 1):
                validationCondition4 = False
            else:
                validationCondition4, words = validateFunction(words, "word")

            while (not validationCondition4):
                words = input("Input word not valid. Must be one single word: ")
                words = words.split(",")
                if (len(words) > 1):
                    validationCondition4 = False
                else:
                    validationCondition4, words = validateFunction(words, "word")

            print()

            # Checking if there is already data created
            print("Checking if data for word already created...")

            foldersList = os.listdir(os.path.join("Saved Data", "Corpus 2"))
            dataFolder = []
            # #_Plots folders list
            for folder in foldersList:
                for subfolder in os.listdir(os.path.join("Saved Data", "Corpus 2", folder)):
                    wrd = subfolder.split("_")[0]
                    if (words == wrd):
                        dataFolder.append([words, folder, subfolder])

            if (dataFolder == []):
                print("No data for chosen words")
            else:
                dataExist = True

        print("The following data was found: ")
        for count, data in enumerate(dataFolder):
            # Info
            squareSize = data[2].split("_")[1]

            # Check if checkpoints are made with a year difference
            print(count + 1, "-", f"{data[0]} for {data[1]} with a square size of {squareSize}")

        print()
        dataChoice = input("Input the number from where the density plots will be based: ")

        # Validate answer - dataChoice
        dataChoice = dataChoice.split(",")
        if(len(dataChoice) > 1):
            validationCondition5 = False
        else:
            validationCondition5, dataChoice = validateFunction(dataChoice, "dataChoice", len(dataFolder))

        while (not validationCondition5):
            dataChoice = input(f"Input not valid, must be a number from the ones shown. Try again: ")
            dataChoice = dataChoice.split(",")
            if(len(dataChoice) > 1):
                validationCondition5 = False
            else:
                validationCondition5, dataChoice = validateFunction(dataChoice, "dataChoice", len(dataFolder))

        print()
        menu = False

    # Create density plots for the 2D data and plot them
    if (option == "1"):
        numbPlots = int(dataFolder[dataChoice - 1][1].split("_")[0])

        # Density plots - global plots
        if (dataType == "global"):
            # Folder to retrieve complete dataframes
            dataF = os.path.join("Saved Data", "Corpus 2", dataFolder[dataChoice - 1][1])

            # Folder to save data
            saveFolder = os.path.join(dataF, dataFolder[dataChoice - 1][2], "densityPlots_" + dataFolder[dataChoice - 1][0])

            if not os.path.exists(saveFolder):
                os.makedirs(saveFolder)

            # Load data
            dataListComplete, limitsDict = loadData(numbPlots, metric, 2, dataF)

            # Density plot
            DensityPlotCorp2.densityPlot(dataListComplete, dataType, limitsDict, metric, maxCB, step, False, True, saveFolder)

        # Density plots - square plots
        if (dataType == "square"):
            # Folder to retrieve square dataframes
            dataF = os.path.join("Saved Data", "Corpus 2", dataFolder[dataChoice - 1][1], dataFolder[dataChoice - 1][2], "squarePlots_" + dataFolder[dataChoice - 1][0])

            # Folder to save data
            saveFolder = os.path.join("Saved Data", "Corpus 2", dataFolder[dataChoice - 1][1], dataFolder[dataChoice - 1][2], "densityPlots_" + dataFolder[dataChoice - 1][0])
            
            if not os.path.exists(saveFolder):
                os.makedirs(saveFolder)

            # Load data
            squareSide = float(dataFolder[dataChoice - 1][2].split("_")[1])
            if (squareSide % 1 == 0.0):
                halfEdge = squareSide // 2
            else:
                halfEdge = squareSide

            dataList, limitsList = loadSquareData(dataFolder[dataChoice - 1][0], halfEdge, metric, 2, dataF)

            # Density plot
            DensityPlotCorp2.densityPlot(dataList, dataType, limitsList, metric, maxCB, step, False, True, saveFolder)

    # Visualise previously created data
    if (option == "2"):
        numbPlots = int(dataFolder[dataChoice - 1][1].split("_")[0])
        
        # Density plots - global plots
        if (dataType == "global"):
            # Folder to retrieve complete dataframes
            dataF = os.path.join("Saved Data", "Corpus 2", dataFolder[dataChoice - 1][1])

            # Load data
            dataListComplete, limitsDict = loadData(numbPlots, metric, 2, dataF)

            # Density plot
            DensityPlotCorp2.densityPlot(dataListComplete, dataType, limitsDict, metric, maxCB, step)

        # Density plots - square plots
        if (dataType == "square"):
            # Folder to retrieve square dataframes
            dataF = os.path.join("Saved Data", "Corpus 2", dataFolder[dataChoice - 1][1], dataFolder[dataChoice - 1][2], "squarePlots_" + dataFolder[dataChoice - 1][0])

            # Load data
            squareSide = float(dataFolder[dataChoice - 1][2].split("_")[1])
            if (squareSide % 1 == 0.0):
                halfEdge = squareSide // 2
            else:
                halfEdge = squareSide

            dataList, limitsList = loadSquareData(dataFolder[dataChoice - 1][0], halfEdge, metric, 2, dataF)
    
            # Density plot
            DensityPlotCorp2.densityPlot(dataList, dataType, limitsList, metric, maxCB, step)

    end = True

    # End program menu
    while (end):
        print()
        endOption = input("End program (y/n)? ")

        if (endOption == "y" or endOption == "Y"):
            run = False
            end = False

        elif (endOption == "n" or endOption == "N"):
            menu = True
            end = False
            print()
        else:
            print("Input not valid. Please try again: ")