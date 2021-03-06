# psyLex: an open-source implementation of the Linguistic Inquiry Word Count
# Created by Sean C. Rife, Ph.D.
# srife1@murraystate.edu // seanrife.com // @seanrife
# Licensed under the MIT License

# Function to count and categorize words based on an LIWC dictionary

# this version was tweaked by Maria Priestley, priestleymaria@yahoo.co.uk
# Sean's original code can be found at https://github.com/seanrife/psyLex

import collections, nltk
from nltk.tokenize import RegexpTokenizer

def wordCount(data, dictOutput, catList):
    # Create a new dictionary for the output
    outList = collections.OrderedDict()

    # Number of non-dictionary words
    nonDict = 0

    # Convert to lowercase
    data = data.lower()

    # Tokenize and create a frequency distribution
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(data)

    fdist = nltk.FreqDist(tokens)
    wc = len(tokens)
    
    # bad stems
    bad_stems = []

    # Using the Porter stemmer for wildcards, create a stemmed version of the data
    porter = nltk.PorterStemmer()
    stems = [porter.stem(word) for word in tokens]
    # handle bad stems
    # some words get counted twice due to created stem being different from the actual word
    # e.g. "happy" gets stemmed to "happi*" which produces an additional distinct match later on 
    # so we fix this
    for stem in stems:
        good_token = False
        for token in tokens:
            if stem in token:
                good_token = True
        if good_token == False:
            bad_stems.append(stem)
    
    fdist_stem = nltk.FreqDist(stems)

    # Access categories and populate the output dictionary with keys
    for cat in catList:
        outList[cat[0]] = 0

    # Dictionaries are more useful
    fdist_dict = dict(fdist)
    fdist_stem_dict = dict(fdist_stem)
    # print(bad_stems)
    for stem in bad_stems:
        fdist_stem_dict.pop(stem, None)
    # print(fdist_stem_dict)

    # Number of classified words
    classified = 0

    for key in dictOutput:
        if "*" in key and key[:-1] in fdist_stem_dict:
            classified = classified + fdist_stem_dict[key[:-1]]
            for cat in dictOutput[key]:
                outList[cat] = outList[cat] + fdist_stem_dict[key[:-1]]
        elif key in fdist_dict:
            classified = classified + fdist_dict[key]
            for cat in dictOutput[key]:
                outList[cat] = outList[cat] + fdist_dict[key]

    # Calculate the percentage of words classified
    if wc > 0:
        percClassified = (float(classified) / float(wc)) * 100
    else:
        percClassified = 0

    # Return the categories, the words used, the word count, the number of words classified, and the percentage of words classified.
    return [outList, tokens, wc, classified, percClassified]