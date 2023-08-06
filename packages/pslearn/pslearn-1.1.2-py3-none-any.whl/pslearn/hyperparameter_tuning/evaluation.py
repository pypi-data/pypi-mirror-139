import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator

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

    def _evaluate(self, p: dict, X: pd.DataFrame, y: pd.DataFrame):
        """Run fit on the estimator with randomly drawn parameters.
       Parameters
       ----------
        X : array-like or sparse matrix, shape = [n_samples, n_features]
            The training input samples.
        y : array-like, shape = [n_samples] or [n_samples, n_output]
            Target relative to X for classification or regression (class
            labels should be integers or strings).
       """

        # Convert dictionary values into [values]
        params = {k: v[0] for k, v in p.items()}

        # Check if parameters are already in memo, if so, use values from memo
        if str(params) in self.memo:
            score = self.memo[str(params)]

        # If not do grid search
        else:
            g = GridSearchCV(
                estimator=self.estimator,
                cv=self.cv,
                scoring=self.scoring,
                n_jobs=self.n_jobs,
                param_grid=p
            )

            g.fit(X=X, y=y)
            score = g.score(X=X, y=y)
            self.memo[str(params)] = score

        return params, score