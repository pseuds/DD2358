import pytest
from JuliaSet import calc_pure_python

def test_julia():
    assert calc_pure_python(desired_width=1000, max_iterations=300) == 33219980

# How would you implement the unit test with the possibility of having a different number of iterations and grid points?
'''
How would you implement the unit test with the possibility of having a different number of iterations and grid points?
Compare the current implementation of the Julia Set Code with 
reference implementations or established libraries that have the Julia Set Code implementations.
'''
