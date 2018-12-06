# DETest

A Differential Equation Testing Suite

Alejandro Francisco Queiruga  
Lawrence Berkeley National Lab  
2018

This repository contains a set of testing problems with known analytical solutions or reference solutions from a "trusted" code: oracles.
It can generate a testing framework based on Python's unittest test will automatically compare your code to these oracles, making sure on a variety of problems that your code are exactly correct, an approximation that converges at the expected rate, or at least gives you the same answer you got yesterday.

These tests were originally written to support Millstone, TOUGH+, HGMiv, and [Periflakes]().

## Introduction

Testing numerical scientific and engineering codes has a further challenge than normal software.
The results are inexact and the expected behavior can be unknown.
When we see something wrong with out codes, we don't know if it's a problem with:

1. a bug in the code?
2. a failure of the numerical model?
3. a fundamental problem with the underlying theory?
4. or incorrect expectations?

We address bullet point #4 by providing a trusted set of analytical solutions to be oracles in this library.
The oracles (their theory, mathematical solution, and implementation) are verified by being in agreement with multiple codes!
We can use these oracles and an understanding of the behavior we expect to see from our codes to help us diagnose issues #1-#3.

1. Unit Tests - make sure the code works
2. Known Analytical Oracles - tests with known solutions. The code could either get these solutions exactly correct, or only approximates the solution approach at an expected convergence rate.
3. Self-Similarity Convergence - Problems without known solutions, but the testee should behave consistently with itself.
4. Reference Tests - tests with no known solutions, but we compare the codes to an over-discretized trusted code, or experimental data.

The philosophy I have evolved has the following phases:

### Unit Tests

These are software tests.
These tests are for things on the order of "Does the code read an input file correctly?"
This repository doesn't deal with them: they're unique to the codebase.

### Oracle-based Exact Precision Tests

The methods we use to solve problems should be able to get certain solutions **Exactly Correct**.

