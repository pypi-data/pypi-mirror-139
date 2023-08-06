# coding=utf-8

# Author: Rodolfo J. O. Soares <rodolfoj.soares@gmail.com>

import numpy as np

def estimate_mean_vector_per_class(X, y, unique_classes, count_classes):
    """Estimate the mean vector for each class

    Parameters
    ----------
    X : array of shape (n_samples, n_features)
        The input data.

    y : array of shape (n_samples, )
        class labels of each example in X.

    unique_classes : array of shape (n_classes,)
                     The unique class labels 

    count_classes : array of shape (n_classes, )
                    The number of times each of the unique class labels comes up in the database

    Returns
    -------
    mean_vectors: array of shape (n_classes, n_features)
                  The mean vectors for each class
    """

    # Get the data belongs to each class
    instance_classes = list(
        map(lambda w: X[y == w], unique_classes)
    )

    # Compute the data mean of each class
    mean_vectors = list(
        map(lambda x, c: x.sum(axis=0) / c, instance_classes, count_classes)
    )
    
    return np.array(mean_vectors)   


def estimate_delta_mean_vector_per_class(X, mean_vectors, count_classes):
    """Estimate the mean vector for each class after insertion of samples

    Parameters
    ----------
    X : array of shape (n_samples, n_features)
        The input data.
    
    mean_vectors : array of shape (n_classes, n_features)
                   The mean vectors for each class.
    
    count_classes : array of shape (n_classes, )
                    The number of times each of the unique class labels comes up in the database

    Returns
    -------
    new_mean_vectors: array of shape (n_classes, n_features)
                      The new mean vectors for each class after insertion of test samples.
    """

    # Compute the mean vector after simulation insert the sample query 
    delta_mean_vectors = list(
        map(lambda x: (x - mean_vectors) / (count_classes[:, np.newaxis] + 1), X)
    )

    return np.array(delta_mean_vectors)


def estimate_covariance_matrix_per_class(X, y, unique_classes, count_classes, mean_vectors):
    """Estimate the covariance matrix for each class

    Parameters
    ----------
    X : array of shape (n_samples, n_features)
        The input data.

    y : array of shape (n_samples)
        class labels of each example in X.

    unique_classes : array of shape (n_classes,)
                     The unique class labels .

    count_classes : array of shape (n_classes, )
                    The number of times each of the unique class labels comes up in the database.
    
    mean_vectors : array of shape (n_classes, n_features)
                   The mean vector for each class.

    Returns
    -------
    covariance_matrix: array of shape (n_classes, n_features, n_features)
                       The covariance matrix for each class.
    """

    covariances_matrix = np.zeros((unique_classes.shape[0], X.shape[1], X.shape[1]), dtype=np.float_)
    for i, (w, c) in enumerate(zip(unique_classes, count_classes)):

        # Get data point belongs to each class
        data_per_class = X[y == w]

        # Get the mean of the class
        mean = mean_vectors[i]

        # Compute the covariance matrix belongs to each class
        data_mean_diff = (data_per_class - mean)
        data_covariance = np.dot(data_mean_diff.T, data_mean_diff) / c
        covariances_matrix[i] = data_covariance

    return np.asarray(covariances_matrix)


def estimate_delta_covariance_matrix_per_class(X, mean_vectors, covariances_matrix, count_classes):
    """Estimate the covariance matrix for each class after insertion of samples

    Parameters
    ----------
    X : array of shape (n_samples, n_features)
        The input data.
    
    mean_vectors : array of shape (n_classes, n_features)
                   The mean vector for each class.
    
    covariances_matrix : array of shape (n_classes, n_features, n_features)
                         The covariance matrix for each class.
    
    count_classes : array of shape (n_classes, )
                    The number of times each of the unique class labels comes up in the database.

    Returns
    -------
    new_covariance_matrix: array of shape (n_classes, n_features, n_features)
                           The new covariance matrix for each class after insertion of test samples.
    """

    # Compute difference between each test instance and each mean of the class
    X_diff_mean = list(
        map(lambda x: list(
            map(lambda m: (x - m).reshape(len(x), 1), mean_vectors)
        ), X)
    )

    # Compute the delta covariance matrix of each class
    delta_covariances_matrix = list(
        map(lambda perts: list(
            map(lambda per, n: np.dot(per, per.T) / (n + 1), perts, count_classes)
        ), X_diff_mean)
    )

    delta_covariances_matrix = list(
        map(lambda perts: list(
            map(lambda cov, per, n: ((-(cov / n)) + per), covariances_matrix, perts, count_classes)
        ), delta_covariances_matrix)
    )

    return np.array(delta_covariances_matrix)

