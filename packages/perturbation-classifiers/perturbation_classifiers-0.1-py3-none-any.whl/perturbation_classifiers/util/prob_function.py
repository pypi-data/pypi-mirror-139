# coding=utf-8

# Author: Rodolfo J. O. Soares <rodolfoj.soares@gmail.com>

import numpy as np

def softmax(vector, theta=1.0):
    """Takes an vector w of S N-element and returns a vectors where each column
    of the vector sums to 1, with elements exponentially proportional to the
    respective elements in N.

    Parameters
    ----------
    vector : array of shape = [N,  M]
        
    theta : float (default = 1.0)
            used as a multiplier  prior to exponentiation

    Returns
    -------
    dist : array of shape = [N, M]
           Which the sum of each row sums to 1 and the elements are exponentially
           proportional to the respective elements in N
    """
    
    w = np.atleast_2d(vector)
    e = np.exp(np.array(w) / theta)
    dist = e / np.sum(e, axis=1).reshape(-1, 1)
    return dist

def softmin(vector):
    """Takes a vector w of S N-element and return a softmax-based activation function 
    that is defined as f(x)=softmax(−x).

    Parameters
    ----------
    vector : array of shape = [N,  M]

    Returns
    -------
    dist : array of shape = [N, M]
           Which the sum of each row sums to 1 and the elements are exponentially
           proportional to the respective elements in N
    """

    return softmax((-1 * vector))