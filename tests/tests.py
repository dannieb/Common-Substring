from highlights import Highlights
from nltk.stem.porter import PorterStemmer
import csv
import os
import unittest


class Test(unittest.TestCase):
    STEMMER = PorterStemmer()

    def test_convertToFLoat(self):
        highlights = Highlights()
        features = highlights._getFeatures("abc DEFG. higjk, lmn,o p can't do it and you know you won't")
        
        self.assertTrue(len(features) == 12)
        self.assertTrue(features[0] == "abc")
        self.assertTrue(features[1] == "defg")
        self.assertTrue(features[2] == "higjk")
        self.assertTrue(features[3] == "lmno")
        self.assertTrue(features[4] == "can't")
        self.assertTrue(features[5] == "do")
        self.assertTrue(features[6] == "it")
        self.assertTrue(features[7] == "and")
        self.assertTrue(features[8] == "you")
        self.assertTrue(features[9] == "know")
    
            
            
    def testHighlighting(self):
        
        highlighter = Highlights()
        highlighter.addCorpus("once upon a time was great people")
        phrases = highlighter.getTopWords(numWords=1, num=5)
        self.assertTrue(len(phrases) == 0 )
        
        
        highlighter.addCorpus("There once was a cow named joe great people")
        phrases = highlighter.getTopWords(numWords=1, num=5)
        print phrases
        self.assertTrue(len(phrases) == 5)
        self.assertTrue(phrases[0] == self.STEMMER.stem("once"))
        self.assertTrue(phrases[1] == self.STEMMER.stem("great"))
        self.assertTrue(phrases[2] == self.__getHighlightSequence([self.STEMMER.stem("great"), self.STEMMER.stem("people")]))
        self.assertTrue(phrases[3] == self.STEMMER.stem("was"))
        self.assertTrue(phrases[4] == self.STEMMER.stem("people"))
        
        
        highlighter.addCorpus("Joe was a funny man but he really liked using Groupon because of the Customer  service with great people")
        phrases = highlighter.getTopWords(numWords=1, num=5)
        print phrases
        self.assertTrue(len(phrases) == 5)
        self.assertTrue(phrases[0] == self.STEMMER.stem("great"))
        self.assertTrue(phrases[1] == self.STEMMER.stem("was"))
        self.assertTrue(phrases[2] == self.__getHighlightSequence([self.STEMMER.stem("great"), self.STEMMER.stem("people")]))
        self.assertTrue(phrases[3] == self.STEMMER.stem("people"))
        self.assertTrue(phrases[4] == self.STEMMER.stem("once"))
        
        
        highlighter.addCorpus("Groupon's customer service was fantastic!")
        phrases = highlighter.getTopWords(numWords=1, num=5)
        print phrases
        self.assertTrue(len(phrases) == 5)
        self.assertTrue(phrases[0] == self.STEMMER.stem("was"))
        self.assertTrue(phrases[1] == self.STEMMER.stem("great"))
        self.assertTrue(phrases[2] == self.__getHighlightSequence([self.STEMMER.stem("great"), self.STEMMER.stem("people")]))
        self.assertTrue(phrases[3] == self.STEMMER.stem("people"))
        self.assertTrue(phrases[4] == self.STEMMER.stem("once"))
        
        
        phrases = highlighter.getTopWords(numWords=2, num=5)
        print phrases
        self.assertTrue(len(phrases) == 2)
        self.assertTrue(phrases[0] == self.__getHighlightSequence([self.STEMMER.stem("great"), self.STEMMER.stem("people")]))
        self.assertTrue(phrases[1] == self.__getHighlightSequence([self.STEMMER.stem("customer"), self.STEMMER.stem("service")]))
        
        
        
    
    def test_aHighlightingLS(self):
        highlighter = Highlights()
        for corpus in self.__getCorpusList(os.path.join(os.path.dirname(__file__), "yelp-beijing-restaurant.csv")) :
            highlighter.addCorpus(corpus)
        
        print highlighter.getTopWords(numWords=3, num=50)
        print highlighter.getTopWords(numWords=4, num=50)
        print "----------------------------------------"
        
        
    #private helper functions
    def __getHighlightSequence(self, strs):
        return "|".join(strs)
        
        
    def __getCorpusList(self, fileName):
        corpa = []
        with open(fileName, "r") as fd :
            reader = csv.reader(fd)
            for row in reader :
                corpa.append(row[0])
                
        return corpa
