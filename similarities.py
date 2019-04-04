import sys
import numpy
import fastText
from numpy import inner
from numpy.linalg import norm
from nltk.corpus import stopwords 
import math

# Sorensen–Dice coefficient
# dice(t1,t2) = (2 * |(t1 and t2)|) / (|t1| + |t2|)
class DiceNGramSimilarity:
    def __init__(self,ngram =3):
        self.ngram = ngram
    def similarity(self, segment1, segment2):
        threegrams = NGrams()
        threegrams_t1 = threegrams.findNgrams(segment1,self.ngram)
        threegrams_t2 = threegrams.findNgrams(segment2,self.ngram)
        commonelements = len(threegrams_t1.intersection(threegrams_t2))
        return (2 * commonelements) / (len(threegrams_t1) + len(threegrams_t2))
    def getName(self):
        return type(self).__name__+str(self.ngram)

# Jaccard coefficient
class JaccardWordSimilarity:
    def __init__(self,ngram =3):
        self.ngram = ngram
    def similarity(self, segment1, segment2):
        if len(segment1) ==0 or len(segment2)==0:
            return 0.0
        threegrams_t1 = set(segment1.split())
        threegrams_t2 = set(segment2.split())
        if len(threegrams_t1)==0 or len(threegrams_t2)==0:
            return 0.0
        size_intersection = len(threegrams_t1.intersection(threegrams_t2))
        size_union = len(threegrams_t1.union(threegrams_t2))
        return size_intersection / size_union
    def getName(self):
        return type(self).__name__+str(self.ngram)
# jaccard(t1, t1) = |(t1 and t2)| / |(t1 or t2)|
class JaccardNGramSimilarity:
    def __init__(self,ngram =3):
        self.ngram = ngram
    def similarity(self, segment1, segment2):
        if len(segment1) ==0 or len(segment2)==0:
            return 0.0
        threegrams = NGrams()
        threegrams_t1 = threegrams.findNgrams(segment1,self.ngram)
        threegrams_t2 = threegrams.findNgrams(segment2,self.ngram)
        if len(threegrams_t1)==0 or len(threegrams_t2)==0:
            return 0.0
        size_intersection = len(threegrams_t1.intersection(threegrams_t2))
        size_union = len(threegrams_t1.union(threegrams_t2))
        return size_intersection / size_union
    def getName(self):
        return type(self).__name__+str(self.ngram)


class CosineEmbeddings:
    def __init__(self,embedding_file,num_embeddings):
        sys.stderr.write("Loading Embeddings: %d\n"%num_embeddings)
        self.model = fastText.load_model(embedding_file)
        self.num_embeddings = num_embeddings
        self.stopwords = set(stopwords.words('english'))
    def similarity(self, segment1, segment2):
        centroid1 = self.getCentroid(segment1)
        centroid2 = self.getCentroid(segment2)
        return inner(centroid1, centroid2) / (norm(centroid1) * norm(centroid2))
    def sigmoid(self,x):
        return 1 / (1 + numpy.exp(-x))
    def getCentroid(self, segment):
        wordVectors = []
        for line in segment.split('\n'):
            for word in line.split(' '):
                if word in self.stopwords:
                    continue
                wordVectors.append(self.model.get_word_vector(word))
        mean =  numpy.mean(wordVectors, axis=0)
        #mean = self.sigmoid(mean)
        return (mean).tolist()
    def getName(self):
        return type(self).__name__ +str(self.num_embeddings)

class NGrams:
    # extract three-grams from lines of a text segment: lines separated by '\n'
    def findNgrams(self, text, n = 3):
        threegrams = set()
        for line in text.split('\n'):
            for i in range(len(line) - (n-1)):
                if line[i:i + n] not in threegrams:
                    threegrams.add(str(line[i:i + n]))
        return threegrams
