# Test that some internal components don't break.

import HydrogeologyTesting as hgtest
from HydrogeologyTesting import TestRunner

import unittest as ut

class trivial(ut.TestCase):
    def test(self):
        TestRunner.TestRunner(hgtest.oracles.mechanics_constant, lambda x:x)
        TestRunner.TestRunner(hgtest.oracles.mechanics_constant, lambda x:x, scratch_space='foo')
