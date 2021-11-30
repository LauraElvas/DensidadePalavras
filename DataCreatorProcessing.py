# Menu script to facilitate the creation of data

# Possible Actions:
# - Create models, 2D and 3D dataframes in a given interval, saving them at given checkpoints (bulk creation available) and plot them
# - Load all the created dataframes and plot them

import os

import DataCreator

# Always print to console
import functools
print = functools.partial(print, flush=True)

#--------------------------------------- CONFIGURATIONS ----------------------------------------------

# Change these variables if there is an increase in data and more years are added and if the maximum number of years before a checkpoint is reached needs to be bigger
minYear  = 1987
maxYear  = 2020
checkMax = 10

#------------------------------------------- CODE ----------------------------------------------------

# Changes in the following code may break it

def validateFunction(choice, type):
    # Verifies if the value is in accordance with the type of action made
    # choice   - value of the choice made
    # type     - type of validation to be made, "option", "interval", "checkpoint", "dimension" or "metric"
    # return   - wether value is valid or not and choice, -1 is invalidity of the choice or type

    # Check if choice is empty
    if (not choice):
        return False, -1

    # Verifies input for the option menu
    if (type == "option"):
        validationCondition = (choice == "1") or (choice == "2")

        return validationCondition, -1
    
    # Verifies input for the interval
    if (type == "interval"):
        for count, yearInt in enumerate(choice):
            yearInt = yearInt.split("-")

            if (len(yearInt) < 2):
                return False, -1

            validationCondition = yearInt[0].isnumeric() and yearInt[1].isnumeric()

            if (not validationCondition):
                return False, -1
            else:
                yearInt[0] = int(yearInt[0])
                yearInt[1] = int(yearInt[1])
                choice[count] = [yearInt[0], yearInt[1]]
                validationCondition = (yearInt[0] <= yearInt[1]) and (yearInt[0] >= minYear) and (yearInt[1] <= maxYear)

                if(not validationCondition):
                    return False, -1

        return True, choice

    # Verifies input for the checkpoint
    if (type == "checkpoint"):
        if (not all(x.isnumeric() for x in choice)):
            return False, -1

        for count, checkP in enumerate(choice):
            choice[count] = int(checkP)
            validationCondition = (choice[count] > 0) and (choice[count] <= checkMax)
        
            if (not validationCondition):
                return False, -1

        return True, choice

    # Verifies input for the dimension
    if (type == "dimension"):
        validationCondition = (choice == "2") or (choice == "3") or (choice == "both")

        if (choice.isnumeric()):
            choice = int(choice)

        return validationCondition, choice

    # Verifies input for the metric
    if (type == "metric"):
        validationCondition = (choice == "cosine") or (choice == "dot") or (choice == "both")

        return validationCondition, choice

    return False, -1

# Loop controling variables
run = True
menu = True

