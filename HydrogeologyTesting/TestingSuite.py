from .ExactTestRunner import ExactTestRunner
from .NumericalTestRunner import NumericalTestRunner



def fill_suite(cls, suite):
    for entry in suite:
        setattr(cls, 'test_{0}'.format(entry.name), entry.test)
