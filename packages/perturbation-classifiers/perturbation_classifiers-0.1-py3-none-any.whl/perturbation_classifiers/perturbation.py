# coding=utf-8

# Author: Rodolfo J. O. Soares <rodolfoj.soares@gmail.com>

import numpy as np

def perturbation_mean(mean_vectors):
    """Compute the perturbation based on mean vectors.

    Parameters
    ----------
    mean_vectors : array of shape (n_classes, n_features)
                   The mean vectors for each class.

    Returns
    -------
    perturbations : array of shape (n_classes, )
                    Perturbation estimates for each class.
    """
    ndim = mean_vectors.ndim - 1

    return np.linalg.norm(mean_vectors, axis=ndim)


def perturbation_covariance(covariances_matrix):
    """Compute the perturbation based on covariances matrix

    Parameters
    ----------
    covariances_matrix : array of shape (n_classes, n_features, n_features)
                         The covariances matrix for each class.

    Returns
    -------
    perturbations: array of shape (n_classes, )
                   Perturbation estimates for each class.
    """
    ndim_x = covariances_matrix.ndim - 2
    ndim_y = covariances_matrix.ndim - 1

    return np.linalg.norm(covariances_matrix, 'fro', axis=(ndim_x, ndim_y))

def perturbation_combination(X, mean_vectors, inverse_covariances_matrix, delta_mean_vectors, delta_covariances_matrix):
    """Compute the perturbation based on combination of mean vectors and covariances matrix

    Parameters
    ----------
    X : array of shape (n_samples, n_features)
        The input data.
    
    mean_vectors : array of shape (n_classes, n_features)
                   The mean vectors for each class.
    
    inverse_covariances_matrix : array of shape (n_classes, n_features, n_features)
                                 The pseudo-inverse of covariances matrix for each class.
    
    delta_mean_vectors : array of shape (n_classes, n_features)
                         The new mean vectors for each class after insertion of test samples.
    
    delta_covariances_matrix : array of shape (n_classes, n_features, n_features)
                               The new covariances matrix for each class after insertion of test samples.

    Returns
    -------
    perturbations: array of shape (n_classes, )
                   Perturbation estimates for each class.
    """
    
    # Compute the difference between each test instance and each mean of the class
    difference_means = list(
        map(lambda x: list(
            map(lambda m: (x - m).reshape(len(x), 1), mean_vectors)
        ), X)
    )

    # Compute the expression for the means
    combinations_perturbations_means = list(
        map(lambda x, d_means: list(
            map(lambda inv, d_mean: np.dot((-2 * inv), d_mean).T, inverse_covariances_matrix, d_means)
        ), X, difference_means)
    )

    # Compute the multiplication between perturbation mean of each class and its values calculate before
    combinations_perturbations_means = list(
        map(lambda perts, means: list(
            map(lambda per, m: np.dot(m, per), perts, means)
        ), delta_mean_vectors, combinations_perturbations_means)
    )

    combinations_perturbations_means = np.array(
        list(
            map(np.concatenate, combinations_perturbations_means)
        )
    )

    # Compute the expression for the covariance matrix.
    combinations_perturbations_covariances = list(
        map(lambda d_means: list(
            map(lambda d_mean, inv: (inv - np.dot(np.dot(np.dot(inv, d_mean), d_mean.T), inv)), d_means, inverse_covariances_matrix)
        ), difference_means)
    )

    # Compute the multiplication between the value calculate before and its perturbation covariance.
    combinations_perturbations_covariances = list(
        map(lambda perts, covs: list(
            map(lambda per, cov: np.dot(per, cov), perts, covs)
        ), delta_covariances_matrix, combinations_perturbations_covariances)
    )

    # Compute trace of each result matrix calculate before
    combinations_perturbations_covariances = list(
        map(lambda perts: list(
            map(np.matrix.trace, perts)
        ), combinations_perturbations_covariances)
    )

    combinations_perturbations_covariances = np.array(combinations_perturbations_covariances)

    # Compute the combination perturbation for each class
    combinations_perturbations = list(
        map(lambda means, covs: means + covs, combinations_perturbations_means, combinations_perturbations_covariances)
    )

    # Compute Absolute value
    norms = np.array(
        list(
            map(lambda perts: list(
                map(np.fabs, perts)
            ), combinations_perturbations)
        )
    )

    return norms