# Menu Loop
while (run):

    # User menu
    if (menu):
        print("What would you like to do?")
        print("1 - Create models and 2D or 3D dataframes in a given interval, saving them at given checkpoints and plot them (bulk creation available)")
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
        dimension = input(f"Input if data created must be 2D, 3D or both (2 for 2D, 3 for 3D or word \"both\"): ")

        # Validate answer - dimension
        validationCondition2, dimension = validateFunction(dimension, "dimension")

        while (not validationCondition2):
            dimension = input(f"Input is not valid. Must be 2, 3 or word \"both\". Try again: ")
            validationCondition2, dimension = validateFunction(dimension, "dimension")

        print()
        metric = input(f"Input if data created is based on cosine similarity, dot product or both (cosine for cosine similarity, dot for dot product or word \"both\"): ")

        # Validate answer - metric
        validationCondition3, metric = validateFunction(metric, "metric")

        while (not validationCondition3):
            metric = input(f"Input is not valid. Must be cosine, dot or word \"both\". Try again: ")
            validationCondition3, metric = validateFunction(metric, "metric")

        menu = False

	# Option 1 - Create models and 2D or 3D dataframes in a given interval, saving them at given checkpoints and plot them
    if (option == "1"):
        print()
        interval = input(f"Input an interval from {minYear} to {maxYear} in the form ####-#### (an interval of the type ####-#### followed by a comma and another interval, ex. 2000-2008,2010-2020, will perform the action in bulk over the multiple intervals): ")

	    # Validate answer - interval
        interval = interval.split(",")
        validationCondition4, interval = validateFunction(interval, "interval")

        while (not validationCondition4):
            interval = input(f"Input is not valid. Must be of the form ####-#### or ####-####,####-#### with no space before or after commas or \"-\" and between {minYear} to {maxYear}. Try again: ")
            interval = interval.split(",")
            validationCondition4, interval = validateFunction(interval, "interval")

        print()
        checkpoint = input(f"Input how many years must go by until the model reaches a checkpoint and saves (must be a number smaller or equal to {checkMax}. An input of the form #,#, no space before or after commas, will perform the action in bulk over the multiple checkpoints): ")

        # Validate answer - checkpoint
        checkpoint = checkpoint.split(",")
        validationCondition5, checkpoint = validateFunction(checkpoint, "checkpoint")

        while (not validationCondition5):
            checkpoint = input(f"Input is not a valid number or group of numbers. Must input numbers smaller or equal to {checkMax} and no space before or after commas. Try again: ")
            checkpoint = checkpoint.split(",")
            validationCondition5, checkpoint = validateFunction(checkpoint, "checkpoint")

        print()

        # Cycle through all year intervals
        for intv in interval:
            beg = intv[0]
            end = intv[1]

            # Cycle through all different checkpoints options
            for checkP in checkpoint:
                # Create save folder
                saveFolder = os.path.join("Saved Data", str(beg) + "_" + str(end) + "_" + str(checkP))

                if not os.path.exists(saveFolder):
                    os.makedirs(saveFolder)

                # Create data
                DataCreator.dataCreator(beg, end, checkP, saveFolder)

                if (dimension == "both"):
                    # Load data
                    yearList, dataListComplete2D, dataListComplete3D, limitsDict2D, limitsDict3D = DataCreator.loadData(beg, end, checkP, metric, dimension, saveFolder)

                    # Plot data
                    DataCreator.plotGlobal2D(yearList, dataListComplete2D, limitsDict2D, False, True, saveFolder)
                    DataCreator.plotGlobal3D(yearList, dataListComplete3D, limitsDict3D, False, True, saveFolder)

                else:
                    # Load data
                    yearList, dataListComplete, limitsDict = DataCreator.loadData(beg, end, checkP, metric, dimension, saveFolder)

                    # Plot data
                    if (dimension == 2):
                        DataCreator.plotGlobal2D(yearList, dataListComplete, limitsDict, False, True, saveFolder)
                    elif (dimension == 3):
                         DataCreator.plotGlobal3D(yearList, dataListComplete, limitsDict, False, True, saveFolder)

        close = True

    # Option 2 - Load and visualise previously created data
    if (option == "2"):
        # Check if data exists
        validationCondition6 = False
        while (not validationCondition6):
            print()
            interval = input(f"Input an interval from {minYear} to {maxYear} in the form ####-#### (ex. 2000-2008): ")

            # Validate answer - interval (extra steps - no bulk action available)
            interval = interval.split(",")
            if (len(interval) > 1):
                validationCondition4 = False
            else:
                validationCondition4, interval = validateFunction(interval, "interval")

            while (not validationCondition4):
                interval = input(f"Input is not valid. Must be of the form ####-#### with no space before or after \"-\" and between {minYear} to {maxYear}. Try again: ")

                interval = interval.split(",")
                if (len(interval) > 1):
                    validationCondition4 = False
                else:
                    validationCondition4, interval = validateFunction(interval, "interval")

            print()
            checkpoint = input(f"Input how many years must go by until the model reaches a checkpoint and saves (must be a number smaller or equal to {checkMax}): ")

            # Validate answer - checkpoint (extra steps - no bulk action available)
            checkpoint = checkpoint.split(",")
            if (len(checkpoint) > 1):
                validationCondition5 = False
            else:
                validationCondition5, checkpoint = validateFunction(checkpoint, "checkpoint")

            while (not validationCondition5):
                checkpoint = input(f"Input is not a valid number or group of numbers. Must input numbers smaller or equal to {checkMax} and no space before or after commas. Try again: ")

                checkpoint = checkpoint.split(",")
                if (len(checkpoint) > 1):
                    validationCondition5 = False
                else:
                    validationCondition5, checkpoint = validateFunction(checkpoint, "checkpoint")

            # Years info
            beg = interval[0][0]
            end = interval[0][1]

            # Save folder
            saveFolder = os.path.join("Saved Data", str(beg) + "_" + str(end) + "_" + str(checkpoint[0]))

            if (not os.path.exists(saveFolder)):
                print()
                print("No data created with the information chosen. Try again")
            else:
                validationCondition6 = True

        print()

        checkP = checkpoint[0]

        if (dimension == "both"):
            # Load data
            yearList, dataListComplete2D, dataListComplete3D, limitsDict2D, limitsDict3D = DataCreator.loadData(beg, end, checkP, metric, dimension, saveFolder)

            # Plot data
            DataCreator.plotGlobal2D(yearList, dataListComplete2D, limitsDict2D)
            DataCreator.plotGlobal3D(yearList, dataListComplete3D, limitsDict3D)

        else:
        	# Load data
        	yearList, dataListComplete, limitsDict = DataCreator.loadData(beg, end, checkP, metric, dimension, saveFolder)

        	# Plot data
        	if (dimension == 2):
        		DataCreator.plotGlobal2D(yearList, dataListComplete, limitsDict)
        	elif (dimension == 3):
        		DataCreator.plotGlobal3D(yearList, dataListComplete, limitsDict)

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