# Auxiliary script, used by DataCreatorProcessing.py, SquareSpacePlot.py, SquarePlotProcessing.py and DensityProcessing.py

# Functions in this script are responsible for:
# - Creating models in a given interval and saving them at given checkpoints
# - Creating 2D and 3D dataframes from the models with the entire vocabulary
# - Loading all the dataframes and plotting them

import os
import matplotlib.pyplot as plt
import pandas as pd
import gensim.models.word2vec as w2v

import ModelTraining
import DimensionReduction
import WordSpacePlot
import CorpusCombinator

# Always print to console
import functools
print = functools.partial(print, flush=True)

# Create save general folder
if not os.path.exists("Saved Data"):
    os.makedirs("Saved Data")

def dataCreator(beg, end, checkP, saveFolder):
    # Creates and trains a model for a given year interval, saving the model state in a dataframe at user-defined checkpoints. The calculations are based on the cosine similarity and dot product
    # beg        - first year of the year interval
    # end        - last year of the year interval
    # checkP     - value for the number of years to pass before a checkpoint is reached and the model is saved
    # saveFolder - folder to save data
    # return     - none

    # Create year list
    yearList = [*range(beg, end + 1, checkP)]

    # If last year on the list is not == end then add that year
    if (yearList[-1] != end):
        yearList.append(end)

    print()
    print(f"Creating data - {beg} to {end} in steps of {checkP}")

    # Create and train the model
    for index in range(len(yearList) - 1):
        # Name of the save folder
        saveFolderName = os.path.join(saveFolder, "Checkpoint_" + str(index + 1))

        # Load the corpus path to be used
        corpusPath = CorpusCombinator.corpusCombinatorMain(yearList[index], yearList[index + 1], saveFolderName)

        # Name of the model
        modelName = "Model_" + str(beg) + "_" + str(end) + "_" + str(index + 1)

        # Check if trained model already exists
        if (os.path.exists(os.path.join(saveFolderName, modelName + ".w2v"))):
            model = w2v.Word2Vec.load(os.path.join(saveFolderName, modelName + ".w2v"))
        else:
            # If no model exists, create one

            # Check if it is the first pass, if yes then create the model
            if (yearList[index] == beg):
                # Create Model
                model = ModelTraining.createModel(corpusPath, saveFolderName, modelName)

            else:
                # Load the previous model and train it again
                model = ModelTraining.createModel(corpusPath, saveFolderName, modelName, model)

        print()
        print(f"Model for {yearList[index]} - {yearList[index + 1]} created")
        print()

        if (not os.path.exists(os.path.join(saveFolderName, "dataframeComplete3D_" + str(index + 1) + ".csv"))):
            # Reduce the dimension and produce a 3D dataframe - calculations cosine similarity
            matrix = DimensionReduction.reduceDimension(model, saveFolderName, 3, "cosine")
            dataframe3D = WordSpacePlot.createDataframe(model, matrix, 3)
            dataframe3D.to_csv(os.path.join(saveFolderName, "dataframeComplete3D_" + str(index + 1) + ".csv"), index = False)
            print("Global 3D dataframes created - cosine similarity")

        if (not os.path.exists(os.path.join(saveFolderName, "dataframeComplete2D_" + str(index + 1) + ".csv"))):
            # Reduce the dimension and produce a 2D dataframe - calculations cosine similarity
            matrix = DimensionReduction.reduceDimension(model, saveFolderName, 2, "cosine")
            dataframe2D = WordSpacePlot.createDataframe(model, matrix, 2)
            dataframe2D.to_csv(os.path.join(saveFolderName, "dataframeComplete2D_" + str(index + 1) + ".csv"), index = False)
            print("Global 2D dataframes created - cosine similarity")

        if (not os.path.exists(os.path.join(saveFolderName, "dataframeComplete3D_dot_" + str(index + 1) + ".csv"))):
            # Reduce the dimension and produce a 3D dataframe - calculations dot product
            matrix = DimensionReduction.reduceDimension(model, saveFolderName, 3, "dotProduct")
            dataframe3D_dot = WordSpacePlot.createDataframe(model, matrix, 3)
            dataframe3D_dot.to_csv(os.path.join(saveFolderName, "dataframeComplete3D_dot_" + str(index + 1) + ".csv"), index = False)
            print("Global 3D dataframes created - dot product")

        if (not os.path.exists(os.path.join(saveFolderName, "dataframeComplete2D_dot_" + str(index + 1) + ".csv"))):
            # Reduce the dimension and produce a 2D dataframe - calculations dot product
            matrix = DimensionReduction.reduceDimension(model, saveFolderName, 2, "dotProduct")
            dataframe2D_dot = WordSpacePlot.createDataframe(model, matrix, 2)
            dataframe2D_dot.to_csv(os.path.join(saveFolderName, "dataframeComplete2D_dot_" + str(index + 1) + ".csv"), index = False)
            print("Global 2D dataframes created - dot product")

    return None

