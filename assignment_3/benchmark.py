def run_copy(a, b, c, size):
    for j in range(size):
        c[j] = a[j]

def run_scale(a, b, c, size):
    scalar = 2.0
    for j in range(size):
        b[j] = scalar * c[j]

def run_sum(a, b, c, size):
    for j in range(size):
        c[j] = a[j] + b[j]

def run_triad(a, b, c, size):
    scalar = 2.0
    for j in range(size):
        a[j] = b[j] + scalar * c[j]