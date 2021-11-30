# Script that concentrates all corpus related functions for ease of use in case corpus processing is required. Although the corpus processing usually happens only once, if more data is acquired or for some reason the reprocessing needs to happen again, this script allows a quick way of doing it.

# Possible Actions:
# - Clean the individual corpora of news and articles
# - Combine individual processed news and articles into a main clean corpus

import os

import CorpusCombinator
import CorpusCollector
import CorpusCleaning

# Always print to console
import functools
print = functools.partial(print, flush=True)

#--------------------------------------- CONFIGURATIONS ----------------------------------------------

# Change these variables if there is an increase in data and more years are added
minYear = 1987
maxYear = 2020

#------------------------------------------- CODE ----------------------------------------------------

# Changes in the following code may break it

def validateFunction(choice, type):
    # Verifies if the value is in accordance with the type of option to be chosen
    # choice - value of the choice made in the menu
    # type   - type of validation to be made, "option" or "interval"
    # return - wether value is valid or not, -1 invalidity of the choice or type

    # Check if choice is empty
    if (not choice):
        return False, -1, -1

    # Verifies input for the option menu
    if (type == "option"):
        validationCondition = (choice == "1") or (choice == "2")

        return validationCondition, -1, -1
    
    # Verifies input for the interval
    if (type == "interval"):
        
        if (len(choice) == 1 and choice[0].isnumeric()):
            year1 = year2 = int(choice[0])
        elif (len(choice) == 2 and choice[0].isnumeric() and choice[1].isnumeric()):
            year1 = int(choice[0])
            year2 = int(choice[1])
        else:
            year1 = year2 = -1

        validationCondition = (year1 <= year2) and (year1 >= minYear) and (year2 <= maxYear)
        
        return validationCondition, year1, year2

    return False, -1, -1

# Loop controling variables
run = True
menu = True

# Menu Loop
while (run):

    # User menu
    if (menu):
        print("What would you like to do?")
        print("1 - Clean the individual corpora of the news and articles")
        print("2 - Combine individual processed news and articles into a main clean corpus")
        option = input()

        # Validate answer - option
        validationCondition1, _, _ = validateFunction(option, "option")
        while (not validationCondition1):
            option = input("Input is neither 1, 2. Try again: ")
            validationCondition1, _, _ = validateFunction(option, "option")

        print()
        interval = input(f"Input an year from {minYear} to {maxYear} (an interval of the type ####-####, ex. 2000-2008, will perform the action in bulk): ")

        # Validate answer - interval
        interval = interval.split("-")
        validationCondition2, year1, year2 = validateFunction(interval, "interval")

        while (not validationCondition2):
            interval = input(f"Input is not a valid interval. Must be of the form #### or ####-#### and between {minYear} to {maxYear}. Try again: ")
            interval = interval.split("-")
            validationCondition2, year1, year2 = validateFunction(interval, "interval")

        menu = False
    
    # Option 1 - Clean the individual corpora of the news and articles
    if (option == "1"):
        print()
        unprocessedCorpusList = CorpusCollector.unprocessedCorpusCollector(year1, year2)
        CorpusCleaning.corpusCleaning(unprocessedCorpusList)
        close = True

    # Option 2 - Combine individual processed news and articles into a main clean corpus
    if (option == "2"):
        print()
        CorpusCombinator.corpusCombinatorProcessed(year1, year2)
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