def loadData(beg, end, checkP, metric, dimension, saveFolder):
    # Loads the dataframes previously created by dataCreator based on the metric chosen and dimension
    # beg        - first year of the year interval
    # end        - last year of the year interval
    # checkP     - value for the number of years to pass before a checkpoint is reached and the model is saved
    # metric     - metric to consider when loading dataframes ("cosine" - loads dataframes created based on the cosine similarity, "dot" - loads dataframes created based on the dot product, "both" - loads all dataframes)
    # dimension  - dimension to load (2 - loads 2D dataframes, 3 - loads 3D dataframes, "both" - loads all dataframes)
    # saveFolder - folder to retrieve data from
    # return     - lists with all the years to parse, chosen dataframes and their global limits dictionary

    # Create year list for future plots
    yearList = [*range(beg, end + 1, checkP)]

    # If last year on the list is not == end then add that year
    if (yearList[-1] != end):
        yearList.append(end)

    # Important lists
    if (dimension == 2 or dimension == "both"):
        dataListComplete2D = [] # List saving 2D dataframes of all words for each plot
        if (metric == "dot" or  metric == "both"):
            dataListCompleteDot2D = [] # Temporary list saving 2D dataframes of all words for each plot created based on the dot product

    if (dimension == 3 or dimension == "both"):
        dataListComplete3D = [] # List saving 3D dataframes of all words for each plot
        if (metric == "dot" or  metric == "both"):
            dataListCompleteDot3D = [] # Temporary list saving 3D dataframes of all words for each plot created based on the dot product

    # Dictionary initialization
    keys2D = ["limMinX", "limMaxX", "limMinY", "limMaxY", "limMinXDot", "limMaxXDot", "limMinYDot", "limMaxYDot"]
    keys3D = ["limMinX", "limMaxX", "limMinY", "limMaxY", "limMinZ", "limMaxZ", "limMinXDot", "limMaxXDot", "limMinYDot", "limMaxYDot", "limMinZDot", "limMaxZDot"]

    limitsDict2D = {key: 0 for key in keys2D} # Dictionary with the global 2D limits for all plots
    limitsDict3D = {key: 0 for key in keys3D} # Dictionary with the global 3D limits for all plots

    # Find dataframes folder
    dataFolders = [folder for folder in os.listdir(saveFolder) if folder.split("_")[0] == "Checkpoint"]
    dataFolders = sorted(dataFolders, key = lambda x: int(x.split("_")[-1]))

    print()
    print("Loading data...")

    # Load all data
    for folder in dataFolders:
        # Grab all data files
        dataFiles = os.listdir(os.path.join(saveFolder, folder))

        for file in dataFiles:
            file = file.split("_")

            if (dimension == 3 or dimension == "both"):
                # Load dataframeComplete3D
                if(file[0] == "dataframeComplete3D" and not file[1] == "dot" and (metric == "cosine" or metric == "both")):
                    dataComplete = pd.read_csv(os.path.join(saveFolder, folder, "_".join(file)))
                    dataListComplete3D.append(dataComplete)

                    # Calculate the global 3D limits, the limits are shared by all global plots
                    if (limitsDict3D["limMinX"] > min(dataComplete.x)):
                        limitsDict3D["limMinX"] = min(dataComplete.x)

                    if (limitsDict3D["limMaxX"] < max(dataComplete.x)):
                        limitsDict3D["limMaxX"] = max(dataComplete.x)

                    if (limitsDict3D["limMinY"] > min(dataComplete.y)):
                        limitsDict3D["limMinY"] = min(dataComplete.y)

                    if (limitsDict3D["limMaxY"] < max(dataComplete.y)):
                        limitsDict3D["limMaxY"] = max(dataComplete.y)

                    if (limitsDict3D["limMinZ"] > min(dataComplete.z)):
                        limitsDict3D["limMinZ"] = min(dataComplete.z)

                    if (limitsDict3D["limMaxZ"] < max(dataComplete.z)):
                        limitsDict3D["limMaxZ"] = max(dataComplete.z)

                    print("Global 3D dataframes loaded - cosine similarity")

                # Load dataframeComplete3D_dot
                if(file[0] == "dataframeComplete3D" and file[1] == "dot" and (metric == "dot" or metric == "both")):
                    dataComplete = pd.read_csv(os.path.join(saveFolder, folder, "_".join(file)))
                    dataListCompleteDot3D.append(dataComplete)

                    # Calculate the global 3D limits, the limits are shared by all global plots
                    if (limitsDict3D["limMinXDot"] > min(dataComplete.x)):
                        limitsDict3D["limMinXDot"] = min(dataComplete.x)

                    if (limitsDict3D["limMaxXDot"] < max(dataComplete.x)):
                        limitsDict3D["limMaxXDot"] = max(dataComplete.x)

                    if (limitsDict3D["limMinYDot"] > min(dataComplete.y)):
                        limitsDict3D["limMinYDot"] = min(dataComplete.y)

                    if (limitsDict3D["limMaxYDot"] < max(dataComplete.y)):
                        limitsDict3D["limMaxYDot"] = max(dataComplete.y)

                    if (limitsDict3D["limMinZDot"] > min(dataComplete.z)):
                        limitsDict3D["limMinZDot"] = min(dataComplete.z)

                    if (limitsDict3D["limMaxZDot"] < max(dataComplete.z)):
                        limitsDict3D["limMaxZDot"] = max(dataComplete.z)

                    print("Global 3D dataframes loaded - dot product")

            if (dimension == 2 or dimension == "both"):
                # Load dataframeComplete2D
                if(file[0] == "dataframeComplete2D" and not file[1] == "dot" and (metric == "cosine" or metric == "both")):
                    dataComplete = pd.read_csv(os.path.join(saveFolder, folder, "_".join(file)))
                    dataListComplete2D.append(dataComplete)

                    # Calculate the global 2D limits, the limits are shared by all global plots
                    if (limitsDict2D["limMinX"] > min(dataComplete.x)):
                        limitsDict2D["limMinX"] = min(dataComplete.x)

                    if (limitsDict2D["limMaxX"] < max(dataComplete.x)):
                        limitsDict2D["limMaxX"] = max(dataComplete.x)

                    if (limitsDict2D["limMinY"] > min(dataComplete.y)):
                        limitsDict2D["limMinY"] = min(dataComplete.y)

                    if (limitsDict2D["limMaxY"] < max(dataComplete.y)):
                        limitsDict2D["limMaxY"] = max(dataComplete.y)

                    print("Global 2D dataframes loaded - cosine similarity")

                # Load dataframeComplete2D_dot
                if(file[0] == "dataframeComplete2D" and file[1] == "dot" and (metric == "dot" or metric == "both")):
                    dataComplete = pd.read_csv(os.path.join(saveFolder, folder, "_".join(file)))
                    dataListCompleteDot2D.append(dataComplete)

                    # Calculate the global 2D limits, the limits are shared by all global plots
                    if (limitsDict2D["limMinXDot"] > min(dataComplete.x)):
                        limitsDict2D["limMinXDot"] = min(dataComplete.x)

                    if (limitsDict2D["limMaxXDot"] < max(dataComplete.x)):
                        limitsDict2D["limMaxXDot"] = max(dataComplete.x)

                    if (limitsDict2D["limMinYDot"] > min(dataComplete.y)):
                        limitsDict2D["limMinYDot"] = min(dataComplete.y)

                    if (limitsDict2D["limMaxYDot"] < max(dataComplete.y)):
                        limitsDict2D["limMaxYDot"] = max(dataComplete.y)

                    print("Global 2D dataframes loaded - dot product")

    print("Loading complete")
    
    # Combine list if 3D dot product list has information
    if ((metric == "dot" or metric == "both") and (dimension == 3 or dimension == "both")):
        dataListComplete3D = dataListComplete3D + [-1] + dataListCompleteDot3D

    # Combine list if 2D dot product list has information
    if ((metric == "dot" or metric == "both") and (dimension == 2 or dimension == "both")):
        dataListComplete2D = dataListComplete2D + [-1] + dataListCompleteDot2D

    # Return loaded dataframes
    if (dimension == 2):
        return yearList, dataListComplete2D, limitsDict2D
    elif (dimension == 3):
        return yearList, dataListComplete3D, limitsDict3D
    else:
        return yearList, dataListComplete2D, dataListComplete3D, limitsDict2D, limitsDict3D

