from __future__ import absolute_import, division, print_function
import numpy as np
from scipy import linalg
from scipy.sparse import csr_matrix
import time
import math
import sys

class ImportanceScoresHelperLsgkm(object):
    def __init__(self, support_vectors, gamma, alphas):
        self.gamma = gamma
	self.alphas = alphas
	self.support_vectors = support_vectors
	self.refcount = 0

    def get_analytic_gradient(self, testpoint):
        per_coordinate_differences = (self.support_vectors
                                      - testpoint[None, :])
        common_term_per_sv = (self.alphas
                              * 2.0
                              * self.gamma
                              * np.exp(
            -1.0 * self.gamma *
            np.sum(
                np.square(per_coordinate_differences),
                axis=1)))
        return np.sum(
            per_coordinate_differences
            * common_term_per_sv[:, None], axis=0)

    def get_average_gradient_between_two_points(self, frompoint, topoint, numsteps):
        self.refcount += 1
        if (self.refcount % 1 == 0):
            print("Starting average gradient calculation for ", self.refcount, "th point")
        distance = linalg.norm(topoint - frompoint)
        unit = (topoint - frompoint) / distance
        waypoints = np.linspace(0, distance, numsteps)
        return np.average([self.get_analytic_gradient(frompoint + waypoints[i] * unit) for i in range(numsteps)],
                          axis=0)

    def get_average_gradient_between_points(self, frompoints, topoints, numsteps):
        start = time.time()
        self.refcount = 0
        to_return = np.array([self.get_average_gradient_between_two_points(
            frompoint=x, topoint=y, numsteps=numsteps)
            for x, y in zip(frompoints, topoints)])
        print("Avg grad computed in:", round(time.time() - start, 2), "s")
        return to_return

    def get_feature_contribs_using_average_gradient_from_reference(self, testpoints, reference_points, numsteps):
        assert (np.isfinite(testpoints).all()), "Some of the training points are not finite!"
        assert (np.isfinite(reference_points).all()), "Some of the obtained reference points are not finite!"
        avg_gradients = self.get_average_gradient_between_points(frompoints=reference_points, topoints=testpoints, numsteps=numsteps)
        contribs = (testpoints - reference_points) * avg_gradients
        return contribs, avg_gradients
