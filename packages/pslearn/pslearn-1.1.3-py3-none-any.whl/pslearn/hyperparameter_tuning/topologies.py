import pandas as pd
import numpy as np
import itertools
from scipy.spatial import distance
from joblib import Parallel, delayed
from pslearn.hyperparameter_tuning.update import Update


# PSO
class ParticleSwarmSearchCV:
    def __init__(self, initilization_fn, evaluation_fn, n_iter):
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

        self.initilization_fn = initilization_fn
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

        self.update_fn.n_iter = self.n_iter
        # 1) Spawn Particles
        particles = self.initilization_fn._spawn()

        # Initiate global best score, global best parameters and iteration
        gbest = None
        gbest_params = None
        iter = 0
        while True:
            # 2) Evaluate each particles
            scores_params = Parallel(n_jobs=-1)(delayed(self.evaluation_fn._evaluate)(p, X, y) for p in particles)
            scores_params = pd.DataFrame(scores_params, columns=['params', 'score'])

            # 3) Get the current best score and current best parameters
            cbest_params = scores_params.sort_values('score', ascending=False).iloc[0, 0]
            cbest = scores_params.sort_values('score', ascending=False).iloc[0, 1]

            # 4) Update global best score and parameters if current best is greater than the global best
            if gbest == None or gbest < cbest:
                gbest = cbest
                gbest_params = cbest_params

            # 5) Check stopping criteria
            if iter >= self.n_iter:
                break

            # 6) Update the velocities of the particles
            self.update_fn.iter = iter
            particles = Parallel(n_jobs=1)(delayed(self.update_fn._update)(p, gbest_params) for p in particles)

            if iter >= self.n_iter:
                break

            iter += 1

        self.best_score_ = gbest
        self.best_params_ = gbest_params


# SPSO
class SlicedParticleSwarmSearchCV:
    def __init__(self, initilization_fn, evaluation_fn, n_iter, n_slice):
        self.initilization_fn = initilization_fn
        self.evaluation_fn = evaluation_fn
        self.update_fn = Update()
        self.n_iter = n_iter
        self.search_space = initilization_fn.search_space
        self.n_slice = n_slice
        self.best_score_ = None

    def _slice_space(self):
        # For all numerical spaces
        all_num_key = {k: v for k, v in self.search_space.items() if sum([isinstance(i, str) for i in v]) != len(v)}
        num_dim = []
        for s in all_num_key.values():
            lower = s[0]
            upper = s[1]
            prior = s[2]

            # Create space with lower and upper
            range_ = np.arange(s[0], s[1])

            # Split the space in to sub spaces
            splitted_range_ = np.split(range_, self.n_slice)
            splitted_range_ = [list(j) for j in splitted_range_]
            splitted_range_ = str(splitted_range_)
            num_dim.append(splitted_range_)

        num_dim = ", ".join(num_dim)

        num_sub_space = eval(f'''[i for i in itertools.product({num_dim})]''')

        # For all categorical spaces
        all_str_key = {k: v for k, v in self.search_space.items() if sum([isinstance(i, str) for i in v]) == len(v)}
        sub_spaces = []
        for categories in all_str_key.values():
            for category in categories:
                for s in num_sub_space:
                    sub_cat_dim = []
                    for dim in s:
                        sub_cat_dim.append(dim)

                    sub_cat_dim.append([category] * 3)

                    sub_spaces.append(sub_cat_dim)

        # Total sub spaces = n_slice ** n_num_dim * n_categories
        all_sub_spaces = []
        for i in range(len(sub_spaces)):
            sub_space = {}
            for k, j in enumerate(self.search_space.items()):
                dim_name = j[0]
                prior = j[1][-1]
                if isinstance(sub_spaces[i][k][0], str) and isinstance(sub_spaces[i][k][-1], str):
                    sub_space[str(dim_name)] = sub_spaces[i][k]

                else:
                    #                     1  X  lower
                    sub_dim = (sub_spaces[i][k][0], sub_spaces[i][k][-1], prior)
                    sub_space[str(dim_name)] = sub_dim

            all_sub_spaces.append(sub_space)

        return all_sub_spaces

    def fit(self, X, y):
        sub_spaces = self._slice_space()
        for space in sub_spaces:
            self.update_fn.n_iter = self.n_iter
            # 1) Spawn Particles
            self.initilization_fn.search_space = space
            particles = self.initilization_fn._spawn()

            # Initiate global best score, global best parameters and iteration
            gbest = None
            gbest_params = None
            iter = 0
            while True:
                # 2) Evaluate each particles
                scores_params = Parallel(n_jobs=-1)(delayed(self.evaluation_fn._evaluate)(p, X, y) for p in particles)
                scores_params = pd.DataFrame(scores_params, columns=['params', 'score'])

                # 3) Get the current best score and current best parameters
                cbest_params = scores_params.sort_values('score', ascending=False).iloc[0, 0]
                cbest = scores_params.sort_values('score', ascending=False).iloc[0, 1]

                # 4) Update global best score and parameters if current best is greater than the global best
                if gbest == None or gbest < cbest:
                    gbest = cbest
                    gbest_params = cbest_params

                # 5) Check stopping criteria
                if iter >= self.n_iter:
                    break

                # 6) Update the velocities of the particles
                particles = Parallel(n_jobs=1)(delayed(self.update_fn._update)(p, gbest_params, iter) for p in particles)

                iter += 1

            if (self.best_score_ == None) or (gbest > self.best_score_):
                self.best_score_ = gbest
                self.best_params_ = gbest_params


