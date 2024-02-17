import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
#from line_profiler import profile
#import gauss_seidel_ctype
import torch
from torch import (roll, zeros)
#import cupy as cp
import h5py

#@profile
def gauss_seidel(f):
    newf = f.copy()
    
    for i in range(1, newf.shape[0] - 1):
        for j in range(1, newf.shape[1] - 1):
            newf[i, j] = 0.25 * (newf[i, j + 1] + newf[i, j - 1] + newf[i + 1, j] + newf[i - 1, j])
    
    return newf

def gauss_seidel_torch(f):
    newf = f.clone()

    return ((roll(newf, 0, 1) + roll(newf, 0, 1) + roll(newf, 0, 0) + roll(newf, 0, 0)) * 0.25)

#def gauss_seidel_cupy(f):
#    newf = f.copy()
#
#   return ((cp.roll(newf, 0, 1) + cp.roll(newf, 0, 1) + cp.roll(newf, 0, 0) + cp.roll(newf, 0, 0)) * 0.25)

def gauss_seidel_torch(f):
    newf = f.clone()

    return ((roll(newf, 0, 1) + roll(newf, 0, 1) + roll(newf, 0, 0) + roll(newf, 0, 0)) * 0.25)

def initialize_grid(size):
    grid = np.zeros((size, size))
    grid[1: -1, 1: -1] = np.random.rand(size - 2, size - 2)
    return grid

def initialize_grid_torch(size):
    grid = zeros((size, size))
    grid[1: -1, 1: -1] = torch.rand(size - 2, size - 2)
    return grid

#def initialize_grid_cupy(size):
#    grid = cp.zeros((size, size))
#    grid[1: -1, 1: -1] = cp.random.rand(size - 2, size - 2)
#    return grid

def plot_gauss(grid_size, times):

    plt.plot(grid_size, times)

    plt.xlabel('Grid Size')
    plt.ylabel('Run Time')
    plt.title('Run Time of Gauss-Seidel iteration for varying grid sizes')
    plt.show()

def plot_cython_gauss(grid_size, times, cytimes):

    plt.plot(grid_size, times, label='Original')
    plt.plot(grid_size, cytimes, label='With Cython')

    plt.xlabel('Grid Size')
    plt.ylabel('Run Time')
    plt.title('Run Time of Gauss-Seidel iteration for varying grid sizes')
    plt.legend(loc='upper left')
    plt.show()

def plot_torch_gauss(grid_size, times, torchtimes, ylim):

    plt.plot(grid_size, times, label='Original')
    plt.plot(grid_size, torchtimes, label='With PyTorch')

    plt.xlabel('Grid Size')
    plt.ylabel('Run Time')
    plt.xlim(5, 100)
    plt.ylim(0, ylim)
    plt.title('Run Time of Gauss-Seidel iteration for varying grid sizes')
    plt.legend(loc='upper left')
    plt.show()

def plot_torch_cupy_gauss(grid_size, times, torchtimes, cupytimes, ylim):

    plt.plot(grid_size, times, label='Original')
    plt.plot(grid_size, torchtimes, label='With PyTorch')
    plt.plot(grid_size, cupytimes, label='With CuPy')

    plt.xlabel('Grid Size')
    plt.ylabel('Run Time')
    plt.xlim(5, 101)
    plt.ylim(0, ylim)
    plt.title('Run Time of Gauss-Seidel iteration for varying grid sizes')
    plt.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":

    '''
    
                    Task 2.1
    ______________________________________

    grid_size = [i for i in range(2, 201)]
    times = []
    for size in grid_size:
        grid = initialize_grid(size)
        start_time = timer()
        grid = gauss_seidel(grid)
        times.append(timer() - start_time)

    plot_gauss(grid_size, times)

    
                    Task 2.2
    ______________________________________

    grid_size = 1000
    start_time = timer()
    grid = initialize_grid(grid_size)
    gauss_seidel(grid)
    time = timer() - start_time
    print(gauss_seidel.__name__ + " took", time, "seconds for a 1000 x 1000 grid")

    
                    Task 2.4
    ______________________________________

    grid_size = [i for i in range(2, 201)]
    times = []
    cytimes = []
    for size in grid_size:
        grid = initialize_grid(size)
        start_time = timer()
        gauss_seidel(grid)
        times.append(timer() - start_time)

        start_time = timer()
        gauss_seidel_ctype.gauss_seidel(grid)
        cytimes.append(timer() - start_time)

    plot_cython_gauss(grid_size, times, cytimes)

    
                    Task 2.5
    ______________________________________
    grid_size = [i for i in range(2, 101)]
    torchtimes = []
    for size in grid_size:
        grid_torch = initialize_grid_torch(size)

        grid_torch = grid_torch.cuda()
        start_time = timer()
        gauss_seidel_torch(grid_torch)
        torchtimes.append(timer() - start_time)

    plot_gauss(grid_size, torchtimes)

    
                    Task 2.6
    ______________________________________
    grid_size = [i for i in range(2, 101)]
    cupytimes = []
    for size in grid_size:
        grid_cupy = initialize_grid_cupy(size)

        start_time = timer()
        cp.cuda.Stream.null.synchronize()
        gauss_seidel_cupy(grid_cupy)
        cupytimes.append(timer() - start_time)

    plot_gauss(grid_size, cupytimes)
    

                    Task 2.7
    ______________________________________
    grid_size = [i for i in range(2, 101)]
    times = []
    torchtimes = []
    cupytimes = []
    for size in grid_size:
        grid_ori = initialize_grid(size)
        grid_torch = initialize_grid_torch(size)
        grid_cupy = initialize_grid_cupy(size)

        start_time = timer()
        gauss_seidel(grid_ori)
        times.append(timer() - start_time)

        grid_torch = grid_torch.cuda()
        start_time = timer()
        gauss_seidel_torch(grid_torch)
        torchtimes.append(timer() - start_time)

        start_time = timer()
        cp.cuda.Stream.null.synchronize()
        gauss_seidel_cupy(grid_cupy)
        cupytimes.append(timer() - start_time)

    plot_torch_cupy_gauss(grid_size, times, torchtimes, cupytimes, ylim=max(times))

    
                    Task 2.8
    ______________________________________
    grid_size = 6
    grid = initialize_grid(grid_size)
    newgrid = gauss_seidel(grid)

    with h5py.File('newgrid.hdf5', 'w') as f:
        f.create_dataset('New Grid', data=newgrid)

    with h5py.File('newgrid.hdf5', 'r') as f:
        read_grid = f['New Grid'][:]

    print(newgrid)
    print(read_grid)
    '''

    print("Assignment III Question 2 Done")