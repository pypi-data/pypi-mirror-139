"""A Python library for perturbation-based classifiers.

``Perturbation Classifier`` is a library containing the implementation of the Perturbation-based
Classifier (PerC) and subconcept Perturbation-based Classifier (sPerC). 

Subpackages
-----------
subconcept
    The implementation of subconcept Perturbation-based Classifier (sPerC).
util
    The implementation of probability function and load keel dataset format. 
"""

from perturbation_classifiers.perc import PerC

# list of all modules available in the library
__all__ = ['PerC', 'subconcept', 'util']

__version__ = '0.1.dev'