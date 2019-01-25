from __future__ import absolute_import, division, print_function
import numpy as np
from scipy import sparse
from scipy import linalg
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import time
import math
import sys


class ImportanceScoresHelper(object):
    def __init__(self, svmclassifier, gamma, points, labels, use_csr=False):
        self.clf = svmclassifier
        self.gamma = gamma
        self.points = points
        self.labels = labels
        self.nn_initialized = False
        self.negative_neighbors = None
        self.positive_neighbors = None
        self.negative_indices = None
        self.positive_indices = None
        self.refcount = 0
        self.analyticgradientcount = 0
        self.use_csr = use_csr
        self.csr_support_vectors = csr_matrix(self.clf.support_vectors_)
        print("Support vector shape is " + str(self.clf.support_vectors_.shape))
        self.initialize_reduced_arrays()

    def initialize_reduced_arrays(self):
        self.support_vector_non_zero_indices = self.get_non_zero_column_indices(self.clf.support_vectors_)
        self.non_zero_support_vectors = self.get_non_zero_dense(self.clf.support_vectors_, self.support_vector_non_zero_indices)

    def get_non_zero_column_indices(self, dense_array):
        return np.array(np.nonzero(np.sum(dense_array, axis=0) != 0)).squeeze()

    def get_non_zero_dense(self, dense_array, indices):
        return dense_array[:, indices]

    def initialize_nearest_neigbors(self):
        if not self.nn_initialized:
            self.positive_indices = np.nonzero(self.labels == 1)[0]
            self.negative_indices = np.nonzero(self.labels == 0)[0]
            self.positive_neighbors = NearestNeighbors(n_neighbors=1)
            self.positive_neighbors.fit(self.points[self.positive_indices])
            print("Organized nearest neighbors for ", self.positive_indices.shape[0], " positive points")
            sys.stdout.flush()
            self.negative_neighbors = NearestNeighbors(n_neighbors=1)
            self.negative_neighbors.fit(self.points[self.negative_indices])
            print("Organized nearest neighbors for ", self.negative_indices.shape[0], " negative points")
            sys.stdout.flush()
            self.nn_initialized = True

    def get_closest_opposite_points_using_neighbor_set(self, testpoints, neighbors, indices):
        (dist, ind) = neighbors.kneighbors(testpoints)
        ind = np.squeeze(ind)
        return self.points[indices[ind]]

    def get_closest_opposite_points(self, testpoints):
        self.initialize_nearest_neigbors()
        predictions = self.clf.predict(testpoints)
        pos_pred_ind = np.nonzero(predictions == 1)[0]
        neg_pred_ind = np.nonzero(predictions == 0)[0]
        if len(pos_pred_ind) != 0:
            closest_to_pos = self.get_closest_opposite_points_using_neighbor_set(testpoints[pos_pred_ind],
                                                                                 self.negative_neighbors,
                                                                                 self.negative_indices)
        else:
            closest_to_pos = None
        print("Calculated closest opposite points of ", pos_pred_ind.shape[0], " positive testpoints")
        sys.stdout.flush()
        if len(neg_pred_ind) != 0:
            closest_to_neg = self.get_closest_opposite_points_using_neighbor_set(testpoints[neg_pred_ind],
                                                                                 self.positive_neighbors,
                                                                                 self.positive_indices)
        else:
            closest_to_neg = None
        print("Calculated closest opposite points of ", neg_pred_ind.shape[0], " negative testpoints")
        sys.stdout.flush()
        opp_points = np.zeros_like(testpoints)
        if closest_to_pos is not None:
            opp_points[pos_pred_ind] = closest_to_pos
        if closest_to_neg is not None:
            opp_points[neg_pred_ind] = closest_to_neg
        return opp_points

    def get_reference_point_from_closest_opposite_point(self, testpoint, oppositepoint, error=0.01):
        self.refcount += 1
        if (self.refcount % 1000 == 0):
            print("Starting reference point calculation for ", self.refcount, "th point")
            sys.stdout.flush()
        testval = self.clf.decision_function([testpoint])
        oppval = self.clf.decision_function([oppositepoint])
        # if testval*oppval > 0:
        #   print("Testpoint: " + str(testpoint) + " val " + str(testval) + " predict " + str(self.clf.predict([testpoint])))
        #   print("Oppositepoint: " + str(oppositepoint) + " val " + str(oppval) + " predict " + str(self.clf.predict([oppositepoint])))
        # Assertion removed because some opposite points have wrong predictions causing assertion to fail
        # assert (testval*oppval < 0), 'Opposite point has same sign for decision function!'
        startpoint = np.copy(testpoint)
        endpoint = np.copy(oppositepoint)
        # Added second condition "linalg.norm(..." because above assertion failure prevents decision function error from
        # ever falling below specified error
        while ((abs(self.clf.decision_function([endpoint])) > error)
               and (linalg.norm(endpoint - startpoint) > error)):
            distance = linalg.norm(endpoint - startpoint)
            unit = (endpoint - startpoint) / distance
            midpoint = startpoint + (distance / 2.0) * unit
            midval = self.clf.decision_function([midpoint])
            startval = self.clf.decision_function([startpoint])
            if midval * startval > 0:
                startpoint = endpoint
                endpoint = midpoint
            else:
                endpoint = midpoint
        return endpoint

    def get_reference_points_from_closest_opposite_points(self, testpoints):
        opposite_points = self.get_closest_opposite_points(testpoints)
        self.refcount = 0
        to_return = np.array(
            [self.get_reference_point_from_closest_opposite_point(testpoints[i], opposite_points[i]) for i in
             range(testpoints.shape[0])])
        return to_return

    def one_dimension_gradient(self, testpoint, dimension, delta):
        newpoint = np.copy(testpoint)
        newpoint[dimension] += delta
        grad = None
        try:
            grad = (self.clf.decision_function([newpoint])[0] - self.clf.decision_function([testpoint])[0]) / delta
            return grad
        except ValueError:
            print("Value error for testpoint ", testpoint)
            print("Value for newpoint ", newpoint)
            raise

    def get_gradient(self, testpoint, delta=0.001):
        return [self.one_dimension_gradient(testpoint, i, delta) for i in range(testpoint.shape[0])]

    def functional_margin(self, testpoint):
        # Each term in the sum is alpha_i*y_i* e**(-gamma*(norm(ith_support_vector - testpoint))**2) + b
        return np.sum(np.array([self.clf.dual_coef_[0][i]
                                * math.exp(-1.0 * self.gamma
                                           * math.pow(linalg.norm(self.clf.support_vectors_[i] - testpoint), 2)
                                           )
                                for i in range(self.clf.support_vectors_.shape[0])
                                ])
                      ) + self.clf.intercept_[0]

    def get_one_dimension_analytic_gradient(self, testpoint, j):
        # Each term in the sum is alpha_i*y_i*2*gamma*(jth_dimension_of_ith_support_vector - jth_dimension_of_test_point)
        # * e**(-gamma*(norm(ith_support_vector - testpoint))**2)
        return np.sum(np.array([self.clf.dual_coef_[0][i]
                                * 2.0 * self.gamma
                                * (self.clf.support_vectors_[i][j] - testpoint[j])
                                * math.exp(-1.0 * self.gamma
                                           * math.pow(linalg.norm(self.clf.support_vectors_[i] - testpoint), 2)
                                           )
                                for i in range(self.clf.support_vectors_.shape[0])
                                ]))

    # def get_analytic_gradient(self, testpoint):
    #    return np.array([self.get_one_dimension_analytic_gradient(testpoint,j) for j in range(testpoint.shape[0])])

    def get_analytic_gradient(self, testpoint):
        per_coordinate_differences = (self.clf.support_vectors_
                                      - testpoint[None, :])
        common_term_per_sv = (self.clf.dual_coef_[0]
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

    def get_analytic_gradient_csr(self, testpoint):
        self.analyticgradientcount += 1
        print("Analytic gradient for testpoint ", self.analyticgradientcount)
        print("TESTPOINT SHAPE: " + str(testpoint.shape))
        start = time.time()
        # matrix of differences of testpoint from each support vector, per
        # coordinate
        per_coordinate_differences = csr_matrix((self.csr_support_vectors.shape[0], self.csr_support_vectors.shape[1]))
        start5 = time.time()
        for i in range(0, self.csr_support_vectors.shape[0]):
            per_coordinate_differences[i] = self.csr_support_vectors.getrow(i) - testpoint
        print("Per coordinate differences computed in:", round(time.time() - start5, 2), "s")
        # compute the vector of terms that stay the same per support vector
        start2 = time.time()
        dual_coef_vector = self.clf.dual_coef_[0]
        common_term_per_sv = csr_matrix(np.multiply(dual_coef_vector[:, None],
                                                    2.0
                                                    * self.gamma
                                                    * np.exp(
                                                        -1.0 * self.gamma *
                                                        np.sum(per_coordinate_differences.power(2),
                                                               axis=1))))
        print("COMMON TERM PER SV SHAPE: " + str(common_term_per_sv.shape))
        print("Common term per SV computed in:", round(time.time() - start2, 2), "s")
        print("DUAL COEF SHAPE: " + str(self.clf.dual_coef_[0].shape))
        print("PER COORDINATE DIFF SHAPE: " + str(per_coordinate_differences.shape))
        product = csr_matrix((per_coordinate_differences.shape[1], per_coordinate_differences.shape[0]))
        start3 = time.time()
        for i in range(0, per_coordinate_differences.shape[1]):
            temp = common_term_per_sv.transpose()
            product[i] = temp.multiply(per_coordinate_differences.getcol(i))
        print("PRODUCT SHAPE: " + str(product.shape))
        print("Product computed in:", round(time.time() - start3, 2), "s")
        returnable = np.sum(product, axis=0)
        start4 = time.time()
        print("Product summed in:", round(time.time() - start4, 2), "s")
        print("One testpoint analytic gradient computed in:", round(time.time() - start, 2), "s")
        return returnable

    def get_average_gradient_between_two_points_csr(self, frompoint, topoint, numsteps):
        self.refcount += 1
        if (self.refcount % 100 == 0):
            print("Starting average gradient calculation for ", self.refcount, "th point")
        distance = sparse.linalg.norm(topoint - frompoint)
        unit = (topoint - frompoint) / distance
        waypoints = np.linspace(0, distance, numsteps)
        return np.average([self.get_analytic_gradient_csr(frompoint + waypoints[i] * unit) for i in range(numsteps)],
                          axis=0)

    def get_average_gradient_between_two_points(self, frompoint, topoint, numsteps):
        self.refcount += 1
        if (self.refcount % 100 == 0):
            print("Starting average gradient calculation for ", self.refcount, "th point")
        distance = linalg.norm(topoint - frompoint)
        unit = (topoint - frompoint) / distance
        waypoints = np.linspace(0, distance, numsteps)
        return np.average([self.get_analytic_gradient(frompoint + waypoints[i] * unit) for i in range(numsteps)],
                          axis=0)

    def get_average_gradient_between_two_points_optimized(self, frompoint, topoint, numsteps):
        self.refcount += 1
        if (self.refcount % 100 == 0):
            print("Starting average gradient calculation for ", self.refcount, "th point")
        distance = linalg.norm(topoint - frompoint)
        unit = (topoint - frompoint) / distance
        waypoints = np.linspace(0, distance, numsteps)
        #print("GAMMA DIMENSIONS: " + str(self.gamma.shape))
        testpointarray = np.array([(frompoint + waypoints[i] * unit) for i in range(numsteps)])
        sv_feature_array = self.get_non_zero_dense(testpointarray, self.support_vector_non_zero_indices)
        xclusive_non_zero_indices = np.setdiff1d(self.get_non_zero_column_indices(testpointarray), self.support_vector_non_zero_indices)
        xclusive_feature_array = self.get_non_zero_dense(testpointarray, xclusive_non_zero_indices)
        # ||Z^i - X(p)||^2 term where i spans support vectors, p spans testarraypoints
        mag = np.sum(np.square(self.non_zero_support_vectors[:,None,:]-sv_feature_array[None,:,:]),axis=2) \
                            + np.sum(np.square(xclusive_feature_array[None,:,:]),axis=2)
       #print("MAG DIMENSIONS: " + str(mag.shape))
        #print("DUAL COEF DIMENSIONS: " + str(self.clf.dual_coef_.shape))
        common_term_array = np.exp(mag)*self.clf.dual_coef_[:,:].transpose((1,0))*2*self.gamma

        
        
        # Axis 0 is number of support vectors, Axis 1 is number of interpolations, Axis 2 is number of nonzero support vector features
        allinterp=np.sum(common_term_array[:,:,None]*(self.non_zero_support_vectors[:,None,:]-sv_feature_array[None,:,:]), axis=0)
        average_gradient_xsv=np.average(allinterp, axis=0)
        # Same set of axes as last one
        allinterpxclusive = np.sum(common_term_array[:, :, None] * (-xclusive_feature_array[None, :, :]), axis=0)
        #print("ALLINTERPXCLUSIVE SHAPE: " + str(allinterpxclusive.shape))
        average_gradient=np.zeros(testpointarray.shape[1])
        if not len(xclusive_non_zero_indices)==0:
            average_gradient_xclusive = np.average(allinterpxclusive, axis=0)
            average_gradient[xclusive_non_zero_indices]=average_gradient_xclusive
        average_gradient[self.support_vector_non_zero_indices]=average_gradient_xsv
	return average_gradient
        


    def get_average_gradient_between_points_csr(self, frompoints, topoints, numsteps):
        start = time.time()
        self.refcount = 0
        to_return = np.array([self.get_average_gradient_between_two_points_csr(
            frompoint=frompoints[i], topoint=topoints[i], numsteps=numsteps)
            for i in range(frompoints.shape[0])])
        print("Avg grad computed in:", round(time.time() - start, 2), "s")
        return to_return

    def get_average_gradient_between_points(self, frompoints, topoints, numsteps):
        start = time.time()
        self.refcount = 0
        to_return = np.array([self.get_average_gradient_between_two_points(
            frompoint=x, topoint=y, numsteps=numsteps)
            for x, y in zip(frompoints, topoints)])
        print("Avg grad computed in:", round(time.time() - start, 2), "s")
        return to_return

    def get_feature_contribs_using_average_gradient_from_reference(self, testpoints, reference_to_use, numsteps):
        assert (np.isfinite(testpoints).all()), "Some of the training points are not finite!"
        if (reference_to_use is None):
            frompoints = self.get_reference_points_from_closest_opposite_points(testpoints)
        else:
            frompoints = reference_to_use
        assert (np.isfinite(frompoints).all()), "Some of the obtained reference points are not finite!"
        if self.use_csr:
            frompoints_csr = csr_matrix(frompoints)
            testpoints_csr = csr_matrix(testpoints)
            print("From points shape is " + str(frompoints.shape))
            print("From points CSR nonzero count is " + str(len(frompoints_csr.nonzero()[0])))
            print("Test points shape is " + str(testpoints.shape))
            print("Test points CSR nonzero count is " + str(len(testpoints_csr.nonzero()[0])))
            avg_gradients = self.get_average_gradient_between_points_csr(frompoints_csr, testpoints_csr,
                                                                         numsteps=numsteps)
            contribs = (testpoints_csr - frompoints_csr) * avg_gradients
            return contribs.todense(), avg_gradients.todense()
        else:
            avg_gradients = self.get_average_gradient_between_points(frompoints, testpoints, numsteps=numsteps)
            contribs = (testpoints - frompoints) * avg_gradients
            return contribs, avg_gradients
