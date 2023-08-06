import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import cross_val_score
from joblib import Parallel, delayed

class Evaluation:
    """
    Parameters
    ----------
    estimator : estimator object.
        A object of that type is instantiated for each search point.
        This object is assumed to implement the scikit-learn estimator api.
        Either estimator needs to provide a ``score`` function,
        or ``scoring`` must be passed.

    scoring : string, callable or None, default=None
        A string (see model evaluation documentation) or
        a scorer callable object / function with signature
        ``scorer(estimator, X, y)``.
        If ``None``, the ``score`` method of the estimator is used.

    n_jobs : int, default=-1
        Number of jobs to run in parallel. At maximum there are
        ``n_points`` times ``cv`` jobs available during each iteration.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross validation,
          - integer, to specify the number of folds in a `(Stratified)KFold`,
          - An object to be used as a cross-validation generator.
          - An iterable yielding train, test splits.
        For integer/None inputs, if the estimator is a classifier and ``y`` is
        either binary or multiclass, :class:`StratifiedKFold` is used. In all
        other cases, :class:`KFold` is used.
        """
    def __init__(self, estimator: BaseEstimator, cv: int, scoring: str, n_jobs: int=-1):
        self.estimator = estimator
        self.cv = cv
        self.scoring = scoring
        self.n_jobs = n_jobs
        self.memo = {}

    def _evaluate(self, solutions: pd.DataFrame):
        """Run fit on the estimator with randomly drawn parameters.
           Parameters
           ----------
           solutions : array-like or sparse matrix, shape = [n_samples, n_solutions]
                       A pool of solution candidates.
           """
        def _sub_evaluate(s, memo):
            # If the generated expression contains no features, then retry
            while True:
                expression = pd.Series(self.X.columns)[s > np.random.random()]
                if len(expression) == 0:
                    continue

                break

            # Check if expression is already in memo, if not then store
            if str(list(expression)) not in memo:
                score = cross_val_score(estimator=self.estimator, cv=self.cv, X=self.X[expression], y=self.y, scoring=self.scoring).mean()
                memo[str(list(expression))] = score

            # If so, use values from memo
            else:
                score = memo[str(list(expression))]

            s = pd.Series(s)
            s = pd.concat([s, pd.Series(score)])
            s.index = list(s.index[:-1]) + ['score']

            return s, memo

        solutions = Parallel(n_jobs=-1)(delayed(_sub_evaluate)(s[1], self.memo) for s in solutions.iterrows())
        for d in solutions:
            self.memo.update(d[1])
        solutions = [s[0] for s in solutions]
        solutions = pd.concat(solutions, axis=1).T

        return solutions