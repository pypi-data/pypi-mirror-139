import numpy as np
import pandas as pd


class Initilization:
    """Run fit on the estimator with randomly drawn parameters.
       Parameters
       ----------
       n_particles : int
                    Determines the number of initial solution candidates.
       """

    def __init__(self, n_particles: int):
        self.n_particles = n_particles

    def _initialize(self):
        solutions = [np.random.random(size=len(self.X.columns)) for n in range(self.n_particles)]
        solutions = pd.DataFrame(solutions)

        return solutions