from scipy.linalg import blas
from dgemm import run
import numpy as np

def test_dgemm():
    N, A, B, pred = run(5)
    exp = np.zeros((N, N), dtype=np.float64)
    exp = blas.dgemm(1.0, A, B, 0.0, exp)
    assert np.allclose(exp, pred)
