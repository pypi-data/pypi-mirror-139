# coding=utf-8

# Author: Rodolfo J. O. Soares <rodolfoj.soares@gmail.com>

import numpy as np
from abc import abstractmethod, ABCMeta

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.metrics import accuracy_score

from perturbation_classifiers.util.prob_function import softmin

class BasePerC(BaseEstimator, ClassifierMixin):
    """Base class for Perturbation-based Classifier (PerC) and
       subconcept Perturbation-based Classifier (sPerC) methods.

    Warning: This class should not be used directly.
    Use derived classes instead.

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, mode="auto"):
        self.mode = mode
    
    @abstractmethod
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
        # Check that X and y have correct shape
        X, y = check_X_y(X, y)
    
    def predict(self, X):
        """Predict the class label for each sample in X.

        Parameters
        ----------
        X : array of shape (n_samples, n_features)
            The input data.

        Returns
        -------
        predicted_labels : array of shape (n_samples, )
                           Predicted class label for each sample in X.
        """
        # Check is fit had been called
        check_is_fitted(self, "classes_")

        # Input validation
        X = check_array(X)

        # Compute the perturbation of each class
        perturbations = self.perturbation(X)

        # Predict the class label for each sample query
        idx = perturbations.argmin(axis=1)
        return self.classes_[idx]
    
    @abstractmethod
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
        # Check is fit had been called
        check_is_fitted(self, "classes_")

        # Input validation
        X = check_array(X)
    
    def score(self, X, y):
        """Return the accuracy on the given test data and labels.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input data.

        y : array-like of shape (n_samples, )
            class labels of each example in X.

        Returns
        -------
        score: float
               accuracy of self.predict(X)
        """

        # Compute the prediction of X set
        y_pred = self.predict(X)
        return accuracy_score(y, y_pred)
    
    def predict_proba(self, X):
        """Estimates the posterior probabilities for sample in X.

        Parameters
        ----------
        X : array of shape (n_samples, n_features)
            The input data.

        Returns
        -------
        predicted_proba : array of shape (n_samples, n_classes)
                          Probabilities estimates for each sample in X.
        """
        # Compute perturbation of each class
        perturbations = self.perturbation(X)
        return softmin(perturbations)
    
    @abstractmethod
    def __validate_parameters(self):
        """Verify if the input parameters are correct.
        """
        pass