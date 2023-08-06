import numpy as np
import pandas as pd
from joblib import Parallel, delayed


class Update:
    def __init__(self):
        pass

    def _update(self, solutions, n_iter, i, gbest_params):
        """Run fit on the estimator with randomly drawn parameters.
           Parameters
           ----------
           solutions : array-like or sparse matrix, shape = [n_samples, n_solutions]
                       A pool of solution candidates.

           n_particles : int
                        Determines the number of initial solution candidates.

           i : int
                Current iteration.

           gbest_params : dict
                        Current global best parameters.
           """

        solutions.drop('score', axis=1, inplace=True)

        def _sub_update(s):
            rev_iter = [r for r in reversed(range(1, n_iter + 1))]
            velo = (gbest_params - solutions.iloc[s]) / (rev_iter[i])
            s = solutions.iloc[s] + velo * i

            return s

        solutions = Parallel(n_jobs=-1)(delayed(_sub_update)(s) for s in range(len(solutions)))
        solutions = pd.concat(solutions, axis=1).T

        return solutions
