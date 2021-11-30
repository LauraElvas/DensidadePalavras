# Menu script to facilitate the creation of square plots centered in a given word

# Possible Actions:
# - Create dataframes for square plots centered in a given word with a given size and plot them
# - Load all the created dataframes and plot them

import os

import SquareSpacePlotCorp2
from DataCreatorCorp2 import loadData

# Always print to console
import functools
print = functools.partial(print, flush=True)

#--------------------------------------- CONFIGURATIONS ----------------------------------------------

# Change this variable if plotting the labels along with the datapoints is not necessary
labels = True

#------------------------------------------- CODE ----------------------------------------------------

# Changes in the following code may break it

def validateFunction(choice, type):
    # Verifies if the value is in accordance with the type of option to be chosen
    # choice   - value of the choice made in the menu
    # type     - type of validation to be made, "option", "metric", "dimension", "numPlots", "word" or "halfEdge"
    # return   - wether value is valid or not and choice, -1 is invalidity of the choice or type

    # Check if choice is empty
    if (not choice):
        return False, -1

    # Verifies input for the option menu
    if (type == "option"):
        validationCondition = (choice == "1") or (choice == "2")

        return validationCondition, -1

    # Verifies input for the metric
    if (type == "metric"):
        validationCondition = (choice == "cosine") or (choice == "dot") or (choice == "both")

        return validationCondition, choice

    # Verifies input for the dimension
    if (type == "dimension"):
        validationCondition = (choice == "2") or (choice == "3") or (choice == "both")

        if (choice.isnumeric()):
            choice = int(choice)

        return validationCondition, choice

    # Verifies input for the halfEdge
    if (type == "halfEdge"):
        try:
            choice = float(choice)
        except ValueError:
            return False, -1
        else:
            if ((choice >= 1) and (choice % 1 == 0)):
                choice = int(choice)
            elif(choice < 1 and choice > 0):
                choice = float(choice)

            return True, choice

    # Verifies input for the numPlots
    if (type == "numPlots"):
        validationCondition = all(x.isnumeric() for x in choice)
        
        if (not validationCondition):
            return False, -1
        else:
            choice = int(choice[0])
            validationCondition = (str(choice) + "_plots") in os.listdir(os.path.join("Saved Data", "Corpus 2"))

            if (not validationCondition):
                return False, -1

            return True, choice

    # Verifies input for the word
    if (type == "word"):
        validationCondition = any(x.isnumeric() for x in choice)

        return not validationCondition, choice[0]

    return False, -1

# Loop controling variables
run = True
menu = True