![assert](https://latex.codecogs.com/gif.latex?assert\left(&space;\left|\left|&space;code&space;-&space;oracle&space;\right|\right|&space;<&space;10^{-12}&space;\right))
<!--\[
assert\left( \left|\left| code - oracle \right|\right| < 10^{-12} \right)
\]-->

These can be done in the same unit testing framework. They should be cheap.
This library will generate a unittest object for requested exact precision tests.

### Oracle-based Convergence Tests

These problems should also have the property that they are Lipschitz continuous; i.e. the numerical problem should converge smoothly.

These require more computational effort to run.
There is some advice for designing simple problems that the testee should be able to execute extremely quickly.

This library will generate a unittest object for requested exact precision tests.

![error](https://latex.codecogs.com/gif.latex?e(h)&space;=&space;\left|\left|&space;code(h)&space;-&space;oracle&space;\right|\right|)
<!--\[
e(h) = \left|\left| code(h) - oracle \right|\right|
\]-->

![assert](https://latex.codecogs.com/gif.latex?assert\left(&space;regression(\log(h),\log(e))&space;\approx&space;rate&space;\right))
<!-- \[
assert\left( regression(\log(h),\log(e)) \approx rate \right)
\] -->

for an expected rate.

### Self-Similarity Convergence Tests

We assume self similarity.

![error](https://latex.codecogs.com/gif.latex?e(h)&space;=&space;\left|\left|&space;code(h)&space;-&space;code(H^*)&space;\right|\right|)
<!-- \[
e(h) = \left|\left| code(h) - code(H^*) \right|\right|
\] -->

where $H^*\ll h$.

![assert](https://latex.codecogs.com/gif.latex?assert\left(&space;regression(\log(h),\log(e))&space;\approx&space;rate&space;\right))
<!-- \[
assert\left( regression(\log(h),\log(e)) \approx rate \right)
\] -->

### Reference Tests

We can construct a reference solution by saving the solutions of a "golden code" in the database, and then comparing future codes to it.

### Regression Tests

Running all of the above tests can be costly.
Most of our everyday programming shouldn't effect the results for most of the codes capabilities.
After a set of changes, we should assert

![assert](https://latex.codecogs.com/gif.latex?assert\left(&space;code(today)&space;\approx&space;code(yesterday)&space;\right))
<!-- \[
assert\left( code(today) \approx code(yesterday) \right)
\] -->

for every problem we don't think we changed.
These can be very fast and short, and randomly generated every day.

DETest will eventually have a class that runs these tests and maintains this history database.

## What makes a good test?

What happens when one of these tests isn't Lipschitz continuous? What if the physics itself has bifurcation points?
How do we verify a code that is supposed to be solving a nonsmooth problem?
These are hard problems to solve.
A strategy is to examine ergodic properties, such as the center point of an attractor, the total amount of gas in the reservoir, the granular temperature of the system, etc.
These have to be coupled by making your code solve the simpler problems, too.
Currently, we have no such tests in this package.


## The Tests

Right now, there are only solutions for poroelasticity and single-phase flow.

- Oracles:

  1. Constant strain modes in elasticity
  2. Constant flux flow
  1. Terzaghi's consolidation
  2. de Leeuw's consolidation
  3. Thin crack in tension / under pressure
  4. Poisson problem
  5. Radial production in a poroelastic system

- Reference problems:

  1. None yet

The problems in the library each have their own module.
Each module has a description, default parameter dictionary, and at least one class that implements the solution.
The class is meant to behave like a closure, where it is initialized with a parameter set and is callable.
Each closure evaluates the analytical solution at a point that is some combination of $(x,y,z,t)$ for the given parameters.
The module will have a default set of parameters.

The units for default properties are all in SI.
This strictly doesn't matter, but for some codes the properties are not inputs, but instead intrinsic to the theoretical formulation.

## Installation

detest is compatible with both Python 2 and 3. Numpy is required, and some of the oracles make use of Scipy and Sympy. Install it with setuptools,
```bash
python setup.py install --prefix=/path/to/install/to
```
and then import it with `import detest`.

## Using the Test Suite

### Wrapping the code

The developer needs to wrap their code into a Python script with one function call for each oracle.
The routine for your code takes two arguments: a dictionary of parameters, and an 'h' argument for discretization scale.
The parameters a specific to the oracle problem (e.g. domain size, conductivity, etc.); read the description of the oracle.
To check mesh refinement, 'h' will be a grid spacing or a timestep size. (I sometimes make it control both.)
Detest will automatically call the script with a set of parameters with many different 'h's.
The output is a dictionary that matches the field names of the oracle, plus an additional field 'points'.

For a command line code, this will look something like this:
```python
def myScript(parameters, h):
  make_tough_input(h,parameters)
  sp.call(['TH','millstone_input.py',str(h)])
  x,U,P = process_results_for_testing()
  return {'U':U,'P':P, 'points':x}
```
where the developer is responsible for autogenerating their input files.

### Making an automated suite

Detest will autogenerate a unittest suite.
A snippet this short will populate the unittest framework:
```python
suite = [
    detest.ExactTest(      detest.oracles.Uniaxial, myUniaxial),
    detest.ExactTest(      detest.oracles.Shear,    myShear),
    detest.ConvergenceTest(detest.oracles.Terzaghi, myTerzaghi, 1),
]
MyTestSuite = detest.make_suite(suite)
```
The file can then be executed with the unittest module,
```bash
python -m unittest MyTestSuite.py
```
The power of this architecture is that list can be generated with a loop.
An example of this is in [afqsrungekutta](https://github.com/afqueiruga/afqsrungekutta/blob/master/test/de_test.py),
wherein a seperate ConvergenceTest for every each tableau is made.

### Just using the oracles

Detest is also a library of analytical solutions.
One can just import the solutions if that's useful,
```python
import detest
f = detest.oracles.Terzaghi({'k':2.0e-12})
displacement = f([[5.0,10.0]])['U']
```
This is particularly useful for applying truncated boundary conditions for some of the convergence tests.

### Computation Expense Concerns

Running numerical tests is expensive in terms of computing time, which is also a dollar-cost.
There are different strategies to minimize the cost and enable real-time continuous integration:

1. Only test randomly with frequency, and save the rigorous-churn through tests for weekly tests.
2. Use a scheduling environment to run tests in parallel on commodity resources.
3. Schedule them for low-priority queues at a low-cost off-hours.

## License

Copyright (C) Alejandro Francisco Queiruga, 2015-2018  
Lawrence Berkeley National Lab

DETest is released under version 3 of the GNU Lesser General Public License, as per LICENSE.txt.

## Acknowledgements

This library was developed to support various projects in the Earth and Environmental Sciences division at Lawrence Berkeley National Lab.
