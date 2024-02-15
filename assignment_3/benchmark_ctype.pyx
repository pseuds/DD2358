import cython

@cython.boundscheck(False)  # deactivate bounds checking
def run_copy(a, b, c, int size):
    cdef int j 
    for j in range(size):
        c[j] = a[j]

@cython.boundscheck(False)  # deactivate bounds checking
def run_scale(a, b, c, int size):
    cdef int j 
    cdef float scalar = 2.0
    for j in range(size):
        b[j] = scalar * c[j]

@cython.boundscheck(False)  # deactivate bounds checking
def run_sum(a, b, c, int size):
    cdef int j 
    for j in range(size):
        c[j] = a[j] + b[j]

@cython.boundscheck(False)  # deactivate bounds checking
def run_triad(a, b, c, int size):
    cdef int j 
    cdef float scalar = 2.0
    for j in range(size):
        a[j] = b[j] + scalar * c[j]