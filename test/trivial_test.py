# Test that some internal components don't break.

import detest
from detest import TestRunner

import unittest as ut

class trivial(ut.TestCase):
    def test(self):
        TestRunner.TestRunner(detest.oracles.mechanics_constant.Uniaxial,
            lambda x:x)
        TestRunner.TestRunner(detest.oracles.mechanics_constant.Uniaxial,
            lambda x:x, scratch_space='foo')