def plotGlobal2D(yearList, dataListComplete, limitsDict, show = True, save = False, saveFolder = None):
    # Creates the global 2D plots with all the words
    # yearList         - list with all the years in the interval to consider
    # dataListComplete - list with the complete dataframes with all the words in the model for each plot
    # limitsDictList   - dictionary with the global limits for all plots
    # show             - wether to show plots or not
    # save             - wether to save plots or not
    # saveFolder       - folder to save data
    # return           - none

    # Variable for controlling the change in dataframes based on the cosine similarity to the dataframes based on the dot product
    dot = False

    # Variable for indexes of list that are the same for cosine similarity and dot product data
    repIndex = 0

    # Plot data
    for count, dataComplete in enumerate(dataListComplete):
        # Check if the dataframes changed in metric
        if (not isinstance(dataComplete, pd.DataFrame)):
            dot = True
            repIndex = 0
            continue

        fig, ax = plt.subplots(figsize=(20,20))

        if (not dot):
            fig.suptitle("Metric: Cosine Similarity")
        else:
            fig.suptitle("Metric: Dot Product")

        # Plot the word points
        ax.plot(dataComplete.x, dataComplete.y, color='crimson', marker='o', linestyle='None', markersize=5, alpha=0.40)

        # Defining Axes
        offset = 0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits
        if (not dot):
            ax.set_xlim(limitsDict["limMinX"] - offset, limitsDict["limMaxX"] + offset)
            ax.set_ylim(limitsDict["limMinY"] - offset, limitsDict["limMaxY"] + offset)
        else:
            ax.set_xlim(limitsDict["limMinXDot"] - offset, limitsDict["limMaxXDot"] + offset)
            ax.set_ylim(limitsDict["limMinYDot"] - offset, limitsDict["limMaxYDot"] + offset)

        # Title
        ax.set_title(f"{yearList[repIndex]} - {yearList[repIndex + 1]} (Number of words: {len(dataComplete.index)})")

        # Save plot
        if (save):
            if (not dot):
                plt.savefig(os.path.join(saveFolder, "Checkpoint_" + str(repIndex + 1), "AllWordsPlot2D_" + str(repIndex + 1) + ".png"))
            else:
                plt.savefig(os.path.join(saveFolder, "Checkpoint_" + str(repIndex + 1), "AllWordsPlot2D_Dot_" + str(repIndex + 1) + ".png"))

        if (show):
            plt.show()

        repIndex += 1

    return None

