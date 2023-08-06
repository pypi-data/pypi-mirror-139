# coding=utf-8

# Author: Rodolfo J. O. Soares <rodolfoj.soares@gmail.com>

from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
from gap_statistic import OptimalK
import numpy as np

def best_k_calinsk_harabasz(X, kmeans_algorithms):
    """Find the best k-value for KMeans algorithms 
       based on calinsk-harabasz (ch) method.

    Parameters
    ----------
    X : array of shape (n_samples, n_features)
        The input data.
    
    kmeans_algorithms : list of sklearn.cluster.KMeans
                        List of KMeans algorithm to be evaluated

    Returns
    -------
    best_k_means: sklearn.cluster.KMeans
                  The best KMeans according to calinsk-harabasz method.
    """
    size = len(kmeans_algorithms)
    scores = np.zeros(size, dtype=np.float_)

    for i, kmeans in enumerate(kmeans_algorithms):
        labels = kmeans.labels_
        ch_score = calinski_harabasz_score(X, labels)
        scores[i] = ch_score

    idx = scores.argmax()
    return kmeans_algorithms[idx]


def best_k_davies_bouldin(X, kmeans_algorithms):
    """Find the best k-value for KMeans algorithms 
       based on davies-bouldin (db) method.

    Parameters
    ----------
    X : array of shape (n_samples, n_features)
        The input data.
    
    kmeans_algorithms : list of sklearn.cluster.KMeans
                        List of KMeans algorithm to be evaluated

    Returns
    -------
    best_k_means: sklearn.cluster.KMeans
                  The best KMeans according to davies-bouldin method.
    """
    size = len(kmeans_algorithms)
    scores = np.zeros(size, dtype=np.float_)

    for i, kmeans in enumerate(kmeans_algorithms):
        labels = kmeans.labels_
        db_score = davies_bouldin_score(X, labels)
        scores[i] = db_score

    idx = scores.argmin()
    return kmeans_algorithms[idx]


def best_k_gap_statistic(X, kmeans_algorithms, n_refs):
    """Find the best k-value for KMeans algorithms 
       based on Gap Statistic (gap) method.

    Parameters
    ----------
    X : array of shape (n_samples, n_features)
        The input data.
    
    kmeans_algorithms : list of sklearn.cluster.KMeans
                        List of KMeans algorithm to be evaluated.
    
    n_refs : int
             Number of random reference data sets used as inertia reference to actual data.

    Returns
    -------
    best_k_means: sklearn.cluster.KMeans
                  The best KMeans according to gap statistic method.
    """

    k_values = []
    for kmeans in kmeans_algorithms:
        k_value = kmeans.cluster_centers_.shape[0]
        k_values.append(k_value)

    min_k = min(k_values)
    max_k = max(k_values)

    optimalK = OptimalK(parallel_backend='rust')
    k_best = optimalK(X, n_refs=n_refs, cluster_array=np.arange(min_k, (max_k + 1)))

    idx = k_values.index(k_best)
    return kmeans_algorithms[idx]


def best_k_silhouette(X, kmeans_algorithms):
    """Find the best k-value for KMeans algorithms 
       based on silhouette (sil) method.

    Parameters
    ----------
    X : array of shape (n_samples, n_features)
        The input data.
    
    kmeans_algorithms : list of sklearn.cluster.KMeans
                        List of KMeans algorithm to be evaluated

    Returns
    -------
    best_k_means: sklearn.cluster.KMeans
                  The best KMeans according to silhouette method.
    """
    size = len(kmeans_algorithms)
    scores = np.zeros(size, dtype=np.float_)

    for i, kmeans in enumerate(kmeans_algorithms):
        labels = kmeans.labels_
        sil_score = silhouette_score(X, labels)
        scores[i] = sil_score

    idx = scores.argmax()
    return kmeans_algorithms[idx]

