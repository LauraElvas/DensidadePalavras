# Script with all functions related to the combination of multiple corpora into one main corpus. Auxiliary script, used by CorpusProcessing.py and DataCreator.py

import os

# Always print to console
import functools
print = functools.partial(print, flush=True)

# Main folder with all the years
mainFolder = os.path.join(os.getcwd(), "Years")

def corpusCombinatorProcessed(year1, year2):
    # Combines all processed corpora present in the folder "CLEAN_TEXTS - YEAR" that's inside the folder of each year into one main clean corpus called "CLEAN_MAIN_CORPUS - YEAR.txt"
    # year1  - first year of the interval
    # year2  - last year of the interval
    # return - none

    # Loop to cycle through the years
    for year in range(year1, year2 + 1):
        # Year folder
        yearFolder = os.path.join(mainFolder, str(year))

        # Grab a list of all files inside "CLEAN_TEXTS"
        corpusFiles = os.listdir(yearFolder)

        # Check if list is empty == no corpus files to collect
        if (("CLEAN_TEXTS - " + str(year)) in corpusFiles):
            # Create main corpus file
            mainCorpus = os.path.join(yearFolder, "CLEAN_MAIN_CORPUS - " + str(year) + ".txt")

            # Loop for reading the individual corpus and appending it to the main corpus
            for corpus in os.listdir(os.path.join(yearFolder, "CLEAN_TEXTS - " + str(year))):
                file = open(os.path.join(yearFolder, "CLEAN_TEXTS - " + str(year), corpus), "r", encoding = "utf-8")
                text = file.read()
                file.close()

                with open(mainCorpus, "a", encoding = "utf-8") as file:
                    file.write(text)

            print(f"Corpora from {year} combined.", flush = True)

        else:
            print(f"No corpus to collect from {year}.", flush = True)
        
    return None

def corpusCombinatorMain(beginning, end, saveFolderName):
    # Combines the clean main corpora from multiple years into one main corpus "CORPUS.txt". If "CORPUS.txt" is already created, it appends the new corpora to it
    # beginning      - first year of the interval
    # end            - last year of the interval
    # saveFolderName - folder where to save and retrieve data
    # return         - "CORPUS.txt" path

    # Create save folder
    if not os.path.exists(saveFolderName):
        os.makedirs(saveFolderName)

    # Corpus path
    mainCorpus = os.path.join(saveFolderName, "CORPUS.txt")

    # Variables for controlling the loop
    year = beginning

    while (year != end + 1):
        # Check if "CLEAN_MAIN_CORPUS" file exists and added it to the main corpus
        if os.path.exists(os.path.join(mainFolder, str(year), "CLEAN_MAIN_CORPUS - " + str(year) + ".txt")):
            corpus = os.path.join(mainFolder, str(year), "CLEAN_MAIN_CORPUS - " + str(year) + ".txt")
            file = open(corpus, "r", encoding = "utf-8")
            text = file.read()
            file.close()

            with open(mainCorpus, "a", encoding = "utf-8") as file:
                file.write(text)

        year += 1

    return mainCorpus