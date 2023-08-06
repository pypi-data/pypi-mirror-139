import pandas as pd
import numpy as np
import itertools
from scipy.spatial import distance
from joblib import Parallel, delayed
from pslearn.feature_selection.update import Update


# PSO
class ParticleSwarmFeatureSelectionCV:
    def __init__(self, initialization_fn, evaluation_fn, n_iter):
        """
        Parameters
        ----------
        initialization_fn : initialization_fn
                            initialization function module from particle_swarm_optimization.feature_seletion.initialization.

        evaluation_fn : evaluation_fn
                        evaluation function module from particle_swarm_optimization.feature_seletion.evaluation.

        n_iter : int
                Determines the maximum number of iterations.
        """

        self.initialization_fn = initialization_fn
        self.evaluation_fn = evaluation_fn
        self.update_fn = Update()
        self.n_iter = n_iter

    def fit(self, X, y):
        """
        Parameters
        ----------
        X : array-like or sparse matrix, shape = [n_samples, n_features]
            The training input samples.
        y : array-like, shape = [n_samples] or [n_samples, n_output]
            Target relative to X for classification or regression (class
            labels should be integers or strings).
        """

        self.initialization_fn.X = X
        self.evaluation_fn.X = X
        self.evaluation_fn.y = y

        gbest = None
        # 1) Spawn Particles

        solutions = self.initialization_fn._initialize()

        # Initiate global best score, global best parameters and iteration
        gbest = None
        gbest_params = None
        iter = 0
        while True:
            # 2) Evaluation
            solutions = self.evaluation_fn._evaluate(solutions)

            # 3) Update Global Best
            cbest = solutions.sort_values('score', ascending=False).iloc[0, -1]
            cbest_params = solutions.sort_values('score', ascending=False).iloc[0, :-1]
            if (gbest == None) or (gbest < cbest):
                gbest = cbest
                gbest_params = cbest_params

            # 4) Check stopping criteria
            if iter >= self.n_iter:
                break

            # 4) Calculate and Update velocities
            solutions = self.update_fn._update(solutions, self.n_iter, iter, gbest_params)

            iter += 1

        self.best_score_ = gbest
        self.best_params_ = list(X.columns[gbest_params > np.random.random()])