def plotGlobal3D(yearList, dataListComplete, limitsDict, show = True, save = False, saveFolder = None):
    # Creates the global 3D plots with all the words
    # yearList         - list with all the years in the interval to consider
    # dataListComplete - list with the complete dataframes with all the words in the model for each plot
    # limitsDictList   - dictionary with the global limits for all plots
    # show             - wether to show plots or not
    # save             - wether to save plots or not
    # saveFolder       - folder to save data
    # return           - none

    # Variable for controlling the change in dataframes based on the cosine similarity to the dataframes based on the dot product
    dot = False

    # Variable for indexes of list that are the same for cosine similarity and dot product data
    repIndex = 0

    # Plot data
    for count, dataComplete in enumerate(dataListComplete):
        # Check if the dataframes changed in metric
        if (not isinstance(dataComplete, pd.DataFrame)):
            dot = True
            repIndex = 0
            continue

        fig = plt.figure(figsize=(20,20))
        ax = fig.add_subplot(projection='3d')

        if (not dot):
            fig.suptitle("Metric: Cosine Similarity")
        else:
            fig.suptitle("Metric: Dot Product")

        # Plot the word points
        ax.plot(dataComplete.x, dataComplete.y, dataComplete.z, color='crimson', marker='o', linestyle='None', markersize=5, alpha=0.40)

        # Defining Axes
        offset = 0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits
        if (not dot):
            ax.set_xlim(limitsDict["limMinX"] - offset, limitsDict["limMaxX"] + offset)
            ax.set_ylim(limitsDict["limMinY"] - offset, limitsDict["limMaxY"] + offset)
            ax.set_zlim(limitsDict["limMinZ"] - offset, limitsDict["limMaxZ"] + offset)
        else:
            ax.set_xlim(limitsDict["limMinXDot"] - offset, limitsDict["limMaxXDot"] + offset)
            ax.set_ylim(limitsDict["limMinYDot"] - offset, limitsDict["limMaxYDot"] + offset)
            ax.set_zlim(limitsDict["limMinZDot"] - offset, limitsDict["limMaxZDot"] + offset)

        # Title
        ax.set_title(f"{yearList[repIndex]} - {yearList[repIndex + 1]} (Number of words: {len(dataComplete.index)})")

        # Save plot
        if (save):
            if (not dot):
                plt.savefig(os.path.join(saveFolder, "Checkpoint_" + str(repIndex + 1), "AllWordsPlot3D_" + str(repIndex + 1) + ".png"))
            else:
                plt.savefig(os.path.join(saveFolder, "Checkpoint_" + str(repIndex + 1), "AllWordsPlot3D_Dot_" + str(repIndex + 1) + ".png"))

        if (show):
            plt.show()

        repIndex += 1

    return None