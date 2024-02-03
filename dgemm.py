import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

def matrix_init(size):
    return np.random.rand(size, size).astype(np.float64)

def run(size):
    A = matrix_init(size)
    B = matrix_init(size)
    C = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            for k in range(size):
                C[i, j] += A[i, k] * B[k, j]
    return size, A, B, C

def matmul(size):
    A = matrix_init(size)
    B = matrix_init(size)
    return size, A, B, np.matmul(A, B)

def plot_times(sizes, times, oper):

    plt.bar(sizes, times, color='blue')

    plt.xlabel('Matrix Size N')
    plt.ylabel('Time (s)')
    plt.title(f'Time vs Matrix Size for {oper}')
    plt.show()

# Calculation of FLOPS: For matrix multiplication between one column of A and one row of B, there are N multiplications and N additions, making it 2N FLOPS.
#                       There are N rows for B, and there are N columns of A. Therefore, the total number of FLOPS will be 2N * N * N = 2N^3.
def calculate_flops_per_second(size, time):
    return ((2 * (size ** 3)) / time) / 10 ** 9

if __name__ == "__main__":

    dot_times = []
    matmul_times = []
    stds = []
    sizes = [i for i in range(2, 31)]
    num_runs = 50

    for size in sizes:
        dot_std_measure = []
        dot_time_count = 0
        matmul_time_count = 0
        for _ in range(num_runs):
            start_time = timer()
            run(size)
            end_time = timer()
            dot_std_measure.append(end_time - start_time)
            dot_time_count += end_time - start_time
            start_time = timer()
            matmul(size)
            end_time = timer()
            matmul_time_count += end_time - start_time
        stds.append(np.std(dot_std_measure))
        dot_times.append(dot_time_count / num_runs)
        matmul_times.append(matmul_time_count / num_runs)

    flops_per_second = [calculate_flops_per_second(size, time) for size, time in zip(sizes, dot_times)]
    print("Standard Deviations: ", stds, '\n')
    print("Giga FLOPS per second: ", flops_per_second)
    print("Theoretical Peak for current processor (AMD Ryzen 7 4800H): 371,2 Giga FLOPs/s")
    plot_times(sizes, dot_times, 'Pseudo Code')
    plot_times(sizes, matmul_times, 'np.matmul')

'''
How does the computational performance vary with increasing the size of the matrices, and why so?
Looking into the execution times of the DGEMM operation, we can see that the times exponentially increases
as the matrix size increases. This is due to the nature of matrix multiplication, which in the pseudo code,
has 3 nested loops and hence its time complexity is O(N^3). Because of this, we can also deduce that since
more time is taken to do matrix multiplication for matrices that have bigger sizes, therefore the 
computational performace decreases with increasing matrix size.

How do the FLOPS/s you measured compare to the theoretical peak of your processor?
The FLOPS/s, even with a higher matrix size, is insiginificantly slower than the theorical peak of my processor (AMD Ryzen 7 4800H).

Compare the performance results with the numpy matmul operation (that uses a BLAS library).
The numpy matnul operation, though it follows the trend of increasing in computation time exponentially as the matrix size increases,
the time it takes to run the operation is significantly faster than the previous implementation.
'''
