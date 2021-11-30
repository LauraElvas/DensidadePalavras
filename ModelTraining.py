# Script used to create the model. Adapted from the code written by Miguel Bernardo in his master degree thesis "Construction of Geometries Based on Automatic Text Interpretation". Auxiliary script, used in DataCreator.py and DataCreatorCorp2.py

from __future__ import absolute_import, division, print_function
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize

import multiprocessing
import os
import re
import gensim.models.word2vec as w2v

def word_tokenizer(raw):
    clean = re.sub("[^a-zA-Z]"," ", raw)
    words = word_tokenize(clean)
    return words

def createModel(corpus, saveFolderName, modelName, model = None):
    # Creates and trains a Skip-gram model from a given corpus and saves it in the specified folder
    # corpus         - corpus used to train the model
    # saveFolderName - name of the folder where model is going to be saved
    # modelName      - the name to give the model when it is created
    # model          - pre-existing model to train
    # return         - model after training

    # Open Book
    if (not isinstance(corpus, tuple)):
        # If corpus isn't a tuple it means it is corpus 1
        file = open(corpus, encoding='utf-8', errors='ignore')
        book = file.read()
        file.close()
    else:
        # Else is corpus 2
        book = " ".join(corpus)

    print("Book loaded!")

    raw_sentences = sent_tokenize(book)

    sentences = []

    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append(word_tokenizer(raw_sentence))

    # Tokens Counter
    token_count = sum([len(sentence) for sentence in sentences])
    print("This corpus contains {} tokens.".format(token_count))

    # Train The Model
    # If there isn't any pre-existing model, create one
    if (model == None):
        Model = w2v.Word2Vec(
            sg = 1, #Skip-Gram
            workers = multiprocessing.cpu_count(),
            size = 300,
            min_count = 8,
            window = 8,
            sample = 1e-4
        )

        Model.build_vocab(sentences)

    else:
        # Else add any new words to the pre-existing model vocabulary
        Model = model
        Model.build_vocab(sentences, update = True)

    Model.train(sentences, total_examples=Model.corpus_count,
                           epochs=Model.epochs)

    # Save The Model
    if not os.path.exists(saveFolderName):
        os.makedirs(saveFolderName)

    Model.save(os.path.join(saveFolderName, modelName + ".w2v"))

    return Model