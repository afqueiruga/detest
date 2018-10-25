class ExactTestRunner():
    """
    Give this clas one problem and one script, and it will run it with a
    bunch of permutations and assert that the error is within machine
    precision. This class uses the standard unittest framework because
    the tests should be _cheap_.

    There is an optional rigor parameter which controls just how far it will
    go.
    """
    def __init__(self, problem, script, rigor=1):
        self.problem = problem
        self.script = script

class NumericalTestRunner():
    """
    Give this clas one problem and one script,
    """
    def __init__(self, problem, script):
        self.problem = problem
        self.script = script

class ExactTestingSuite():
    def __init__(self, TESTS):
        pass

class NumericalTestingSuite():
    def __init__(self, TESTS):
        pass
