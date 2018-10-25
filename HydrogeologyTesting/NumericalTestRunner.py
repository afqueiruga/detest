class NumericalTestRunner():
    """
    Give this clas one problem and one script, and it will run a _convergence_
    test on the code, automatically.
    """
    def __init__(self, problem, script):
        self.problem = problem
        self.script = script


class NumericalTestingSuite():
    """
    This will churn through all of the numerical tests. It is very expensive.

    It can operate in a randomized testing fashion to minimize the cost
    of testing incremental updates. That is, you can configure it to do a
    subsample set frequently, and then schedule the exhaustive tests less
    frequently.
    """
    def __init__(self, TESTS):
        pass
