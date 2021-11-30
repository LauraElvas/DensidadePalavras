# Menu script to facilitate the creation of data

# Possible Actions:
# - Create models, 2D and 3D dataframes for a given number of plots
# - Load all the created dataframes and plot them

import os

import DataCreatorCorp2

#--------------------------------------- CONFIGURATIONS ----------------------------------------------

# Change these variables if there is a wish to increase the maximum number of plots to create at once. Warning: creating a big number of plots can take a considerable amount of time
maxPlots = 50

#------------------------------------------- CODE ----------------------------------------------------

# Changes in the following code may break it

def validateFunction(choice, type):
    # Verifies if the value is in accordance with the type of action made
    # choice   - value of the choice made
    # type     - type of validation to be made, "option", "dimension", "metric" or "numPlots"
    # return   - wether value is valid or not and choice, -1 is invalidity of the choice or type

    # Check if choice is empty
    if (not choice):
        return False, -1

    # Verifies input for the option menu
    if (type == "option"):
        validationCondition = (choice == "1") or (choice == "2")

        return validationCondition, -1

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

	# Verifies input for the numPlots
    if (type == "numPlots"):
        if (not all(x.isnumeric() for x in choice)):
            return False, -1

        choice = int(choice[0])
        validationCondition = (choice > 0) and (choice <= maxPlots)
        
        if (not validationCondition):
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
        print("1 - Create models, 2D and 3D dataframes for a given number of plots")
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

        print()
        numPlots = input(f"Input number of plots and dataframes to create: ")

	    # Validate answer - numPlots
        numPlots = numPlots.split(",")
        if (len(numPlots) > 1):
            validationCondition4 = False
        else:
            validationCondition4, numPlots = validateFunction(numPlots, "numPlots")

        while (not validationCondition4):
            numPlots = input(f"Input is not valid. Must be bigger than 0 and smaller than {maxPlots}. Try again: ")

            numPlots = numPlots.split(",")
            if (len(numPlots) > 1):
                validationCondition4 = False
            else:
                validationCondition4, numPlots = validateFunction(numPlots, "numPlots")

        print()
        menu = False

    # Option 1 - Create models, 2D and 3D dataframes for a given number of plots
    if (option == "1"):
        # Create save folder
        saveFolder = os.path.join("Saved Data", "Corpus 2", str(numPlots) + "_plots")

        if not os.path.exists(saveFolder):
            os.makedirs(saveFolder)

        # Create data
        DataCreatorCorp2.dataCreator(numPlots, saveFolder)

        if (dimension == "both"):
            # Load data
            dataListComplete2D, dataListComplete3D, limitsDict2D, limitsDict3D = DataCreatorCorp2.loadData(numPlots, metric, dimension, saveFolder)

            # Plot data
            DataCreatorCorp2.plotGlobal2D(numPlots, dataListComplete2D, limitsDict2D, False, True, saveFolder)
            DataCreatorCorp2.plotGlobal3D(numPlots, dataListComplete3D, limitsDict3D, False, True, saveFolder)

        else:
            # Load data
            dataListComplete, limitsDict = loadData(beg, end, checkP, metric, dimension)

            # Plot data
            if (dimension == 2):
                DataCreatorCorp2.plotGlobal2D(numPlots, dataListComplete, limitsDict, False, True, saveFolder)
            elif (dimension == 3):
                DataCreatorCorp2.plotGlobal3D(numPlots, dataListComplete, limitsDict, False, True, saveFolder)

        close = True

    # Option 2 - Load and visualise previously created data
    if (option == "2"):
        # Save folder
        saveFolder = os.path.join("Saved Data", "Corpus 2", str(numPlots) + "_plots")

        if (dimension == "both"):
            # Load data
            dataListComplete2D, dataListComplete3D, limitsDict2D, limitsDict3D = DataCreatorCorp2.loadData(numPlots, metric, dimension, saveFolder)

            # Plot data
            DataCreatorCorp2.plotGlobal2D(numPlots, dataListComplete2D, limitsDict2D)
            DataCreatorCorp2.plotGlobal3D(numPlots, dataListComplete3D, limitsDict3D)

        else:
            # Load data
            dataListComplete, limitsDict = DataCreatorCorp2.loadData(numPlots, metric, dimension)

            # Plot data
            if (dimension == 2):
                DataCreatorCorp2.plotGlobal2D(numPlots, dataListComplete, limitsDict)
            elif (dimension == 3):
                DataCreatorCorp2.plotGlobal3D(numPlots, dataListComplete, limitsDict)

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