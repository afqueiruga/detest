

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
    def test(self):
        for test in self.problem.tests:
            pass


class ExactTestingSuite():
    """
    Initialize this class to run All of the Tests.
    It works by populating the unittest framework.
    """
    def __init__(self, TESTS):
        pass
