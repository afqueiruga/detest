# Hydrogeology Testing Suite

Alejandro F Queiruga  
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

The units are all in SI. This strictly doesn't matter, but for some codes the properties are not inputs, but intrinsic to the formulation!

The problems in the database each have their own module.
Each module has a description, default parameter dictionary, and a solution routine.
They solution routine returns a dictionary of closures. Each closure evaluates the analytical solution at a point that is some combination of $(x,y,z,t)$ for the given parameters.
The module will have a default set of parameters.

## Using


```python
def runit(parameters, h,dt):
  make_tough_input(h,dt,parameters)
  sp.call(['TH','millstone_input.py',str(h),str(dt)])
  return process_results_for_testing()
```

## License
