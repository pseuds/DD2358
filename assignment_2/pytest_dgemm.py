from scipy.linalg import blas
from dgemm import run_numpyarray, run_pyarray, run_pylist
import numpy as np

def test_dgemm_numpy():
    N, A, B, pred = run_numpyarray(5)
    exp = np.zeros((N, N), dtype=np.float64)
    exp = blas.dgemm(1.0, A, B, 0.0, exp)
    assert np.allclose(exp, pred)

def test_dgemm_array():
    N, A, B, pred = run_pyarray(5)
    A = np.array(A, dtype=np.float64)
    B = np.array(B, dtype=np.float64)
    exp = np.zeros((N, N), dtype=np.float64)
    exp = blas.dgemm(1.0, A, B, 0.0, exp)
    assert np.allclose(exp, pred)

def test_dgemm_list():
    N, A, B, pred = run_pylist(5)
    exp = np.zeros((N, N), dtype=np.float64)
    exp = blas.dgemm(1.0, A, B, 0.0, exp)
    assert np.allclose(exp, pred)