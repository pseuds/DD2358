from timeit import default_timer as timer
from array import array
import matplotlib.pyplot as plt
import math
import sys

def list_init(size):

    a = [1.0] * size
    b = [2.0] * size
    c = [0.0] * size

    return a, b, c

def array_init(size):

    a = array('f', [1.0] * size)
    b = array('f', [2.0] * size)
    c = array('f', [0.0] * size)

    return a, b, c

def run_benchmark(a, b, c, size):

    times = [None for _ in range(4)]
    scalar = 2.0

    # copy
    times[0] = timer()
    for j in range(size):
        c[j] = a[j]
    times[0] = timer() - times[0]

    # scale
    times[1] = timer()
    for j in range(size):
        b[j] = scalar * c[j]
    times[1] = timer() - times[1]
     
    # sum
    times[2] = timer()
    for j in range(size):
        c[j] = a[j] + b[j]
    times[2] = timer() - times[2]

     # triad
    times[3] = timer()
    for j in range(size):
        a[j] = b[j] + scalar * c[j]
    times[3] = timer() - times[3]

    return times

def calculate_bandwidth(size, times):

    copy_bandwidth = (2 * size * sys.getsizeof(float)) / times[0]
    scale_bandwidth = (3 * size * sys.getsizeof(float)) / times[1]
    sum_bandwidth = (2 * size * sys.getsizeof(float)) / times[2]
    triad_bandwidth = (3 * size * sys.getsizeof(float)) / times[3]

    return copy_bandwidth, scale_bandwidth, sum_bandwidth, triad_bandwidth

def plot_benchmark(array_time, lists_time, sizes, op_type, y_lim):

    log_sizes = [math.log10(size) for size in sizes]

    plt.plot(log_sizes, array_time, label='Array')
    plt.plot(log_sizes, lists_time, label='List')

    plt.xlabel('Log10(Array Size)')
    plt.ylabel('Bandwidth')
    plt.ylim(0, y_lim)
    plt.title(f'STREAM Benchmark ({op_type})')
    plt.legend(loc='upper left')
    plt.show()
    
if __name__ == "__main__":

    array_total = []
    list_total = []
    sizes = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]

    runs = 20

    for r in range(runs):
        array_run = []
        list_run = []
        for size in sizes:
            array_a, array_b, array_c = array_init(size)
            list_a, list_b, list_c = list_init(size)

            array_times = run_benchmark(array_a, array_b, array_c, size)
            list_times = run_benchmark(list_a, list_b, list_c, size)

            array_bandwidth = calculate_bandwidth(size, array_times)
            list_bandwidth = calculate_bandwidth(size, list_times)

            array_run.append(array_bandwidth)
            list_run.append(list_bandwidth)
        array_total.append(array_run)
        list_total.append(list_run)

    avg_array_0 = [sum([array_total[k][i][0] for k in range(len(array_total))])/runs for i in range(len(array_total[0]))]
    avg_array_1 = [sum([array_total[k][i][1] for k in range(len(array_total))])/runs for i in range(len(array_total[0]))]
    avg_array_2 = [sum([array_total[k][i][2] for k in range(len(array_total))])/runs for i in range(len(array_total[0]))]
    avg_array_3 = [sum([array_total[k][i][3] for k in range(len(array_total))])/runs for i in range(len(array_total[0]))]
    avg_list_0 = [sum([list_total[k][i][0] for k in range(len(list_total))])/runs for i in range(len(list_total[0]))]
    avg_list_1 = [sum([list_total[k][i][1] for k in range(len(list_total))])/runs for i in range(len(list_total[0]))]
    avg_list_2 = [sum([list_total[k][i][2] for k in range(len(list_total))])/runs for i in range(len(list_total[0]))]
    avg_list_3 = [sum([list_total[k][i][3] for k in range(len(list_total))])/runs for i in range(len(list_total[0]))]

    y_lim = max(avg_list_0+avg_list_1+avg_list_2+avg_list_3)*1.10

    plot_benchmark([i for i in avg_array_0], [j for j in avg_list_0], sizes, 'Copy', y_lim=y_lim)
    plot_benchmark([i for i in avg_array_1], [j for j in avg_list_1], sizes, 'Scale', y_lim=y_lim)
    plot_benchmark([i for i in avg_array_2], [j for j in avg_list_2], sizes, 'Sum', y_lim=y_lim)
    plot_benchmark([i for i in avg_array_3], [j for j in avg_list_3], sizes, 'Triad', y_lim=y_lim)

    print(avg_array_0)
    print(avg_list_0)
    print(avg_array_1)
    print(avg_list_1)
    print(avg_array_2)
    print(avg_list_2)
    print(avg_array_3)
    print(avg_list_3)

'''
How does the bandwidth vary when increasing the STREAM_ARRAY_SIZE, and why?
As the array size increases, the bandwidth converges to an upper limit. This is because the available memory bandwidth is limited, to the rate at which data can be transferred between the processor and memory becomes a bottleneck.

How do the different implementation bandwidths compare to each other?
The memory bandwidth seems to be a lot more for Python Lists in all array sizes as compared to arrays.
'''
