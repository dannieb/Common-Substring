'''
Created on Sep 13, 2011

@author: dannie
'''
from nltk.probability import FreqDist
from nltk.stem.porter import PorterStemmer
from nltk.tokenize.treebank import TreebankWordTokenizer
import re
import unittest

'''
Allows you to find the common phrases in a list of large texts.
The approach taken is brute force with optimizations.
Worst Case Runtime: O(N * M^2)
where : N = number of texts
        M = Number of words in the largest text
        
Hook this up to a text classifier to filter out meaningless common texts 
and you get something like yelps review highlights
'''
class Highlights(object):
    highlightCache = {}
    featureLists = []
    
    def __init__(self):
        self.featureLists = []
        self.highlightCache = {}
       
       
    '''
        Default Logic for feature extraction:
        retrieves the features from a corpus.
        converts all words to their stemmed versions, lowercases and strips out all non letter and digit
        characters less than 2 characters long.
    ''' 
    def _getFeatures(self, corpus):
        stemmer = PorterStemmer()
        tokens = corpus.split(" ")
        features = filter(lambda x: len(x) > 1, tokens)
        
        finalList = [] 
        for feature in features :
            feature = re.sub("[^a-zA-Z0-9']", "", feature.lower())
            finalList.append(stemmer.stem_word(feature))
            
        return finalList
        
    '''
    Adding a text corpus will appends the new common phrase counts
    '''
    def addCorpus(self, corpus):
        #The features of the new corpus
        addedFeatures = self._getFeatures(corpus)
        
        #tokenize the text
        for features in self.featureLists :
            self.analyze(features, addedFeatures)
            
        self.featureLists.append(addedFeatures)
        
        
    '''
    Accepts two sets of features and looks up the common occuring substrings and increments the common phrase counts
    '''    
    def analyze(self, features, newFeatures):
        posMap = {}
        for x in xrange(len(newFeatures)) :
            feature = newFeatures[x]
            if not posMap.get(feature) :
                posMap[feature] = [x]
            else :
                posMap[feature].append(x)

            
        phrases = {}
        for x in xrange(len(features)) :
            matchedPhrases = self.__getMatchedPhrases(features[x:], posMap)
            for phrase in matchedPhrases :
                phrases[phrase] = 1
        
        for phrase in phrases.keys() :
            self.highlightCache[phrase] = self.highlightCache[phrase] + 1 if self.highlightCache.get(phrase) else 1
                
            
    '''
    Given a starting point for the words, updates the common phrase counts
    '''
    def __getMatchedPhrases(self, features, posMap):
        matchedPhrases = {}
        matches = posMap.get(features[0], [])
        if matches :
            matchedPhrases[features[0]] = 1
            
        #We see how many matches exist for the feature.  For each match, try to
        #match even further
        for match in matches :
            x = 1
            while x < len(features) :
                nextPos = posMap.get(features[x])
                if nextPos and (match + x) in nextPos :
                    matchedPhrases["|".join(features[:x+1])] = 1
                    x += 1 
                else :
                    break
                
        
        return matchedPhrases.keys()
    
            
    '''
    Retrieves the top performing phrases.  Order by number of matches across the corpa then by the length of phrase
    @numWords: number of words in the top matching = 1
    @num: for returning the top N where N = num
    '''
    def getTopWords(self, numWords=1, num=1, showCounts=False):
        topWords = []
        
        for key, value in self.highlightCache.items() :
            features = key.split("|")
            if len(features) >= numWords :
                topWords.append((key, value))
                
        topWords.sort(key=lambda x: x[1], reverse=True)
        if showCounts :
            topWords = map(lambda x: x[0], topWords)
        return topWords[:num]
    
    