# Hydrogeology Testing Suite

Alejandro Francisco Queiruga  
Lawrence Berkeley National Lab  
2018

This repository contains a set of testing problems with known analytical solutions or reference solutions from a "trusted" code. (Note: Sometimes tests are wrong!)

These tests were originally written to test TOUGH+Millstone and HGMiv.

## Introduction

Testing numerical scientific and engineering codes has a further challenge than normal software. The results are inexact and the expected behavior can be unknown. The philosphy I have evolved has the following phases:

1. Unit Tests - make sure the code works
2. Exact Precision Tests - the numerical algorithm gets these **Exactly Correct** to known solutions
3. Known Analytical Tests - tests with known solutions, but we have to discretize to get to them.
4. Reference Tests - tests with no known solutions, but we compare the codes to an over-discretized trusted code.

### Unit Tests

These are software tests. These tests are for things on the order of "Does the code read an input file correctly?". This repository doesn't deal with them, they're unique to the codebase

### Exact Precision Tests

These can be done in the same unit testing framework. They should be cheap.

This library will generate a unittest object for requested exact precision tests.

### Known-Solution Analytical Tests

These problems should also have the property that they are Lipschitz continuous; i.e. the numerical problem should converge smoothly.

These require more computational effort to run.

### Reference Solution Tests

We assume self similarity.

What happens when one of these tests isn't Lipschitz continuous? What if the physics itself has bifurcation points? How do we verify in that case?

## The Tests

Right now, there are only solutions for poroelasticity and single-phase flow.

- Exact problems:
  1. Constant strain modes in elasticity
  2. Constant flux flow
  
- Numerical problems:
  1. Terzaghi's consolidation
  2. de Leeuw's consolidation
  3. (M) Thin crack in tension / pressurized
  4. Poisson problem
  5. Radial production in a poroelastic system
  
- Reference problems:
  1. None yet

The units for default properties are all in SI. This strictly doesn't matter, but for some codes the properties are not inputs, but intrinsic to the formulation!

The problems in the database each have their own module.
Each module has a description, default parameter dictionary, and a solution routine.
They solution routine returns a dictionary of closures. Each closure evaluates the analytical solution at a point that is some combination of $(x,y,z,t)$ for the given parameters.
The module will have a default set of parameters.

## Using the Test Suite

The developer will need to wrap their code into a Python script.

For a command line code, this will look something like this:
```python
def runit(parameters, h,dt):
  make_tough_input(h,dt,parameters)
  sp.call(['TH','millstone_input.py',str(h),str(dt)])
  return process_results_for_testing()
```
where the developer is responsible for autogenerating their input files.

### Making an automated suite

This library also contains tools for 
```python
hgt.ExactTestRunner([
  (hgt.uniaxial, run_uniaxial),
  (hgt.constant_flux, run_constant_flux),
])
```

Running numerical tests is expensive in terms of computing time, which is also a dollar-cost.

There are different strategies to minimize the cost:

1. Only test randomly with frequency, and save the rigorous-churn through tests for weekly tests.
2. Use a scheduling environment to run tests in parallel on commodity resources.
3. Schedule them for low-priority queues at a low-cost off-hours. 

## License
