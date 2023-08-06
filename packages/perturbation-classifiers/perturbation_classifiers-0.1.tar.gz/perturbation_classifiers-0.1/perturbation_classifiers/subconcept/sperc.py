# coding=utf-8

# Author: Rodolfo J. O. Soares <rodolfoj.soares@gmail.com>

import numpy as np

from sklearn.utils.validation import check_random_state
from sklearn.cluster import KMeans

from perturbation_classifiers.base import BasePerC
from perturbation_classifiers.perturbation import perturbation_mean, perturbation_covariance, perturbation_combination
from perturbation_classifiers.estimation import estimate_mean_vector_per_class, estimate_covariance_matrix_per_class, estimate_delta_mean_vector_per_class, estimate_delta_covariance_matrix_per_class
from perturbation_classifiers.subconcept.clustering import best_k_calinsk_harabasz, best_k_davies_bouldin, best_k_gap_statistic, best_k_silhouette, find_small_clusters
from perturbation_classifiers.subconcept.aggregation import min_rule, avg_rule, median_rule, nearest_cluster_rule

class sPerC(BasePerC):
    """subconcept Perturbation-based Classifier (sPerC).
    """

    def __init__(self, mode="auto", aggregation_rule="nearest_cluster", cluster_validation="sil", n_clusters_per_class="auto", alpha=0.1, k_means_iteration=100, n_refs_gap = 100, random_state=None, n_jobs=None):
        super(sPerC, self).__init__(mode = mode)
        self.aggregation_rule = aggregation_rule
        self.cluster_validation = cluster_validation
        self.n_clusters_per_class = n_clusters_per_class
        self.alpha = alpha
        self.k_means_iteration = k_means_iteration
        self.n_refs_gap = n_refs_gap
        self.random_state = random_state
        self.n_jobs = n_jobs

    def fit(self, X, y):
        """Fit the perturbation classifiers according to the given training data.

        Parameters
        ----------
        X : array of shape (n_samples, n_features)
            The input data.
            
        y : array of shape (n_samples, )
            class labels of each example in X.

        Returns
        -------
        self
        """
        super(sPerC, self).fit(X, y)

        self.random_state = check_random_state(self.random_state)

        # Store the classes and its quantity seen during fit
        self.classes_ = np.unique(y)

        # Check that mode paramenters have correct value
        self._validate_parameters()

        self.cluster2class_ = dict()
        self.cluster_centroids_ = np.array([]).reshape(0, X.shape[1])

        # Salve the best k-Means algorith for each class
        bests_k_for_class = dict()
        small_clusters_for_class = dict()

        # Copy X, y input
        X_all, y_all = np.array([]).reshape(0, X.shape[1]), np.array([])

        # Run k-Means and find inner clusters for each class
        for i, w in enumerate(self.classes_):

            X_class_ = X[y == w]

            if self.n_clusters_per_class == "auto":
                k_max = np.ceil(np.sqrt(X_class_.shape[0] * .5))
                k_values = np.arange(2, (k_max + 1)).astype(int)
            else:
                k_values = [self.n_clusters_per_class[i]]
                
            # Define k-Means parameters
            k_means_params = {
                "init": "k-means++",
                "n_init": self.k_means_iteration,
                "max_iter": 300,
                "random_state": self.random_state
            }

            # Clustering data
            kmeans_algorithms = []
            for k in k_values:
                # Run k-Means
                kmeans = KMeans(n_clusters=k, **k_means_params)
                kmeans.fit(X_class_)

                # Storage k-Means object
                kmeans_algorithms.append(kmeans)

            # Internal Validation Index: Calinski-Harabasz
            if self.cluster_validation == "ch":
                best_k = best_k_calinsk_harabasz(X_class_, kmeans_algorithms)
            
            # Internal Validation Index: Davies-Bouldin
            if self.cluster_validation == "db":
                best_k = best_k_davies_bouldin(X_class_, kmeans_algorithms)

            # Internal Validation Index: Gap Statistic
            if self.cluster_validation == "gap":
                best_k = best_k_gap_statistic(X_class_, kmeans_algorithms, self.n_refs_gap)

            # Internal Validation Index: Silhouette
            if self.cluster_validation == "sil":
                best_k = best_k_silhouette(X_class_, kmeans_algorithms)

            # Get centroids calcualte by kmeans
            cluster_centers = best_k.cluster_centers_

            # Remove small clusters
            labels = int(f"{(i+1)}{np.power(10, k_max).astype(int)}") + best_k.labels_
            small_clusters = find_small_clusters(labels, self.alpha)
            
            X_temp = X_class_
            y_temp = labels

            if len(small_clusters) > 0:
                removed_data_idx = np.sum(list(map(lambda sc: labels == sc, small_clusters)), axis=0, dtype=bool)
                removed_centroids_idx = np.sum(list(map(lambda sc: np.unique(labels) == sc, small_clusters)), axis=0, dtype=bool)

                X_temp = np.delete(X_class_, removed_data_idx, axis=0)
                y_temp = np.delete(labels, removed_data_idx)

                cluster_centers = np.delete(cluster_centers, removed_centroids_idx, axis=0)

            X_all = np.concatenate((X_all, X_temp), axis=0)
            y_all = np.concatenate((y_all, y_temp), axis=0)

            self.cluster2class_.update(dict(map(lambda c: (c, w), np.unique(y_temp))))
            self.cluster_centroids_ = np.concatenate((self.cluster_centroids_, cluster_centers), axis=0)

            bests_k_for_class[w] = best_k
            small_clusters_for_class[w] = small_clusters

        self.clusters_, self.count_clusters_ = np.unique(y_all, return_counts=True)
        
        # Compute means vectors for each class
        self.means_ = estimate_mean_vector_per_class(X_all, y_all, self.clusters_, self.count_clusters_)

        # Compute covariances matrix for each class
        if self.mode != "mean":
            self.covariances_ = estimate_covariance_matrix_per_class(X_all, y_all, self.clusters_, self.count_clusters_, self.means_)

        # Compute pseudo-inverse matrix for each covariance matrix
        if self.mode == "auto":
            self.inverse_covariances_ = np.linalg.pinv(self.covariances_)

        return self

    def perturbation(self, X):
        """Return the perturbation for sample in X.

        Parameters
        ----------
        X : array of shape (n_samples, n_features)
            The input data.

        Returns
        -------
        perturbations : array of shape (n_samples, n_classes)
                        Perturbation estimates for each sample in X.
        """
        super(sPerC, self).perturbation(X)

        # Compute perturbation-based the mode input
        perturbations = None

        if self.mode == "mean": 
            # Compute the perturbation-based only mean vector
            delta_mean_vectors = estimate_delta_mean_vector_per_class(X, self.means_, self.count_clusters_)
            perturbations = perturbation_mean(delta_mean_vectors)
        elif self.mode == "covariance": 
            # Compute the perturbation-based only covariance matrix
            delta_covariances_matrix = estimate_delta_covariance_matrix_per_class(X, self.means_, self.covariances_, self.count_clusters_)
            perturbations = perturbation_covariance(delta_covariances_matrix)
        else: 
            # Compute the perturbation-based combination mean vector and covariance matrix
            delta_mean_vectors = estimate_delta_mean_vector_per_class(X, self.means_, self.count_clusters_)
            delta_covariances_matrix = estimate_delta_covariance_matrix_per_class(X, self.means_, self.covariances_, self.count_clusters_)
            perturbations = perturbation_combination(X, self.means_, self.inverse_covariances_, delta_mean_vectors, delta_covariances_matrix)

        # Predict the class label for each sample query
        if self.aggregation_rule == "min":
            perturbations = min_rule(perturbations, self.cluster2class_)
        elif self.aggregation_rule == "avg":
            perturbations = avg_rule(perturbations, self.cluster2class_)
        elif self.aggregation_rule == "median":
            perturbations = median_rule(perturbations, self.cluster2class_)
        else:
            perturbations = nearest_cluster_rule(X, perturbations, self.cluster2class_, self.cluster_centroids_)

        return perturbations
    
    def _validate_parameters(self):
        """Verify if the input parameters are correct.
        """
        # Validate "mode" parameter
        if self.mode not in ["auto", "mean", "covariance"]:
            raise ValueError(
                'Invalid value for parameter "mode".'
                ' "mode" should be one of these options '
                '"auto", "mean", "covariance"'
            )
        
        # Validate "aggregation_rule" parameter
        # TODO: Check when parameter is a pre-defined function
        if isinstance(self.aggregation_rule, str) and self.aggregation_rule not in ["min", "avg", "median", "nearest_cluster"]:
            raise ValueError(
                'Invalid value for parameter "aggregation_rule".'
                ' "aggregation_rule" should be one of these options '
                '"min", "avg", "median", "nearest_cluster" or a callable'
            )
        
        # Validate "cluster_validation" parameter
        # TODO: Check when parameter is a pre-defined function
        if isinstance(self.cluster_validation, str) and self.cluster_validation not in ["ch", "db", "gap", "sil"]:
            raise ValueError(
                'Invalid value for parameter "cluster_validation".'
                ' "cluster_validation" should be one of these options '
                '"ch", "db", "gap", "sil" or a callable'
            )

        # Validate "n_clusters_per_class"
        # TODO: Convert dtype to int into fit method
        if isinstance(self.n_clusters_per_class, str) and self.n_clusters_per_class != "auto":
            raise ValueError(
                'Invalid value for parameter "n_clusters_per_class".'
                ' "n_clusters_per_class" should be one of these options '
                '"auto" or a ndarray'
            )
        elif isinstance(self.n_clusters_per_class, np.ndarray):
            
            param_shape = self.n_clusters_per_class.shape
            input_shape = self.classes_.shape

            if param_shape[0] != input_shape[0]:
                raise ValueError(
                    f'The shape of the parameter "n_clusters_per_class" {param_shape}'
                    f' does not match the number of class {input_shape[0]}.'
                )       
