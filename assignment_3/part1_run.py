import benchmark 
import benchmark_ctype 
from array import array
import math
import matplotlib.pyplot as plt
from timeit import default_timer as timer


def list_init(size):

    a = [float(1.0)] * size
    b = [float(2.0)] * size
    c = [float(0.0)] * size

    return a, b, c

def array_init(size):

    a = array('f', [1.0] * size)
    b = array('f', [2.0] * size)
    c = array('f', [0.0] * size)

    return a, b, c

def calculate_bandwidth(size, times):

    float_size = 4

    copy_bandwidth = (2 * size * float_size) / times[0]
    scale_bandwidth = (3 * size * float_size) / times[1]
    sum_bandwidth = (2 * size * float_size) / times[2]
    triad_bandwidth = (3 * size * float_size) / times[3]

    return copy_bandwidth, scale_bandwidth, sum_bandwidth, triad_bandwidth

def run_ctype_benchmark(a, b, c, size):
    timings = [float(0) for i in range(4)]

    timings[0] = timer()
    benchmark_ctype.run_copy(a, b, c, size)
    timings[0] = timer() - timings[0]

    timings[1] = timer()
    benchmark_ctype.run_scale(a, b, c, size)
    timings[1] = timer() - timings[1]

    timings[2] = timer()
    benchmark_ctype.run_sum(a, b, c, size)
    timings[2] = timer() - timings[2]

    timings[3] = timer()
    benchmark_ctype.run_triad(a, b, c, size)
    timings[3] = timer() - timings[3]

    return timings

def run_benchmark(a, b, c, size):
    timings = [float(0) for i in range(4)]

    timings[0] = timer()
    benchmark.run_copy(a, b, c, size)
    timings[0] = timer() - timings[0]

    timings[1] = timer()
    benchmark.run_scale(a, b, c, size)
    timings[1] = timer() - timings[1]

    timings[2] = timer()
    benchmark.run_sum(a, b, c, size)
    timings[2] = timer() - timings[2]

    timings[3] = timer()
    benchmark.run_triad(a, b, c, size)
    timings[3] = timer() - timings[3]

    return timings

def plot_benchmark(old_time, new_time, sizes, op_type, y_lim):

    log_sizes = [math.log10(size) for size in sizes]

    plt.plot(log_sizes, old_time, label='Original')
    plt.plot(log_sizes, new_time, label='Cython')

    plt.xlabel('Log10(Array Size)')
    plt.ylabel('Bandwidth')
    plt.ylim(0, y_lim)
    plt.title(f'STREAM Benchmark ({op_type})')
    plt.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":

    old_total = []
    new_total = []
    sizes = [1, 10, 100, 1000, 10000, 100000, 1000000]

    runs = 20

    for r in range(runs):
        old_run = []
        new_run = []
        for size in sizes:
            array_a, array_b, array_c = array_init(size)
            old_timings = run_benchmark(array_a, array_b, array_c, size)
            old_bandwidth = calculate_bandwidth(size, old_timings)

            array_a, array_b, array_c = array_init(size)
            new_timings = run_ctype_benchmark(array_a, array_b, array_c, size)
            new_bandwidth = calculate_bandwidth(size, new_timings)

            old_run.append(old_bandwidth)
            new_run.append(new_bandwidth)
            
        old_total.append(old_run)
        new_total.append(new_run)
    
    avg_old_0 = [sum([old_total[k][i][0] for k in range(len(old_total))])/runs for i in range(len(old_total[0]))]
    avg_old_1 = [sum([old_total[k][i][1] for k in range(len(old_total))])/runs for i in range(len(old_total[0]))]
    avg_old_2 = [sum([old_total[k][i][2] for k in range(len(old_total))])/runs for i in range(len(old_total[0]))]
    avg_old_3 = [sum([old_total[k][i][3] for k in range(len(old_total))])/runs for i in range(len(old_total[0]))]
    avg_new_0 = [sum([new_total[k][i][0] for k in range(len(new_total))])/runs for i in range(len(new_total[0]))]
    avg_new_1 = [sum([new_total[k][i][1] for k in range(len(new_total))])/runs for i in range(len(new_total[0]))]
    avg_new_2 = [sum([new_total[k][i][2] for k in range(len(new_total))])/runs for i in range(len(new_total[0]))]
    avg_new_3 = [sum([new_total[k][i][3] for k in range(len(new_total))])/runs for i in range(len(new_total[0]))]

    y_lim = max(avg_new_0+avg_new_1+avg_new_2+avg_new_3+avg_old_0+avg_old_1+avg_old_2+avg_old_3)*1.10

    plot_benchmark([i for i in avg_old_0], [j for j in avg_new_0], sizes, 'Copy', y_lim=y_lim)
    plot_benchmark([i for i in avg_old_1], [j for j in avg_new_1], sizes, 'Scale', y_lim=y_lim)
    plot_benchmark([i for i in avg_old_2], [j for j in avg_new_2], sizes, 'Sum', y_lim=y_lim)
    plot_benchmark([i for i in avg_old_3], [j for j in avg_new_3], sizes, 'Triad', y_lim=y_lim)

    print("avg_old_0 =", avg_old_0)
    print("avg_old_1 =", avg_old_1)
    print("avg_old_2 =", avg_old_2)
    print("avg_old_3 =", avg_old_3)
    print("avg_new_0 =", avg_new_0)
    print("avg_new_1 =", avg_new_1)
    print("avg_new_2 =", avg_new_2)
    print("avg_new_3 =", avg_new_3)