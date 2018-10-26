import HydrogeologyTesting as hgtest

problems = [
    hgtest.mechanics_constant,
]
for problem in problems:
    def mycode(params, h,dt):
        " An exact code "
        return problem(params)
    etr = hgtest.ExactTestRunner(problem,mycode)
