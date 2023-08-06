# coding=utf-8

# Author: Rodolfo J. O. Soares <rodolfoj.soares@gmail.com>

from sklearn.metrics.pairwise import euclidean_distances
import numpy as np


def min_rule(perturbations, cluster2class):
    """Compute the minimum perturbation for each sample based on classes's clusters

    Parameters
    ----------
    perturbations : array of shape (n_samples, n_clusters)
                    The cluster estimated perturbation for each sample.
    
    cluster2class : dict
                    The mapped cluster to class.

    Returns
    -------
    perturbations: array of shape (n_samples, n_classes)
                   The minimum perturbation for each sample.
    """
    classes = np.array(list(cluster2class.values()))

    perturbations_min = np.full((perturbations.shape[0], len(set(classes))), np.inf)

    for i, c in enumerate(set(classes)):
        perturbations_min[:, i] = np.min(perturbations[:, (classes == c)], axis=1)

    return perturbations_min

def avg_rule(perturbations, cluster2class):
    """Compute the average perturbation for each sample based on classes's clusters

    Parameters
    ----------
    perturbations : array of shape (n_samples, n_clusters)
                    The cluster estimated perturbation for each sample.
    
    cluster2class : dict
                    The mapped cluster to class.

    Returns
    -------
    perturbations: array of shape (n_samples, n_classes)
                   The minimum perturbation for each sample.
    """
    classes = np.array(list(cluster2class.values()))

    perturbations_mean = np.full((perturbations.shape[0], len(set(classes))), np.inf)

    for i, c in enumerate(set(classes)):
        perturbations_mean[:, i] = np.mean(perturbations[:, (classes == c)], axis=1)

    return perturbations_mean

def median_rule(perturbations, cluster2class):
    """Compute the median perturbation for each sample based on classes's clusters

    Parameters
    ----------
    perturbations : array of shape (n_samples, n_clusters)
                    The cluster estimated perturbation for each sample.
    
    cluster2class : dict
                    The mapped cluster to class.

    Returns
    -------
    perturbations: array of shape (n_samples, n_classes)
                   The minimum perturbation for each sample.
    """
    classes = np.array(list(cluster2class.values()))

    perturbations_median = np.full((perturbations.shape[0], len(set(classes))), np.inf)

    for i, c in enumerate(set(classes)):
        perturbations_median[:, i] = np.median(perturbations[:, (classes == c)], axis=1)

    return perturbations_median

def nearest_cluster_rule(X, perturbations, cluster2class, centroids):
    """Compute the perturbation for each sample based on nearest centroids

    Parameters
    ----------
    X : array of shape (n_samples, n_features)
        The input data.

    perturbations : array of shape (n_samples, n_clusters)
                    The cluster estimated perturbation for each sample.

    cluster2class : dict
                    The mapped cluster to class.
    
    centroids : array of shape (n_clusters, n_features)
                The centroid for each cluster.

    Returns
    -------
    perturbations: array of shape (n_samples, n_classes)
                   The minimum perturbation for each sample.
    """
    classes = np.array(list(cluster2class.values()))

    perturbations_nearest_cluster = np.full((perturbations.shape[0], len(set(classes))), np.inf)

    for i, c in enumerate(set(classes)):
        class_centers_ = centroids[(classes == c), :]

        dists = euclidean_distances(X, class_centers_)
        nearest_clusters_idx = dists.argmin(axis=1)

        perturbation_clusters = perturbations[:, (classes == c)]
        for j, p in enumerate(nearest_clusters_idx):
            perturbations_nearest_cluster[j, i] = perturbation_clusters[j, p]

    return perturbations_nearest_cluster
