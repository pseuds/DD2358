def gauss_seidel(f):

    cdef unsigned int rows, cols, i, j
    rows = f.shape[0]
    cols = f.shape[1]
    
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            f[i, j] = 0.25 * (f[i, j + 1] + f[i, j - 1] + f[i + 1, j] + f[i - 1, j])
    
    return f