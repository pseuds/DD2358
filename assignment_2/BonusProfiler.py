import psutil
from functools import wraps
import matplotlib.pyplot as plt
import pandas as pd

class CPUProfile:

    # Initialize number of intervals and list of CPU times
    def __init__(self, num_data=1):
        self.num_data = num_data
        self.cpu = []

    # Profiler function
    def profile(self, fn):

        # Using wraps for wrap functionality
        @wraps(fn)
        def measure_cpu_percentage(*args, **kwargs):
            for _ in range(self.num_data):
                cpu_percentages = psutil.cpu_percent(interval=1, percpu=True)
                self.cpu.append(cpu_percentages)
                result = fn(*args, **kwargs)

            # Plot CPU percentages
            self.plotCPU()

            # Create summary table for CPU percentages
            self.sum_table()

            return result
        
        return measure_cpu_percentage

    # Plotting Function
    def plotCPU(self):
        for cpu_num in range(len(self.cpu[0])):
            cpu_values = []
            for cpu_percentages in self.cpu:
                cpu_values.append(cpu_percentages[cpu_num])
            plt.plot([i for i in range(len(self.cpu))], cpu_values, label=f'Core {cpu_num + 1}')

        plt.xlabel('Number of Runs')
        plt.ylabel('CPU Usage (%)')
        plt.legend()
        plt.title('CPU Usage per Core Over Number of Runs')
        plt.show()

    # Summary Table Function
    def sum_table(self):
        df = pd.DataFrame(self.cpu, columns=[f'Core_{i + 1}' for i in range(psutil.cpu_count())])
        print("\nSummary Table:")
        print(df, "\n")
