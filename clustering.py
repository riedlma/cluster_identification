from sklearn.cluster import SpectralClustering as SKLSK
import numpy as np
# SKLSK = sklearn spectral clustering (we reuse the name SpectralClustering)

# run SKLSK on a precomputed affinity matrix
# input: n x n square similarity matrix (np.array)
# output: a 1-dimensional np.array, length n, with cluster labels (int32)
class SpectralClustering:
    def __init__(self, use_fix_random =False):
        self.use_fix_random = use_fix_random
    def cluster(self, num_clusters,matrix):
        if not self.use_fix_random:
                clusters = SKLSK(n_clusters=num_clusters,affinity='precomputed').fit_predict(matrix)
        else:
                clusters = SKLSK(n_clusters=num_clusters,affinity='precomputed',random_state=0).fit_predict(matrix)
        return clusters
	
# run SKLSK on a precomputed affinity matrix, exponentiated (with seems to
# give much better results for reasons I don't really understand)
# input: n x n square similarity matrix (np.array)
# output: a 1-dimensional np.array, length n, with cluster labels (int32)
class SpectralExponentialClustering:
    def __init__(self, use_fix_random = False):
        self.use_fix_random = use_fix_random
    def cluster(self, num_clusters,matrix):
        if not self.use_fix_random:
            clusters = SKLSK(n_clusters=num_clusters,affinity='precomputed').fit_predict(np.exp(matrix))
        else:
            clusters = SKLSK(n_clusters=num_clusters,affinity='precomputed',random_state=0).fit_predict(np.exp(matrix))
        return clusters

        

# test method for this module
def testClustering():
        clusterer = SpectralExponentialClustering()
        X = np.array([[1,0.1,0,0.9],
                      [0.1,1,0,0],
                      [0,0,1,0.8],
                      [0.9,0,0.8,1]])
        print(clusterer.cluster(2,X))
        print(clusterer.cluster(3,X))

if __name__ == "__main__":
    testClustering()