# Menu Loop
while (run):

    # User menu
    if (menu):
        print("What would you like to do?")
        print("1 - Create data for square plots with a given size for a given word")
        print("2 - Load and visualise previously created data")

        print()
        print("Warning:")
        print("- Creation actions will not show the plots but will save them in the correct folders")

        option = input()

        # Validate answer - option
        validationCondition1, _ = validateFunction(option, "option")
        while (not validationCondition1):
            option = input("Input is neither 1, 2. Try again: ")
            validationCondition1, _ = validateFunction(option, "option")

        print()
        metric = input(f"Input if data created is based on cosine similarity, dot product or both (cosine for cosine similarity, dot for dot product or word \"both\"): ")

        # Validate answer - metric
        validationCondition2, metric = validateFunction(metric, "metric")

        while (not validationCondition2):
            metric = input(f"Input is not valid. Must be cosine, dot or word \"both\". Try again: ")
            validationCondition2, metric = validateFunction(metric, "metric")

        print()
        dimension = input(f"Input if data created must be 2D, 3D or both (2 for 2D, 3 for 3D or word \"both\"): ")

        # Validate answer - dimension
        validationCondition3, dimension = validateFunction(dimension, "dimension")

        while (not validationCondition3):
            dimension = input(f"Input is not valid. Must be 2, 3 or word \"both\". Try again: ")
            validationCondition3, dimension = validateFunction(dimension, "dimension")

        # Check if the combination of halfEdge + numPlots + word exists
        validationCondition7 = False
        while(not validationCondition7):
            print()
            halfEdge = input("Distance between word and edge of the square (between 0 and 1 it is assumed to be the bottom limit of the cossine similarity between the central words and all others. Must be an integer if above or equal to 1): ")

            # Validate answer - halfEdge
            validationCondition4, halfEdge = validateFunction(halfEdge, "halfEdge")
            while(not validationCondition4):
                halfEdge = input("Input value not valid. Must be a number above 0 and, if above 1, must be an integer: ")
                validationCondition4, halfEdge = validateFunction(halfEdge, "halfEdge")

            print()
            numPlots = input(f"Input the group of plots to base the data on (ex. 10 for the folder 10_plots): ")

            # Validate answer - numPlots
            numPlots = numPlots.split(",")
            if (len(numPlots) > 1):
                validationCondition5 = False
            else:
                validationCondition5, numPlots = validateFunction(numPlots, "numPlots")

            while (not validationCondition5):
                numPlots = input(f"No data present for the number of plots chosen. Try again: ")

                numPlots = numPlots.split(",")
                if (len(numPlots) > 1):
                    validationCondition5 = False
                else:
                    validationCondition5, numPlots = validateFunction(numPlots, "numPlots")

            print()
            words = input("Word at the center of the square plots: ")

            # Validate answer - word
            words = words.split(",")
            if (len(words) > 1):
                validationCondition6 = False
            else:
                validationCondition6, words = validateFunction(words, "word")

            while (not validationCondition6):
                words = input("Input word not valid. Must be one single word: ")
                words = words.split(",")
                if (len(words) > 1):
                    validationCondition6 = False
                else:
                    validationCondition6, words = validateFunction(words, "word")

            # Folder to retrieve data
            dataFolder = os.path.join("Saved Data", "Corpus 2", str(numPlots) + "_plots")

            if (os.path.exists(dataFolder)):
                if (option == "1"):
                    # Checking if data are present in the models
                    print("Checking if word is present in the models...")

                    # Load complete dataframes - only 2D dataframe based on cosine similarity because all the others are based on the same model and have the same words
                    dataListComplete2D, _ = loadData(numPlots, "cosine", 2, dataFolder)

                    for dataComplete in dataListComplete2D:
                        validationCondition7 = words in dataComplete.Word.values

                        if (not validationCondition7):
                            print("That word isn't present in the model")

                            print()
                            print("Choose other parameters")
                            break
                else:
                    # Checking if there is data already created
                    print("Checking if data for word is already created...")
                    if (halfEdge < 1):
                        validationCondition7 = (words + "_" + str(halfEdge)) in os.listdir(dataFolder)
                    else:
                        validationCondition7 = (words + "_" + str(halfEdge * 2)) in os.listdir(dataFolder)

                    if (not validationCondition7):
                        print("There isn't any data created for that word")
                        print()
                        print("Choose other parameters")
            else:
                print("There isn't any data created for that word")

        print()
        menu = False

    # 1 - Create data for square plots with a given size for a given word
    if (option == "1"):
        # Create save folder
        if (halfEdge >= 1):
            saveFolder = os.path.join(dataFolder, words + "_" + str(halfEdge * 2), "squarePlots_" + words)
        else:
            saveFolder = os.path.join(dataFolder, words + "_" + str(halfEdge), "squarePlots_" + words)

        if not os.path.exists(saveFolder):
            os.makedirs(saveFolder)
        if not os.path.exists(saveFolder):
            os.makedirs(saveFolder)

        # Create data
        SquareSpacePlotCorp2.squareDataCreator(words, halfEdge, numPlots, dataFolder, saveFolder)

        # Load data
        if (dimension == "both"):
            # Load data
            dataListComplete2D, dataListComplete3D, _, _ = loadData(numPlots, metric, dimension, dataFolder)

            dataList2D, dataList3D, limitsList2D, limitsList3D = SquareSpacePlotCorp2.loadSquareData(words, halfEdge, metric, dimension, saveFolder)

            # Analyse data
            distWords2D, prevDistance2D, wordCountList2D = SquareSpacePlotCorp2.squareDataAnalyser(words, dataList2D, dataListComplete2D)
            SquareSpacePlotCorp2.squarePlotTable(dataListComplete2D, wordCountList2D, distWords2D, prevDistance2D, saveFolder)

            distWords3D, prevDistance3D, wordCountList3D = SquareSpacePlotCorp2.squareDataAnalyser(words, dataList3D, dataListComplete3D)
            SquareSpacePlotCorp2.squarePlotTable(dataListComplete3D, wordCountList3D, distWords3D, prevDistance3D, saveFolder)

            # Plot data
            SquareSpacePlotCorp2.plotSquare2D(words, halfEdge, dataList2D, limitsList2D, False, True, saveFolder, labels)
            SquareSpacePlotCorp2.plotSquare3D(words, halfEdge, dataList3D, limitsList3D, False, True, saveFolder, labels)

        else:
            # Load data
            dataListComplete, _= loadData(numPlots, metric, dimension, dataFolder)

            dataList, limitsList = SquareSpacePlotCorp2.loadSquareData(words, halfEdge, metric, dimension, saveFolder)

            # Analyse data
            distWords, prevDistance, wordCountList = SquareSpacePlotCorp2.squareDataAnalyser(words, dataList, dataListComplete)
            SquareSpacePlotCorp2.squarePlotTable(dataListComplete, wordCountList, distWords, prevDistance, saveFolder)

            # Plot data
            if (dimension == 2):
                SquareSpacePlotCorp2.plotSquare2D(words, halfEdge, dataList, limitsList, False, True, saveFolder, labels)
            elif (dimension == 3):
                SquareSpacePlotCorp2.plotSquare3D(words, halfEdge, dataList, limitsList, False, True, saveFolder, labels)

        close = True

    # 2 - Load and visualise previously created data
    if (option == "2"):
        # Folder to retrieve data
        dataFolder = os.path.join("Saved Data", "Corpus 2", str(numPlots) + "_plots")

        # Create save folder
        if (halfEdge >= 1):
            saveFolder = os.path.join(dataFolder, words + "_" + str(halfEdge * 2), "squarePlots_" + words)
        else:
            saveFolder = os.path.join(dataFolder, words + "_" + str(halfEdge), "squarePlots_" + words)

        # Load data
        if (dimension == "both"):
            # Load data
            dataList2D, dataList3D, limitsList2D, limitsList3D = SquareSpacePlotCorp2.loadSquareData(words, halfEdge, metric, dimension, saveFolder)

            # Plot data
            SquareSpacePlotCorp2.plotSquare2D(words, halfEdge, dataList2D, limitsList2D, False, True, saveFolder, labels)
            SquareSpacePlotCorp2.plotSquare3D(words, halfEdge, dataList3D, limitsList3D, False, True, saveFolder, labels)

        else:
            dataList, limitsList = SquareSpacePlotCorp2.loadSquareData(words, halfEdge, metric, dimension, saveFolder)

            # Plot data
            if (dimension == 2):
                SquareSpacePlotCorp2.plotSquare2D(words, halfEdge, dataList, limitsList, False, True, saveFolder, labels)
            elif (dimension == 3):
                SquareSpacePlotCorp2.plotSquare3D(words, halfEdge, dataList, limitsList, False, True, saveFolder, labels)

        close = True

    # End program menu
    while (close):
        print()
        endOption = input("End program (y/n)? ")

        if (endOption == "y" or endOption == "Y"):
            run = False
            close = False

        elif (endOption == "n" or endOption == "N"):
            menu = True
            close = False
            print()
        else:
            print("Input not valid. Please try again: ")