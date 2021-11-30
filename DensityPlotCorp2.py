# Auxiliary script, used by DensityCorp2Processing.py

# Functions in this script are responsible for:
# - Plotting density plots based on the given data

import pandas as pd
import matplotlib.cm
import matplotlib.pyplot as plt
import os
import numpy as np
import math

# Always print to console
import functools
print = functools.partial(print, flush=True)

def densityPlot(dataList, dataType, limitsList, metric, maxCB, step, show = True, save = False, saveFolder = None):
    # Creates density plots based on the given data
    # dataList   - list with all the dataframes
    # dataType   - dataframe type ("global" - complete dataframes with all words of the model, "square" - dataframes of the square models)
    # limitsList - list with the dictionaries with the plots limits or just a dictionary with the global limits
    # metric     - metric to consider when creating density plots ("cosine" - density plots based on the cosine similarity, "dot" - density plots based on the dot product, "both" - loads all dataframes)
    # maxCB      - max value for the highest tick of the color bar
    # step       - difference between two consecutive ticks
    # show       - wether to show plots or not
    # save       - wether to save plots or not
    # saveFolder - folder to save data
    # return     - none

    # Color map definition
    colorMap = matplotlib.cm.get_cmap('viridis', 20)
    ticksLabel = [*range(0, maxCB + 1, step)]

    # Density plot - global plots
    if (dataType == "global"):
        # Variable for the change in metric
        dot = False

        # Variable for indexes of list that are the same for cosine similarity and dot product data
        repIndex = 0

        for count, data in enumerate(dataList):
            # Check if the change in metric has been made
            if (not isinstance(dataList[count], pd.DataFrame)):
                if (metric == "dot" or metric == "both"):
                    dot = True
                    repIndex = 0
                    continue
                else:
                    break

            # Density plot - Global
            fig, ax = plt.subplots(figsize=(20,20))

            if (not dot):
                fig.suptitle("Metric: Cosine Similarity")

                offset = 0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits

                # Histogram configuration
                hist, xedges, yedges = np.histogram2d(data.x, data.y, bins = 100, range = [[limitsList["limMinX"] - offset, limitsList["limMaxX"] + offset], [limitsList["limMinY"] - offset, limitsList["limMaxY"] + offset]])
                hist = hist.T

                # Defining Axes
                ax.set_xlim(limitsList["limMinX"] - offset, limitsList["limMaxX"] + offset)
                ax.set_ylim(limitsList["limMinY"] - offset, limitsList["limMaxY"] + offset)
            else:
                fig.suptitle("Metric: Dot Product")

                offset = 0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits

                # Histogram configuration
                hist, xedges, yedges = np.histogram2d(data.x, data.y, bins = 100, range = [[limitsList["limMinXDot"] - offset, limitsList["limMaxXDot"] + offset], [limitsList["limMinYDot"] - offset, limitsList["limMaxYDot"] + offset]])
                hist = hist.T

                # Defining Axes
                ax.set_xlim(limitsList["limMinXDot"] - offset, limitsList["limMaxXDot"] + offset)
                ax.set_ylim(limitsList["limMinYDot"] - offset, limitsList["limMaxYDot"] + offset)

            # Title
            ax.set_title(f"Plot: {repIndex + 1} (Number of words: {len(data.index)})")

            # Plot
            x, y = np.meshgrid(xedges, yedges)
            im = ax.pcolormesh(x, y, hist, cmap = colorMap, vmin = 0, vmax = maxCB)
            cbar = plt.colorbar(im, ticks = ticksLabel)
            cbar.ax.set_yticklabels([str(x) for x in ticksLabel])

            # Save plots
            if (save):
                if (not dot):
                    plt.savefig(os.path.join(saveFolder, "AllWordsDensity_" + str(repIndex + 1) + ".png"))
                else:
                    plt.savefig(os.path.join(saveFolder, "AllWordsDensity_Dot_" + str(repIndex + 1) + ".png"))

            if (show):
                plt.show()

            repIndex += 1

    # Density plot - square plot
    if (dataType == "square"):
        # Separate cosine dataframes from dot dataframes inside dataList
        dot = False
        sqDataList = []
        sqDataListDot = []

        # Check if there are limits for the plots
        if (limitsList):
            sqLimitsList = []
            sqLimitsListDot = []

        for count in range(len(dataList)):
            # Check if the change in metric has been made
            if (not isinstance(dataList[count], pd.DataFrame)):
                if (metric == "dot" or metric == "both"):
                    dot = True
                    continue
                else:
                    break

            if (not dot):
                sqDataList.append(dataList[count])

                if (limitsList):
                    sqLimitsList.append(limitsList[count])
            else:
                sqDataListDot.append(dataList[count])

                if (limitsList):
                    sqLimitsListDot.append(limitsList[count])

        # Calculate number of rows
        if (sqDataList):
            numRows = math.floor(len(sqDataList) / 5)
        else:
            numRows = math.floor(len(sqDataListDot) / 5)

        # Plot cosine similarity density data if exits
        if (sqDataList):
            # Create global fig
            fig = plt.figure(figsize=(50,50))
            fig.suptitle("Metric: Cosine Similarity", fontsize=30)

            for count, data in enumerate(sqDataList):
                # Subplot configuration
                ax = fig.add_subplot(numRows, 5, count + 1)
                ax.set_aspect("equal")

                if (limitsList):
                    offset = 0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits

                    # Histogram configuration
                    hist, xedges, yedges = np.histogram2d(data.x, data.y, bins = 10, range = [[sqLimitsList[count]["limMinX"], sqLimitsList[count]["limMaxX"]], [sqLimitsList[count]["limMinY"], sqLimitsList[count]["limMaxY"]]])
                    hist = hist.T

                    # Defining Axes
                    ax.set_xlim(sqLimitsList[count]["limMinX"] - offset, sqLimitsList[count]["limMaxX"] + offset)
                    ax.set_ylim(sqLimitsList[count]["limMinY"] - offset, sqLimitsList[count]["limMaxY"] + offset)
                else:
                    # Histogram configuration
                    hist, xedges, yedges = np.histogram2d(data.x, data.y, bins = 10)
                    hist = hist.T

                # Title
                ax.set_title(f"Plot: {count + 1}", fontsize=30)

                # Plot
                x, y = np.meshgrid(xedges, yedges)
                im = ax.pcolormesh(x, y, hist, cmap = colorMap, vmin = 0, vmax = maxCB)

            # Color bar
            fig.subplots_adjust(bottom=0.2, top=0.9, left=0.1, right=0.9, wspace=0.4, hspace=0.1)
            cb_ax = fig.add_axes([0.1, 0.1, 0.8, 0.02])
            cbar = plt.colorbar(im, cax = cb_ax, orientation = "horizontal", ticks = ticksLabel)
            cbar.ax.set_xticklabels([str(x) for x in ticksLabel])

            # Save plots
            if (save):
                plt.savefig(os.path.join(saveFolder, "SquareWordsDensity.png"))

            if (show):
                plt.show()

        # Plot dot product density data if exits
        if (sqDataListDot):
            # Create global fig
            fig = plt.figure(figsize=(50,50))
            fig.suptitle("Metric: Dot Product", fontsize=30)

            for count, data in enumerate(sqDataListDot):
                # Subplot configuration
                ax = fig.add_subplot(numRows, 5, count + 1)
                ax.set_aspect("equal")

                if (limitsList):
                    offset = 0.0 # Change this number to adjust the plot limits in case a little offset is wanted for the limits

                    # Histogram configuration
                    hist, xedges, yedges = np.histogram2d(data.x, data.y, bins = 10, range = [[sqLimitsListDot[count]["limMinXDot"], sqLimitsListDot[count]["limMaxXDot"]], [sqLimitsListDot[count]["limMinYDot"], sqLimitsListDot[count]["limMaxYDot"]]])
                    hist = hist.T

                    # Defining Axes
                    ax.set_xlim(sqLimitsListDot[count]["limMinXDot"] - offset, sqLimitsListDot[count]["limMaxXDot"] + offset)
                    ax.set_ylim(sqLimitsListDot[count]["limMinYDot"] - offset, sqLimitsListDot[count]["limMaxYDot"] + offset)
                else:
                    # Histogram configuration
                    hist, xedges, yedges = np.histogram2d(data.x, data.y, bins = 10)
                    hist = hist.T

                # Title
                ax.set_title(f"Plot: {count + 1}", fontsize=30)

                # Plot
                x, y = np.meshgrid(xedges, yedges)
                im = ax.pcolormesh(x, y, hist, cmap = colorMap, vmin = 0, vmax = maxCB)

            # Color bar
            fig.subplots_adjust(bottom=0.2, top=0.9, left=0.1, right=0.9, wspace=0.4, hspace=0.1)
            cb_ax = fig.add_axes([0.1, 0.1, 0.8, 0.02])
            cbar = plt.colorbar(im, cax = cb_ax, orientation = "horizontal", ticks = ticksLabel)
            cbar.ax.set_xticklabels([str(x) for x in ticksLabel])

            # Save plots
            if (save):
                plt.savefig(os.path.join(saveFolder, "SquareWordsDensity_Dot.png"))

            if (show):
                plt.show()

    return None