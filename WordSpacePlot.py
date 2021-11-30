# Script used to plot the words. Adapted from the code written by Miguel Bernardo in his master degree thesis "Construction of Geometries Based on Automatic Text Interpretation". Auxiliary script, used in DataCreator.py

from __future__ import absolute_import, division, print_function
import numpy as np
import gensim.models.word2vec as w2v
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def createDataframe(model, matrix, dimension):
    # Creates either a 2D or 3D dataframe from a given model and matrix
    # model     - model to be used in the dataframe creation
    # matrix    - matrix to be used in the dataframe creation
    # dimension - dimension to consider for the dataframe, either 2 or 3
    # return    - dataframe with all the matrix points

    # Information for the user
    print("Model loaded")

    # Vocabulary length
    vocab_len = len(model.wv.vocab)
    print("Vocabulary length is ", vocab_len)

    word_vectors_matrix_reduced = matrix

    word_list = []
    i = 0
    for word in model.wv.vocab:
        word_list.append(word)
        i += 1
        if i == vocab_len:
            break

    # Word points DataFrame - 2D
    if (dimension == 2):
        
        points = pd.DataFrame([
            (word, coords[0], coords[1])
            for word, coords in [
                (word, word_vectors_matrix_reduced[word_list.index(word)])
                for word in word_list
            ]
        ], columns=["Word", "x", "y"])

    # Word points DataFrame - 3D
    if (dimension == 3):
        points = pd.DataFrame([
            (word, coords[0], coords[1], coords[2])
            for word, coords in [
                (word, word_vectors_matrix_reduced[word_list.index(word)])
                for word in word_list
            ]
        ], columns=["Word", "x", "y", "z"])

    return points