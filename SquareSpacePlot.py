# Auxiliary script, used by SquareSpaceProcessing.py, DensityProcessing.py

# Functions in this script are responsible for:
# - Creating user-defined square plots around a chosen word for a given interval with saves at given checkpoints
# - Creating 2D and 3D dataframes for the square plots
# - Loading all the dataframes and plotting them

import pandas as pd
import matplotlib.pyplot as plt
import os
import scipy.spatial
import numpy as np
import dataframe_image as dfi

from DataCreator import loadData

# Always print to console
import functools
print = functools.partial(print, flush=True)

def furthestWord(word, data):
    # Calculates the furthest word from the central word
    # word   - central word
    # data   - data with the information about all the words
    # return - the furthest word from central word and it's distance 

    # Load dataframe into array and search for the word index inside the array
    points = data.to_numpy()
    indexWord = np.where(points == word)
    index = indexWord[0][0]

    # Array with all the points coordinates
    xyArray = np.array(list(zip(points[:, 1], points[:, 2])))
    wordPosition = np.array([[points[index, 1], points[index, 2]]], dtype = float)

    # Distance calculation
    distMat = scipy.spatial.distance_matrix(wordPosition, xyArray)

    return points[distMat.argmax(), 0], distMat[0][distMat.argmax()]

def loadSquareData(center, halfEdge, metric, dimension, saveFolder):
    # Loads the dataframes previously created by based on the metric chosen
    # center     - central word
    # halfEdge   - distance from word to side of the square
    # metric     - metric to consider when loading dataframes ("cosine" - loads dataframes created based on the cosine similarity, "dot" - loads dataframes created based on the dot product, "both" - loads all dataframes)
    # dimension  - dimension to load (2 - loads 2D dataframes, 3 - loads 3D dataframes, "both" - loads all dataframes)
    # saveFolder - folder to retrieve data from
    # return     - lists with all the chosen dataframes and their square plots limits dictionaries

    # Important lists
    if (dimension == 2 or dimension == "both"):
        dataList2D = [] # List saving 2D square dataframes for each plot
        limitsList2D = [] # List saving 2D square plots limits
        if (metric == "dot" or  metric == "both"):
            dataListDot2D = [] # Temporary list saving 2D square plots created based on the dot product
            limitsList2DDot = [] # Temporary list saving 2D square plots limits created based on the dot product

    if (dimension == 3 or dimension == "both"):
        dataList3D = [] # List saving 3D square dataframes for each plot
        limitsList3D = [] # List saving 3D square plots limits
        if (metric == "dot" or  metric == "both"):
            dataListDot3D = [] # Temporary list saving 3D square plots created based on the dot product
            limitsList3DDot = [] # Temporary list saving 3D square plots limits created based on the dot product

    print()
    print("Loading data...")
    
    # Load all data
    filesList = [file for file in os.listdir(saveFolder) if (file.split("_")[0] == "squareData2D" or file.split("_")[0] == "squareData3D")]
    filesList = sorted(filesList, key = lambda x: int(x.split(".")[0].split("_")[-1]))

    for file in filesList:
        file = file.split("_")

        if (dimension == 3 or dimension == "both"):
            # Load squareData3D
            if(file[0] == "squareData3D" and not file[1] == "dot" and (metric == "cosine" or metric == "both")):
                data = pd.read_csv(os.path.join(saveFolder, "_".join(file)))

                # Set the indexes of the dataframe to be the words
                data.set_index("Word", inplace = True, drop = True)

                # Calculate the square 3D limits
                limits = {}
                limits["limMinX"] = data.at[center, "x"] - halfEdge
                limits["limMaxX"] = data.at[center, "x"] + halfEdge
                limits["limMinY"] = data.at[center, "y"] - halfEdge
                limits["limMaxY"] = data.at[center, "y"] + halfEdge
                limits["limMinZ"] = data.at[center, "z"] - halfEdge
                limits["limMaxZ"] = data.at[center, "z"] + halfEdge

                dataList3D.append(data)
                limitsList3D.append(limits)

                print("Square 3D dataframes loaded - cosine similarity")

            # Load squareData3D_dot
            if(file[0] == "squareData3D" and file[1] == "dot" and (metric == "dot" or metric == "both")):
                data = pd.read_csv(os.path.join(saveFolder, "_".join(file)))

                # Set the indexes of the dataframe to be the words
                data.set_index("Word", inplace = True, drop = True)

                # Calculate the square 3D limits
                limits = {}
                limits["limMinXDot"] = data.at[center, "x"] - halfEdge
                limits["limMaxXDot"] = data.at[center, "x"] + halfEdge
                limits["limMinYDot"] = data.at[center, "y"] - halfEdge
                limits["limMaxYDot"] = data.at[center, "y"] + halfEdge
                limits["limMinZDot"] = data.at[center, "z"] - halfEdge
                limits["limMaxZDot"] = data.at[center, "z"] + halfEdge

                dataListDot3D.append(data)
                limitsList3DDot.append(limits)

                print("Square 3D dataframes loaded - dot product")

        if (dimension == 2 or dimension == "both"):
            # Load squareData2D
            if(file[0] == "squareData2D" and not file[1] == "dot" and (metric == "cosine" or metric == "both")):
                data = pd.read_csv(os.path.join(saveFolder, "_".join(file)))

                # Set the indexes of the dataframe to be the words
                data.set_index("Word", inplace = True, drop = True)

                # Calculate the square 2D limits
                limits = {}
                limits["limMinX"] = data.at[center, "x"] - halfEdge
                limits["limMaxX"] = data.at[center, "x"] + halfEdge
                limits["limMinY"] = data.at[center, "y"] - halfEdge
                limits["limMaxY"] = data.at[center, "y"] + halfEdge

                dataList2D.append(data)
                limitsList2D.append(limits)

                print("Square 2D dataframes loaded - cosine similarity")

            # Load squareData2D_dot
            if(file[0] == "squareData2D" and file[1] == "dot" and (metric == "dot" or metric == "both")):
                data = pd.read_csv(os.path.join(saveFolder, "_".join(file)))

                # Set the indexes of the dataframe to be the words
                data.set_index("Word", inplace = True, drop = True)

                # Calculate the square 2D limits
                limits = {}
                limits["limMinXDot"] = data.at[center, "x"] - halfEdge
                limits["limMaxXDot"] = data.at[center, "x"] + halfEdge
                limits["limMinYDot"] = data.at[center, "y"] - halfEdge
                limits["limMaxYDot"] = data.at[center, "y"] + halfEdge

                dataListDot2D.append(data)
                limitsList2DDot.append(limits)

                print("Square 2D dataframes loaded - dot product")

    # Combine lists if 3D dot product list has information
    if ((metric == "dot" or metric == "both") and (dimension == 3 or dimension == "both")):
        dataList3D = dataList3D + [-1] + dataListDot3D
        limitsList3D = limitsList3D + [-1] + limitsList3DDot

    # Combine list if 2D dot product list has information
    if ((metric == "dot" or metric == "both") and (dimension == 2 or dimension == "both")):
        dataList2D = dataList2D + [-1] + dataListDot2D
        limitsList2D = limitsList2D + [-1] + limitsList2DDot

    # Return loaded dataframes
    if (dimension == 2):
        return dataList2D, limitsList2D
    elif (dimension == 3):
        return dataList3D, limitsList3D
    else:
        return dataList2D, dataList3D, limitsList2D, limitsList3D

