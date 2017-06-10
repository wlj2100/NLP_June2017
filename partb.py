import os
import numpy as np
from textstat.textstat import textstat
import pandas as pd
import json

def getComplexity(text):
    try:
        wordInSentence = textstat.lexicon_count(text)/textstat.sentence_count(text)
    except Exception as e:
        wordInSentence = 0
    syllables3 = 0
    for word in text.split():
        if textstat.syllable_count(word) >= 3:
            syllables3 += 1
    try:
        percentageOf3Syllables = float(syllables3) * 100 / textstat.lexicon_count(text)
    except Exception as e:
        percentageOf3Syllables = 0

    complexity = {
    'wordInSentence' : wordInSentence,
    'percentageOf3Syllables' : percentageOf3Syllables
    }
    return complexity
    # return json.dumps(complexity)

def getSize(path):
    size = os.path.getsize(path)
    return size / 1024.0

def lexical_diversity(text):
    if len(text.split()) == 0:
        return 0
    return len(text.split()) / float(len(np.unique(text.split())))

def countSpecial(text):
    specialDict = {
    'supplement' : 0,
    'annual' : 0,
    'update' : 0
    }
    wordList1 = ['supplemental', 'supplement', 'supplements', 'supplemented']
    wordList2 = ['annual']
    wordList3 = ['update', 'updates', 'updating', 'updated']
    for word in text.split():
        word = word.lower()
        if len([word for s in wordList1 if s in word]) > 0:
            specialDict['supplement'] += 1
        elif len([word for s in wordList2 if s in word]) > 0:
            specialDict['annual'] += 1
        elif len([word for s in wordList3 if s in word]) > 0:
            specialDict['update'] += 1
    return specialDict
    # return json.dumps(specialDict)

def clean(riskFactorString):
   riskFactorString = riskFactorString.replace('Item 1B', ' ').replace ('font',' ').replace ('Staff Comments',' ').replace ('Item 1A',' ').replace ('Table of Contents', ' ').replace('Unresolved Staff Comments', ' ').replace ('Pagebreak', ' ').replace ('END LOGICAL PAGE', ' ').replace('BEGIN LOGICAL PAGE', ' ').replace('also', ' ').replace('will', ' ').replace('may', ' ').replace('FOLIO', ' ').replace('SEQ', ' ').replace('Not Applicable', ' ').strip()
   return riskFactorString

if __name__ == '__main__':
    dirPath = './10Qdownloadtemp/'
    # requirement 0
    filenames = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]
    # requirement 2
    sizes = [getSize(dirPath + f) for f in filenames]

    # get content of each file
    texts = [clean(open(dirPath + f, 'r').read()) for f in filenames]
    wordCounts = []
    complexities = []
    lexDiversities = []
    uniques = []
    readabilities = []
    specialCount = []
    req8 = []
    for text in texts:
        # requirement 1
        wordCounts.append(textstat.lexicon_count(text))
        # requirement 3
        complexities.append(getComplexity(text))
        # requirement 4
        lexDiversities.append(lexical_diversity(text))
        # requirement 5
        uniques.append(len(np.unique(text.split())))
        # requirement 6
        readabilities.append(textstat.gunning_fog(text))
        # requirement 7
        specialCount.append(countSpecial(text))
        # requirement 8
        if wordCounts[-1] > 3 and wordCounts[-1] < 150:
            req8.append(text.split()[:30])
            # if any("Not" in s for s in req8[-1]):
            #     print text
        else:
            req8.append([])
    # print len(filenames)
    # print len(wordCounts)
    # print len(sizes)
    # print len(complexities)
    # print len(lexDiversities)
    # print len(uniques)
    # print len(readabilities)
    # print len(specialCount)
    # print len(req8)
    df = pd.DataFrame(np.array([filenames, wordCounts, sizes, complexities, lexDiversities, uniques, readabilities, specialCount, req8]).T, columns=['filenames', 'wordCounts', 'sizes', 'complexities', 'lexDiversities', 'uniques', 'readabilities', 'specialCount', 'req8'])

    df.to_csv('output.csv', index=False)
