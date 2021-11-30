# Menu script to facilitate the creation of square plots centered in a given word

# Possible Actions:
# - Create dataframes for square plots centered in a given word with a given size (bulk creation available) and plot them
# - Load all the created dataframes and plot them

import os

import SquareSpacePlot
from DataCreator import loadData

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
    # type     - type of validation to be made, "option", "metric", "dimension", "interval", "word" or "halfEdge"
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
        if (choice.isnumeric()):
            choice = int(choice)

            validationCondition = choice > 0
            return validationCondition, choice

    # Verifies input for the interval
    if (type == "interval"):
        for count, yearInt in enumerate(choice):
            yearInt = yearInt.split("-")

            validationCondition = all(x.isnumeric() for x in yearInt)

            if (not validationCondition):
                return False, -1
            else:
                yearInt = "_".join(yearInt)
                choice[count] = yearInt
                validationCondition = yearInt in os.listdir("Saved Data")

                if (not validationCondition):
                    print(f"No data present for the interval {yearInt}")
                    return False, -1

        return True, choice

    # Verifies input for the word
    if (type == "word"):
        validationCondition = any(x.isnumeric() for x in choice)

        return not validationCondition, choice

    return False, -1

# Loop controling variables
run = True
menu = True

# Menu Loop
while (run):

    # User menu
    if (menu):
        print("What would you like to do?")
        print("1 - Create data for square plots with a given size for a given interval and a given word (bulk creation available)")
        print("2 - Load and visualise previously created data")

        print()
        print("Warning:")
        print("- Creation actions (either singular or bulk) will not show the plots but will save them in the correct folders")
        print("- Never add empty space before or after commas or \"-\"")

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

        menu = False

    # 1 - Create data for square plots with a given size for a given interval and a given word
    if (option == "1"):
        print()
        halfEdge = input("Distance between word and edge of the square (bulk actions not available for this parameter): ")

        # Validate answer - halfEdge
        validationCondition4, halfEdge = validateFunction(halfEdge, "halfEdge")
        while(not validationCondition4):
            halfEdge = input("Input value not valid. Must be a number above 0: ")
            validationCondition4, halfEdge = validateFunction(halfEdge, "halfEdge")

        print()
        interval = input(f"Input an interval in the form ####-####-# (beginning year-end year-checkpoints, an interval of the type ####-####-# followed by a comma and another interval, ex. 2000-2008-4,2010-2020-2, will perform the action in bulk over the multiple intervals): ")

        # Validate answer - interval
        interval = interval.split(",")
        validationCondition5, interval = validateFunction(interval, "interval")

        while (not validationCondition5):
            interval = input(f"Input is not valid or there isn't any data created with the chosen years. Must be of the form ####-####-# or ####-####-#,####-####-# with no space before or after commas or \"-\". Try again: ")
            interval = interval.split(",")
            validationCondition5, interval = validateFunction(interval, "interval")

        print()
        words = input("Word at the center of the squared plots (a list of words separeted by commas will perform the action in bulk over the multiple words): ")

        # Validate answer - word
        validationCondition7 = False
        while (not validationCondition7):
            words = words.split(",")
            validationCondition6, _ = validateFunction(words, "word")

            while (not validationCondition6):
                words = input("Input word or words not valid. Must be a word or list of words separated by commas: ")
                words = words.split(",")
                validationCondition6, _ = validateFunction(words, "word")

            # Checking if words are present in the models
            print("Checking if words are present in the models...")
            invalidWords = []

            for wrd in words:
                for intv in interval:
                    # Folder to retrieve data
                    dataFolder = os.path.join("Saved Data", intv)

                    # Load complete dataframes - only 2D dataframe based on cosine similarity because all the others are based on the same model and have the same words
                    yearList, dataListComplete2D, _ = loadData(int(intv.split("_")[0]), int(intv.split("_")[1]), int(intv.split("_")[2]), "cosine", 2, dataFolder)

                    for dataComplete in dataListComplete2D:
                        validationCondition7 = wrd in dataComplete.Word.values

                        if (not validationCondition7):
                            invalidWords.append([wrd, intv])
                            break

            if (invalidWords):
                validationCondition7 = False
                print("Some words aren't present in the models chosen: ")

                # Print problem words
                for words in invalidWords:
                    print(words[0], "not present in interval", words[1])

                print()
                words = input("Choose other words: ")

        for wrd in words:
            for intv in interval:
                # Folder to retrieve data
                dataFolder = os.path.join("Saved Data", intv)

                # Create year list for data
                yearList = [*range(int(intv.split("_")[0]), int(intv.split("_")[1]), int(intv.split("_")[2]))]

                # If last year on the list is not == end then add that year
                if (yearList[-1] != int(intv.split("_")[1])):
                    yearList.append(int(intv.split("_")[1]))

                # Create save folders
                saveFolder = os.path.join(dataFolder, wrd + "_" + str(halfEdge * 2), "squarePlots_" + str(wrd))

                if not os.path.exists(saveFolder):
                    os.makedirs(saveFolder)

                # Create data
                SquareSpacePlot.squareDataCreator(wrd, halfEdge, yearList, dataFolder, saveFolder)

                # Load data
                if (dimension == "both"):
                    # Load data
                    _, dataListComplete2D, dataListComplete3D, _, _ = loadData(yearList[0], yearList[-1], yearList[1] - yearList[0], metric, dimension, dataFolder)

                    dataList2D, dataList3D, limitsList2D, limitsList3D = SquareSpacePlot.loadSquareData(wrd, halfEdge, metric, dimension, saveFolder)

                    # Analyse data
                    distWords2D, prevDistance2D, wordCountList2D = SquareSpacePlot.squareDataAnalyser(wrd, dataList2D, dataListComplete2D)
                    SquareSpacePlot.squarePlotTable(yearList, dataListComplete2D, wordCountList2D, distWords2D, prevDistance2D, saveFolder)

                    distWords3D, prevDistance3D, wordCountList3D = SquareSpacePlot.squareDataAnalyser(wrd, dataList3D, dataListComplete3D)
                    SquareSpacePlot.squarePlotTable(yearList, dataListComplete3D, wordCountList3D, distWords3D, prevDistance3D, saveFolder)

                    # Plot data
                    SquareSpacePlot.plotSquare2D(wrd, yearList, dataList2D, limitsList2D, distWords2D, prevDistance2D, wordCountList2D, False, True, saveFolder, labels)
                    SquareSpacePlot.plotSquare3D(wrd, yearList, dataList3D, limitsList3D, distWords3D, prevDistance3D, wordCountList3D, False, True, saveFolder, labels)

                else:
                    # Load data
                    _, dataListComplete, _= loadData(yearList[0], yearList[-1], yearList[1] - yearList[0], metric, dimension, dataFolder)

                    dataList, limitsList = SquareSpacePlot.loadSquareData(wrd, halfEdge, metric, dimension, saveFolder)

                    # Analyse data
                    distWords, prevDistance, wordCountList = SquareSpacePlot.squareDataAnalyser(wrd, dataList, dataListComplete)
                    SquareSpacePlot.squarePlotTable(yearList, dataListComplete, wordCountList, distWords, prevDistance, saveFolder)

                    # Plot data
                    if (dimension == 2):
                        SquareSpacePlot.plotSquare2D(wrd, yearList, dataList, limitsList, distWords, prevDistance, wordCountList, False, True, saveFolder, labels)
                    elif (dimension == 3):
                        SquareSpacePlot.plotSquare3D(wrd, yearList, dataList, limitsList, distWords, prevDistance, wordCountList, False, True, saveFolder, labels)

        close = True

    # 2 - Load and visualise previously created data
    if (option == "2"):
        validationCondition7 = False
        while (not validationCondition7):
            print()
            halfEdge = input("Distance between word and edge of the square (bulk actions not available for this parameter): ")

            # Validate answer - halfEdge
            validationCondition4, halfEdge = validateFunction(halfEdge, "halfEdge")
            while(not validationCondition4):
                halfEdge = input("Input value not valid. Must be a number above 0: ")
                validationCondition4, halfEdge = validateFunction(halfEdge, "halfEdge")

            print()
            interval = input(f"Input an interval in the form ####-####-# (beginning year-end year-checkpoints): ")

            # Validate answer - interval (extra steps - no bulk action available)
            interval = interval.split(",")
            if (len(interval) > 1):
                validationCondition5 = False
            else:
                validationCondition5, interval = validateFunction(interval, "interval")

            while (not validationCondition5):
                interval = input(f"Input is not valid or there isn't any data created with the chosen years. Must be of the form ####-####-#. Try again: ")
                interval = interval.split(",")
                if (len(interval) > 1):
                    validationCondition5 = False
                else:
                    validationCondition5, interval = validateFunction(interval, "interval")

            print()
            words = input("Word at the center of the squared plots: ")

            # Validate answer - word (extra steps - no bulk action available)
            words = words.split(",")
            if (len(words) > 1):
                validationCondition6 = False
            else:
                validationCondition6, _ = validateFunction(words, "word")

            while (not validationCondition6):
                words = input("Input word not valid. Must be one single word: ")
                words = words.split(",")
                if (len(words) > 1):
                    validationCondition6 = False
                else:
                    validationCondition6, _ = validateFunction(words, "word")

            # Checking if words are present in the models
            print("Checking if data already exists...")

            foldersList = os.listdir(os.path.join("Saved Data", interval[0]))
            dataFolder = ""
            for folder in foldersList:
                wrd = folder.split("_")[0]
                hfEdge = int(folder.split("_")[1])
                if (words[0] == wrd and (halfEdge * 2) == hfEdge):
                    # Folder to retrieve data
                    dataFolder = os.path.join("Saved Data", interval[0])

            if (not dataFolder):
                print("No data for the chosen parameters")
            else:
                validationCondition7 = True

        # Create save folders
        saveFolder = os.path.join(dataFolder, words[0] + "_" + str(halfEdge * 2), "squarePlots_" + str(words[0]))

        # Create year list for data
        yearList = [*range(int(interval[0].split("_")[0]), int(interval[0].split("_")[1]), int(interval[0].split("_")[2]))]

        # If last year on the list is not == end then add that year
        if (yearList[-1] != int(interval[0].split("_")[1])):
            yearList.append(int(interval[0].split("_")[1]))

        # Load data
        if (dimension == "both"):
            # Load data
            _, dataListComplete2D, dataListComplete3D, _, _ = loadData(int(interval[0].split("_")[0]), int(interval[0].split("_")[1]), int(interval[0].split("_")[2]), metric, dimension, dataFolder)

            dataList2D, dataList3D, limitsList2D, limitsList3D = SquareSpacePlot.loadSquareData(words[0], halfEdge, metric, dimension, saveFolder)

            # Analyse data
            distWords2D, prevDistance2D, wordCountList2D = SquareSpacePlot.squareDataAnalyser(words[0], dataList2D, dataListComplete2D)
            distWords3D, prevDistance3D, wordCountList3D = SquareSpacePlot.squareDataAnalyser(words[0], dataList3D, dataListComplete3D)

            # Plot data
            SquareSpacePlot.plotSquare2D(words[0], yearList, dataList2D, limitsList2D, distWords2D, prevDistance2D, wordCountList2D, True, False, None, labels)
            SquareSpacePlot.plotSquare3D(words[0], yearList, dataList3D, limitsList3D, distWords3D, prevDistance3D, wordCountList3D, True, False, None, labels)

        else:
            # Load data
            _, dataListComplete, _= loadData(int(interval[0].split("_")[0]), int(interval[0].split("_")[1]), int(interval[0].split("_")[2]), metric, dimension, dataFolder)

            dataList, limitsList = SquareSpacePlot.loadSquareData(words[0], halfEdge, metric, dimension, saveFolder)

            # Analyse data
            distWords, prevDistance, wordCountList = SquareSpacePlot.squareDataAnalyser(words[0], dataList, dataListComplete)

            # Plot data
            if (dimension == 2):
                SquareSpacePlot.plotSquare2D(words[0], yearList, dataList, limitsList, distWords, prevDistance, wordCountList, True, False, None, labels)
            elif (dimension == 3):
                SquareSpacePlot.plotSquare3D(words[0], yearList, dataList, limitsList, distWords, prevDistance, wordCountList, True, False, None, labels)

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