import numpy as np


class Initilization:
    """Run fit on the estimator with randomly drawn parameters.
       Parameters
       ----------
       search_spaces : dict, list of dict or list of tuple containing (dict, int).
       Dictionary, where keys are parameter names (strings)
       and values are skopt.space.Dimension instances (Real, Integer
       or Categorical) or any other valid value that defines skopt
       dimension (see skopt.Optimizer docs). Represents search space
       over parameters of the provided estimator.

       n_particles : int
       Determines the number of initial solution candidates.
       """
    def __init__(self, search_space: dict, n_particles: int=10):
        self.search_space = search_space
        self.n_particles = n_particles

    def _spawn(self):
        particles = []
        for n in range(self.n_particles):
            loc = {}
            for parameters, range_ in self.search_space.items():
                lower = range_[0]
                upper = range_[1]
                prior = range_[2]

                # if type of lower and upper are numbers and prior is string, sample solutions from given search spaces according to given prior
                if type(lower) in [int, np.int32, np.int64] and type(upper) in [int, np.int32, np.int64] and isinstance(prior, str):
                    if prior == 'uniform':
                        sample = np.random.uniform(low=lower, high=upper)

                    elif prior == 'normal':
                        sampling = np.arange(lower, upper + 1)
                        mu = sampling.mean()
                        sigma = sampling.std()
                        sample = np.random.normal(loc=mu, scale=sigma)

                    else:
                        sampling = np.arange(lower, upper + 1)
                        mu = sampling.mean()
                        sigma = sampling.std()
                        sample = np.random.lognormal(mean=mu, sigma=sigma)

                    sample = int(sample)

                    if sample < lower:
                        sample = lower

                    elif sample > upper:
                        sample = upper

                # Check if all string, if so, randomly pick a choice
                elif sum(isinstance(i, str) for i in range_) > 0:
                    sample = np.random.choice(range_)

                loc[parameters] = [sample]

            particles.append(loc)

        return particles