# TRIBES
class TRIBES:
    def __init__(self, initilization_fn, evaluation_fn, n_iter, grp_size):
        self.initilization_fn = initilization_fn
        self.evaluation_fn = evaluation_fn
        self.update_fn = Update()
        self.n_iter = n_iter
        self.grp_size = grp_size

    def _group_particles(self, particles):
        similarities = pd.DataFrame()
        for idx1, p1 in enumerate(particles):
            for idx2, p2 in enumerate(particles):
                p1_position_vector = [v[0] for v in p1.values() if not isinstance(v[0], str)]
                p2_position_vector = [v[0] for v in p2.values() if not isinstance(v[0], str)]
                similarity = 1 - distance.cosine(p1_position_vector, p2_position_vector)
                similarities.loc[idx1, idx2] = similarity
                if idx1 == idx2:
                    similarities.loc[idx1, idx2] = np.nan

        flat_list = []
        grouped = []
        while True:
            clusters = [sorted([col] + list(similarities[col].sort_values(ascending=False)[:self.grp_size - 1].index)) for
                        col in similarities.columns]

            clusters_count = {}
            for c1 in clusters:
                clusters_count[str(c1)] = 0
                for c2 in clusters:
                    if c1 == c2:
                        clusters_count[str(c1)] += 1

            clusters_count = pd.DataFrame(clusters_count, index=['Counts']).T
            clusters_count.sort_values('Counts', ascending=False, inplace=True)

            grouped.append(eval(list(clusters_count.index)[0]))
            clusters_count.drop(list(clusters_count.index)[0], inplace=True)

            for sublist in grouped:
                for item in sublist:
                    flat_list.append(item)

            for i in flat_list:
                if i in similarities.columns:
                    similarities.drop(i, inplace=True)
                    similarities.drop(i, axis=1, inplace=True)

            if len(similarities.columns) == 0:
                break

        return grouped

    def fit(self, X, y):
        self.update_fn.n_iter = self.n_iter
        # 1) Spawn Particles
        particles = self.initilization_fn._spawn()

        # Initiate global best score, global best parameters and iteration
        group = self._group_particles(particles)
        for grp_idx in group:
            grp = pd.Series(particles).iloc[grp_idx]
            gbest = None
            gbest_params = None
            iter = 0
            while True:
                # 2) Evaluate each particles
                scores_params = Parallel(n_jobs=-1)(delayed(self.evaluation_fn._evaluate)(p, X, y) for p in grp)
                scores_params = pd.DataFrame(scores_params, columns=['params', 'score'])

                # 3) Get the current best score and current best parameters
                cbest_params = scores_params.sort_values('score', ascending=False).iloc[0, 0]
                cbest = scores_params.sort_values('score', ascending=False).iloc[0, 1]

                # 4) Update global best score and parameters if current best is greater than the global best
                if gbest == None or gbest < cbest:
                    gbest = cbest
                    gbest_params = cbest_params

                # 5) Check stopping criteria
                if iter >= self.n_iter:
                    break

                # 6) Update the velocities of the particles
                particles = Parallel(n_jobs=1)(delayed(self.update_fn._update)(p, gbest_params, iter) for p in particles)

                if iter >= self.n_iter:
                    break

                iter += 1

            if (self.best_score_ == None) or (gbest > self.best_score_):
                self.best_score_ = gbest
                self.best_params_ = gbest_params


# Multi-PSO
class MultiSwarmParticleSwarmSearchCV:
    def __init__(self, initilization_fn, evaluation_fn, n_iter, n_swarm):
        self.initilization_fn = initilization_fn
        self.evaluation_fn = evaluation_fn
        self.update_fn = Update()
        self.n_iter = n_iter
        self.n_swarm = n_swarm

    def fit(self, X, y):
        self.update_fn.n_iter = self.n_iter
        # 1) Spawn Particles
        particles = self.initilization_fn._spawn()

        # Initiate global best score, global best parameters and iteration
        for i in range(n_swarm):
            gbest = None
            gbest_params = None
            iter = 0
            while True:
                # 2) Evaluate each particles
                scores_params = Parallel(n_jobs=-1)(delayed(self.evaluation_fn._evaluate)(p, X, y) for p in particles)
                scores_params = pd.DataFrame(scores_params, columns=['params', 'score'])

                # 3) Get the current best score and current best parameters
                cbest_params = scores_params.sort_values('score', ascending=False).iloc[0, 0]
                cbest = scores_params.sort_values('score', ascending=False).iloc[0, 1]

                # 4) Update global best score and parameters if current best is greater than the global best
                if gbest == None or gbest < cbest:
                    gbest = cbest
                    gbest_params = cbest_params

                # 5) Check stopping criteria
                if iter >= self.n_iter:
                    break

                # 6) Update the velocities of the particles
                particles = Parallel(n_jobs=1)(delayed(self.update_fn._update)(p, gbest_params, iter) for p in particles)

                if iter >= self.n_iter:
                    break

                iter += 1

            if (self.best_score_ == None) or (gbest > self.best_score_):
                self.best_score_ = gbest
                self.best_params_ = gbest_params


# APSO, StochasticStar, Cyber Swarm, and C-PSO
