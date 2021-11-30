# Script that collects all unprocessed corpora from a given year interval. Auxiliary script, used in CorpusProcessing.py

import os

# Always print to console
import functools
print = functools.partial(print, flush=True)

def unprocessedCorpusCollector(year1, year2):
    # Collects all unprocessed corpora from a given year interval
    # year1  - first year of the interval
    # year2  - last year of the interval
    # return - dictionary whose keys are the years to be processed and the values are the unprocessed corpora list 

    # Main folder with all the year's folders
    mainFolder = os.path.join(os.getcwd(), "Years")

    # Dictionary to save all the unprocessed collected corpus 
    unpCorpusDict = {}

    # Loop for running in all years inside user defined interval
    for year in range(year1, year2 + 1):
        # Folder with the unprocessed text
        unprocessedFolder = os.path.join(mainFolder, str(year), "UNPROCESSED_TEXT")

        # Grab a list of all files inside the folder
        unprocessedCorpora = os.listdir(unprocessedFolder)

        # Check if the new list is not empty
        if (len(unprocessedCorpora) != 0):
            # Save in dictionary
            unpCorpusDict[year] = unprocessedCorpora
            print(f"All unprocessed corpora from {year} collected.")
        else:
            print(f"{year} with no unprocessed corpora to collect.")

    print("All unprocessed corpora collected.")

    return unpCorpusDict