def plotSquare2D(center, yearList, dataList, limitsList, distWords, prevDistance, wordCountList, show = True, save = False, saveFolder = None, labels = True):
    # Creates the square 2D plots
    # center        - central word
    # yearList      - list with all the years in the interval to consider
    # dataList      - list with the square plots dataframes
    # limitsList    - list with the dictionaries with the square plots limits
    # distWords     - list with all the furthest words and their distances for each plot
    # prevDistance  - list with the distances of all previous furthest words
    # wordCountList - list with the word count for each square plot
    # show          - wether to show plots or not
    # save          - wether to save plots or not
    # saveFolder    - folder to save data
    # labels        - wether to show labels or not
    # return        - none

    # Separate cosine dataframes from dot dataframes inside dataList
    dot = False
    sqDataList = []
    sqDataListDot = []

    sqLimitsList = []
    sqLimitsListDot = []

    for count in range(len(dataList)):
        # Check if the change in metric has been made
        if (not isinstance(dataList[count], pd.DataFrame)):
            dot = True
            continue

        if (not dot):
            sqDataList.append(dataList[count])
            sqLimitsList.append(limitsList[count])
        else:
            sqDataListDot.append(dataList[count])
            sqLimitsListDot.append(limitsList[count])

    if (not dot):
        # If there isn't any data based on the dot product
        squareSide = round(limitsList[0]["limMaxX"] - limitsList[0]["limMinX"])
    elif (dot and sqDataList):
        # If there is data based on the dot product and cosine similarity
        squareSide = round(limitsList[0]["limMaxX"] - limitsList[0]["limMinX"])
    else:
        # If there isn't any data based on the cosine similarity
        squareSide = round(limitsList[1]["limMaxXDot"] - limitsList[1]["limMinXDot"])

    # Plot cosine similarity data if exits
    if (sqDataList):
        # Create global fig
        fig = plt.figure(figsize=(20,10))
        fig.suptitle(f"Metric: Cosine Similarity, Square Side: {squareSide}")

        for count, data in enumerate(sqDataList):   
            # Plot subplots
            ax = fig.add_subplot(1, len(sqDataList), count + 1)

            # Plot the word points
            ax.plot(data.x, data.y, color='crimson', marker='o', linestyle='None', markersize=5, alpha=0.40)

            # Defining Axes
            offset = -0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits
            ax.set_xlim(sqLimitsList[count]["limMinX"] - offset, sqLimitsList[count]["limMaxX"] + offset)
            ax.set_ylim(sqLimitsList[count]["limMinY"] - offset, sqLimitsList[count]["limMaxY"] + offset)
            ax.set_aspect("equal")

            # Title
            ax.set_title(f"{yearList[count]} - {yearList[count + 1]}")

            text = "Square side: " + str(squareSide)
            ax.text(0.0, -0.25, text, transform=ax.transAxes)

            text = "Number of words: " + str(wordCountList[count])
            ax.text(0.0, -0.35, text, transform=ax.transAxes)

            text = "Furthest word: " + str(distWords[count][0])
            ax.text(0.0, -0.45, text, transform=ax.transAxes)

            text = "Furthest word distance: " + "{:.1f}".format(distWords[count][1])
            ax.text(0.0, -0.55, text, transform=ax.transAxes)


            if (count != 0):
                text = "Prior furthest word dist.: " + "{:.1f}".format(prevDistance[count - 1])
                ax.text(0.0, -0.65, text, transform=ax.transAxes)

            if (labels):
                # Plot the point tags
                k = 0
                for i, j in zip(data.x, data.y):
                    corr = -0.05  # correction for annotation in marker
                    ax.annotate(data.index.values[k], xy=(i + corr, j + corr), size=10)
                    k += 1
            else:
                # Plot the central word tag
                corr = -0.05  # Correction for annotation in marker
                ax.annotate(center, xy=(data.at[center, "x"] + corr, data.at[center, "y"] + corr), size=10)

        # Save plots
        if (save):
            if (labels):
                plt.savefig(os.path.join(saveFolder, "Fig_2D_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + "_" + str(squareSide) + "_" + str(center) + ".png"))
            else:
                plt.savefig(os.path.join(saveFolder, "Fig_2D_No_Labels_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + "_" + str(squareSide) + "_" + str(center) + ".png"))

        if (show):
            plt.show()

    # Plot dot product data if exits
    if (sqDataListDot):
        # Create global fig
        fig = plt.figure(figsize=(20,10))
        fig.suptitle(f"Metric: Dot Product, Square Side: {squareSide}")

        # Rearrange information list to only have dot product data
        index = wordCountList.index(-1)

        distWords = distWords[index + 1:]
        wordCountList = wordCountList[index + 1:]

        if (index == 0):
            prevDistance = prevDistance[index + 1:]
        else:
            prevDistance = prevDistance[index:]

        for count, data in enumerate(sqDataListDot):
            # Plot subplots
            ax = fig.add_subplot(1, len(sqDataListDot), count + 1)

            # Plot the word points
            ax.plot(data.x, data.y, color='crimson', marker='o', linestyle='None', markersize=5, alpha=0.40)

            # Defining Axes
            offset = -0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits
            ax.set_xlim(sqLimitsListDot[count]["limMinXDot"] - offset, sqLimitsListDot[count]["limMaxXDot"] + offset)
            ax.set_ylim(sqLimitsListDot[count]["limMinYDot"] - offset, sqLimitsListDot[count]["limMaxYDot"] + offset)
            ax.set_aspect("equal")

            # Title
            ax.set_title(f"{yearList[count]} - {yearList[count + 1]}")

            text = "Square side: " + str(squareSide)
            ax.text(0.0, -0.25, text, transform=ax.transAxes)

            text = "Number of words: " + str(wordCountList[count])
            ax.text(0.0, -0.35, text, transform=ax.transAxes)

            text = "Furthest word: " + str(distWords[count][0])
            ax.text(0.0, -0.45, text, transform=ax.transAxes)

            text = "Furthest word distance: " + "{:.1f}".format(distWords[count][1])
            ax.text(0.0, -0.55, text, transform=ax.transAxes)

            if (count != 0):
                text = "Prior furthest word dist.: " + "{:.1f}".format(prevDistance[count - 1])
                ax.text(0.0, -0.65, text, transform=ax.transAxes)

            if (labels):
                # Plot the point tags
                k = 0
                for i, j in zip(data.x, data.y):
                    corr = -0.05  # correction for annotation in marker
                    ax.annotate(data.index.values[k], xy=(i + corr, j + corr), size=10)
                    k += 1
            else:
                # Plot the central word tag
                corr = -0.05  # Correction for annotation in marker
                ax.annotate(center, xy=(data.at[center, "x"] + corr, data.at[center, "y"] + corr), size=10)

        # Save plots
        if (save):
            if (labels):
                plt.savefig(os.path.join(saveFolder, "Fig_Dot_2D_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + "_" + str(squareSide) + "_" + str(center) + ".png"))
            else:
                plt.savefig(os.path.join(saveFolder, "Fig_Dot_2D_No_Labels_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + "_" + str(squareSide) + "_" + str(center) + ".png"))

        if (show):
            plt.show()

    return None

def plotSquare3D(center, yearList, dataList, limitsList, distWords, prevDistance, wordCountList, show = True, save = False, saveFolder = None, labels = True):
    # Creates the square 3D plots
    # center        - central word
    # yearList      - list with all the years in the interval to consider
    # dataList      - list with the square plots dataframes
    # limitsList    - list with the dictionaries with the square plots limits
    # distWords     - list with all the furthest words and their distances for each plot
    # prevDistance  - list with the distances of all previous furthest words
    # wordCountList - list with the word count for each square plot
    # show          - wether to show plots or not
    # save          - wether to save plots or not
    # saveFolder    - folder to save data
    # labels        - wether to show labels or not
    # return        - none

    # Separate cosine dataframes from dot dataframes inside dataList
    dot = False
    sqDataList = []
    sqDataListDot = []

    sqLimitsList = []
    sqLimitsListDot = []

    for count in range(len(dataList)):
        # Check if the change in metric has been made
        if (not isinstance(dataList[count], pd.DataFrame)):
            dot = True
            continue

        if (not dot):
            sqDataList.append(dataList[count])
            sqLimitsList.append(limitsList[count])
        else:
            sqDataListDot.append(dataList[count])
            sqLimitsListDot.append(limitsList[count])

    if (not dot):
        # If there isn't any data based on the dot product
        squareSide = round(limitsList[0]["limMaxX"] - limitsList[0]["limMinX"])
    elif (dot and sqDataList):
        # If there is data based on the dot product and cosine similarity
        squareSide = round(limitsList[0]["limMaxX"] - limitsList[0]["limMinX"])
    else:
        # If there isn't any data based on the cosine similarity
        squareSide = round(limitsList[1]["limMaxXDot"] - limitsList[1]["limMinXDot"])

    # Plot cosine similarity data if exits
    if (sqDataList):
        # Create global fig
        fig = plt.figure(figsize=(20,10))
        fig.suptitle(f"Metric: Cosine Similarity, Cube Side: {squareSide}")

        for count, data in enumerate(sqDataList):
            # Plot subplots
            ax = fig.add_subplot(1, len(sqDataList), count + 1, projection='3d')

            # Plot the word points
            ax.plot(data.x, data.y, data.z, color='crimson', marker='o', linestyle='None', markersize=5, alpha=0.40)

            # Defining Axes
            offset = -0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits
            ax.set_xlim(sqLimitsList[count]["limMinX"] - offset, sqLimitsList[count]["limMaxX"] + offset)
            ax.set_ylim(sqLimitsList[count]["limMinY"] - offset, sqLimitsList[count]["limMaxY"] + offset)
            ax.set_zlim(sqLimitsList[count]["limMinZ"] - offset, sqLimitsList[count]["limMaxZ"] + offset)

            # Title
            ax.set_title(f"{yearList[count]} - {yearList[count + 1]}")

            text = "Square side: " + str(squareSide)
            ax.text2D(0.0, -0.25, text, transform=ax.transAxes)

            text = "Number of words: " + str(wordCountList[count])
            ax.text2D(0.0, -0.35, text, transform=ax.transAxes)

            text = "Furthest word: " + str(distWords[count][0])
            ax.text2D(0.0, -0.45, text, transform=ax.transAxes)

            text = "Furthest word distance: " + "{:.1f}".format(distWords[count][1])
            ax.text2D(0.0, -0.55, text, transform=ax.transAxes)


            if (count != 0):
                text = "Prior furthest word dist.: " + "{:.1f}".format(prevDistance[count - 1])
                ax.text2D(0.0, -0.65, text, transform=ax.transAxes)

            if (labels):
                # Plot the point tags
                k = 0
                for i, j, l in zip(data.x, data.y, data.z):
                    corr = -0.05  # correction for annotation in marker
                    ax.text(i + corr, j + corr, l + corr, data.index.values[k], size=10)
                    k += 1
            else:
                # Plot the central word tag
                corr = -0.05  # Correction for annotation in marker
                ax.text(data.at[center, "x"] + corr, data.at[center, "y"] + corr, data.at[center, "z"] + corr, center, size=10)

        # Save plots
        if (save):
            if (labels):
                plt.savefig(os.path.join(saveFolder, "Fig_3D_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + "_" + str(squareSide) + "_" + str(center) + ".png"))
            else:
                plt.savefig(os.path.join(saveFolder, "Fig_3D_No_Labels_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + "_" + str(squareSide) + "_" + str(center) + ".png"))

        if (show):
            plt.show()

    # Plot dot product data if exits
    if (sqDataListDot):
        # Create global fig
        fig = plt.figure(figsize=(20,10))
        fig.suptitle(f"Metric: Dot Product, Cube Side: {squareSide}")

        # Rearrange information list to only have dot product data
        index = wordCountList.index(-1)

        distWords = distWords[index + 1:]
        wordCountList = wordCountList[index + 1:]

        if (index == 0):
            prevDistance = prevDistance[index + 1:]
        else:
            prevDistance = prevDistance[index:]

        for count, data in enumerate(sqDataListDot):
            # Plot subplots
            ax = fig.add_subplot(1, len(sqDataListDot), count + 1, projection='3d')

            # Plot the word points
            ax.plot(data.x, data.y, data.z, color='crimson', marker='o', linestyle='None', markersize=5, alpha=0.40)

            # Defining Axes
            offset = -0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits
            ax.set_xlim(sqLimitsListDot[count]["limMinXDot"] - offset, sqLimitsListDot[count]["limMaxXDot"] + offset)
            ax.set_ylim(sqLimitsListDot[count]["limMinYDot"] - offset, sqLimitsListDot[count]["limMaxYDot"] + offset)
            ax.set_zlim(sqLimitsListDot[count]["limMinZDot"] - offset, sqLimitsListDot[count]["limMaxZDot"] + offset)

            # Title
            ax.set_title(f"{yearList[count]} - {yearList[count + 1]}")

            text = "Square side: " + str(squareSide)
            ax.text2D(0.0, -0.25, text, transform=ax.transAxes)

            text = "Number of words: " + str(wordCountList[count])
            ax.text2D(0.0, -0.35, text, transform=ax.transAxes)

            text = "Furthest word: " + str(distWords[count][0])
            ax.text2D(0.0, -0.45, text, transform=ax.transAxes)

            text = "Furthest word distance: " + "{:.1f}".format(distWords[count][1])
            ax.text2D(0.0, -0.55, text, transform=ax.transAxes)

            if (count != 0):
                text = "Prior furthest word dist.: " + "{:.1f}".format(prevDistance[count - 1])
                ax.text2D(0.0, -0.65, text, transform=ax.transAxes)

            if (labels):
                # Plot the point tags
                k = 0
                for i, j, l in zip(data.x, data.y, data.z):
                    corr = -0.05  # correction for annotation in marker
                    ax.text(i + corr, j + corr, l + corr, data.index.values[k], size=10)
                    k += 1
            else:
                # Plot the central word tag
                corr = -0.05  # Correction for annotation in marker
                ax.text(data.at[center, "x"] + corr, data.at[center, "y"] + corr, data.at[center, "z"] + corr, center, size=10)

        # Save plots
        if (save):
            if (labels):
                plt.savefig(os.path.join(saveFolder, "Fig_Dot_3D_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + "_" + str(squareSide) + "_" + str(center) + ".png"))
            else:
                plt.savefig(os.path.join(saveFolder, "Fig_Dot_3D_No_Labels_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + "_" + str(squareSide) + "_" + str(center) + ".png"))

        if (show):
            plt.show()

    return None

def squareDataAnalyser(center, dataList, dataListComplete):
    # Analyses the square plots data for each plot in terms of the furthest word from central word and its distance, the previous furthest word and its new distance and the word count inside each plot
    # center           - central word
    # dataList         - list with all the square plots dataframes
    # dataListComplete - list with all the complete dataframes with all the words in the model
    # return           - lists with all the furthest words and their distances, previous furthest words and their new distances and word count of each square dataframe

    # Important lists
    distWords = [] # List with all the furthest words and their distances
    prevDistance = [] # List with the new distances of all the previous furthest words
    wordCount = []

    for count, dataComplete in enumerate(dataListComplete):

        if (isinstance(dataComplete, pd.DataFrame)):
            # Calculate furthest word and save it
            furtWord, distance = furthestWord(center, dataComplete)
            distWords.append([furtWord, distance])

            # Check it's the first iteration, if not calculate the distance to the previous furthest word
            # Check if the change in the metric has happened
            if (count != 0 and distWords[count - 1] != -1):
                previous = wordDistance(dataComplete, center, distWords[count - 1][0])
                prevDistance.append(previous)

            # Save word count
            wordCount.append(len(dataList[count].index))
        else:
            distWords.append(-1)
            prevDistance.append(-1)
            wordCount.append(-1)

    return distWords, prevDistance, wordCount

def squareDataCreator(center, halfEdge, yearList, dataFolder, saveFolder):
    # Creates user-defined square plots centered in a given word for a given interval with saves at given checkpoints. The calculations are based on the cosine similarity and dot product
    # center     - central word
    # halfEdge   - distance from word to side of the square
    # yearList   - list with all the years in the interval to consider
    # dataFolder - folder to retrieve data from
    # saveFolder - folder to save data
    # return     - None

    # Load data
    _, dataListComplete2D, dataListComplete3D, _, _ = loadData(yearList[0], yearList[-1], yearList[1] - yearList[0], "both", "both", dataFolder)

    # Variable for controlling the change in dataframes based on the cosine similarity to the dataframes based on the dot product
    dot = False

    # Variable for indexes of list that are the same for cosine similarity and dot product data
    repIndex = 0

    # Square Plots - 2D
    for data in dataListComplete2D:

        # Check if the dataframes changed in metric
        if (not isinstance(data, pd.DataFrame)):
            dot = True
            repIndex = 0
            continue

        # Set the indexes of the dataframe to be the words
        data.set_index("Word", inplace = True, drop = True)

        # Calculate the 2D square plots limits
        limMinX = data.at[center, "x"] - halfEdge
        limMaxX = data.at[center, "x"] + halfEdge
        limMinY = data.at[center, "y"] - halfEdge
        limMaxY = data.at[center, "y"] + halfEdge

        # Create the square plot dataframe
        squareData = data[(limMinX <= data["x"]) & (data["x"] <= limMaxX) & (limMinY <= data["y"]) & (data["y"] <= limMaxY)]

        # Cosine similarity
        if (not dot):
            # Save data
            squareData.to_csv(os.path.join(saveFolder, "squareData2D_" + str(repIndex + 1) + ".csv"))
        else:
            # Dot product

            # Save data
            squareData.to_csv(os.path.join(saveFolder, "squareData2D_dot_" + str(repIndex + 1) + ".csv"))

        repIndex += 1

    # Variable for controlling the change in dataframes based on the cosine similarity to the dataframes based on the dot product
    dot = False

    # Variable for indexes of list that are the same for cosine similarity and dot product data
    repIndex = 0

    # Square Plots - 3D
    for data in dataListComplete3D:

        # Check if the dataframes changed in metric
        if (not isinstance(data, pd.DataFrame)):
            dot = True
            repIndex = 0
            continue

        # Set the indexes of the dataframe to be the words
        data.set_index("Word", inplace = True, drop = True)

        # Calculate the 3D square plots limits
        limMinX = data.at[center, "x"] - halfEdge
        limMaxX = data.at[center, "x"] + halfEdge
        limMinY = data.at[center, "y"] - halfEdge
        limMaxY = data.at[center, "y"] + halfEdge
        limMinZ = data.at[center, "z"] - halfEdge
        limMaxZ = data.at[center, "z"] + halfEdge

        # Create the square plots dataframe
        squareData = data[(limMinX <= data["x"]) & (data["x"] <= limMaxX) & (limMinY <= data["y"]) & (data["y"] <= limMaxY) & (limMinZ <= data["z"]) & (data["z"] <= limMaxZ)]

        # Cosine similarity
        if (not dot):
            # Save data
            squareData.to_csv(os.path.join(saveFolder, "squareData3D_" + str(repIndex + 1) + ".csv"))
        else:
            # Dot product

            # Save data
            squareData.to_csv(os.path.join(saveFolder, "squareData3D_dot_" + str(repIndex + 1) + ".csv"))

        repIndex += 1

    return None

def squarePlotTable(yearList, dataListComplete, wordCountList, distWords, previousDistance, saveFolder):
    # Creates a table with information about the number of words in the entire model, the word count inside each square plot, the furthest words and their distance and distance of prior furthest words
    # yearList         - list with all the years in the interval to consider
    # dataListComplete - list with the dataframes with all the words in the model for each plot
    # wordCountList    - list with the count of words for each plot
    # distWords        - list with the furthest words for each plot
    # previousDistance - list with the new distance of the prior furthest word
    # saveFolder       - folder where data is stored
    # return           - none

    # Table configurations
    dfIndexes = ["Total number of words", "Number of words:", "Furthest word", 
             "Furthest word distance", "Prior furthest word dist."]
    columnsNames = []
    dfData = []

    # Separate cosine dataframes from dot dataframes inside dataListComplete
    dot = False
    dataListComp = []
    dataListCompDot = []

    for count in range(len(dataListComplete)):
        # Check if the change in metric has been made
        if (not isinstance(dataListComplete[count], pd.DataFrame)):
            dot = True
            continue

        if (not dot):
            dataListComp.append(dataListComplete[count])
        else:
            dataListCompDot.append(dataListComplete[count])

    # Table for cosine similarity data if exits
    if(dataListComp):
        for index in range(len(dataListComp)):
            # Column name
            column = f"{yearList[index]} - {yearList[index + 1]}"
            columnsNames.append(column)

            data = []
            # Total number of words
            data.append(len(dataListComp[index].index))

            # Number of words inside square
            data.append(wordCountList[index])
            
            # Furthest word
            data.append(distWords[index][0])

            # Furthest word distance
            data.append(round(distWords[index][1], 1))

            # Prior furthest word distance
            if (index == 0):
                data.append("-")
            else:
                data.append(round(previousDistance[index - 1], 1))

            dfData.append(data)

        # Transpose list
        transposeList = np.array(dfData)
        transposeList = transposeList.T
        dfData = transposeList.tolist()

        # Create general dataframe
        generalDf = pd.DataFrame(data = dfData,
                                 columns = columnsNames,
                                 index = dfIndexes)

        # Check for dimension
        if (not "z" in dataListComp[0].columns):
            # Save table as an image
            dfi.export(generalDf, os.path.join(saveFolder, "Table_2D_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + ".png"))

            # Save table as a csv file
            generalDf.to_csv(os.path.join(saveFolder, "generalDf2D" + ".csv"))
        else:
            # Save table as an image
            dfi.export(generalDf, os.path.join(saveFolder, "Table_3D_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + ".png"))

            # Save table as a csv file
            generalDf.to_csv(os.path.join(saveFolder, "generalDf3D" + ".csv"))

    # Table for dot product data if exits
    columnsNames = []
    dfData = []

    if(dataListCompDot):
        # Rearrange information list to only have dot product data
        index = wordCountList.index(-1)

        distWords = distWords[index + 1:]
        wordCountList = wordCountList[index + 1:]

        if (index == 0):
            previousDistance = previousDistance[index + 1:]
        else:
            previousDistance = previousDistance[index:]

        for index in range(len(dataListCompDot)):
            # Column name
            column = f"{yearList[index]} - {yearList[index + 1]}"
            columnsNames.append(column)

            data = []
            # Total number of words
            data.append(len(dataListCompDot[index].index))

            # Number of words inside square
            data.append(wordCountList[index])
            
            # Furthest word
            data.append(distWords[index][0])

            # Furthest word distance
            data.append(round(distWords[index][1], 1))

            # Prior furthest word distance
            if (index == 0):
                data.append("-")
            else:
                data.append(round(previousDistance[index - 1], 1))

            dfData.append(data)

        # Transpose list
        transposeList = np.array(dfData)
        transposeList = transposeList.T
        dfData = transposeList.tolist()

        # Create general dataframe
        generalDf = pd.DataFrame(data = dfData,
                                 columns = columnsNames,
                                 index = dfIndexes)

        # Check for dimension
        if (not "z" in dataListCompDot[0].columns):
            # Save table as an image
            dfi.export(generalDf, os.path.join(saveFolder, "Table_Dot_2D_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + ".png"))

            # Save table as a csv file
            generalDf.to_csv(os.path.join(saveFolder, "generalDf2D_dot" + ".csv"))
        else:
            # Save table as an image
            dfi.export(generalDf, os.path.join(saveFolder, "Table_Dot_3D_" + str(yearList[0]) + "_" + str(yearList[-1]) + "_" + str(yearList[1] - yearList[0]) + ".png"))

            # Save table as a csv file
            generalDf.to_csv(os.path.join(saveFolder, "generalDf3D_dot" + ".csv"))

    return None

def wordDistance(data, word1, word2):
    # Calculates the euclidean distance between two words
    # data   - data with the information about all the words
    # word1  - first word for the calculation
    # word2  - second word for the calculation
    # return - euclidean distance between two words

    # Load dataframe into array and search for the word1 index inside the array
    points = data.to_numpy()
    indexWord1 = np.where(points == word1)
    index1 = indexWord1[0][0]

    # Search for the word2 index inside the array
    indexWord2 = np.where(points == word2)
    index2 = indexWord2[0][0]

    # Word position values
    word1Position = np.array([[points[index1, 1], points[index1, 2]]], dtype = float)
    word2Position = np.array([[points[index2, 1], points[index2, 2]]], dtype = float)

    # Distance calculation
    distMat = scipy.spatial.distance_matrix(word1Position, word2Position)

    return distMat[0][0]