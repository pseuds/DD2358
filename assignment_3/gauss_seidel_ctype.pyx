def gauss_seidel(f):
    newf = f.copy()

    cdef unsigned int rows, cols, i, j
    rows = f.shape[0]
    cols = f.shape[1]
    
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            newf[i, j] = 0.25 * (newf[i, j + 1] + newf[i, j - 1] + newf[i + 1, j] + newf[i - 1, j])
    
    return newf
