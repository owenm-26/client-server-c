def get_response_times(filepath):
    with open(filepath, 'r') as f:
        content = f.readlines()
        response_lines = [line for line in content if line.startswith('T') and 'R' in line]

    # get sum of all times in use
    response_times = []
    for line in response_lines:
        # build total response time
        completion = float(line.split(':')[1].split(',')[-1])
        sent = float(line.split(':')[1].split(',')[0])
        response_times.append(completion - sent)
    
    # return response_times
    return np.array(response_times)  # Convert to numpy array

def plot_cdf(data, ax, title, min_time, max_time):  # Added min_time and max_time as parameters
    # Sort data for CDF
    sorted_data = np.sort(data)
    # Calculate CDF values (using n+1 to avoid division by zero)
    cdf = np.arange(1, len(sorted_data) + 1) / (len(sorted_data))
    
    # Plot CDF
    ax.plot(sorted_data, cdf, 'b-', label='CDF')
    
    # Calculate and plot average
    avg = np.mean(data)
    ax.axvline(x=avg, color='r', linestyle='--', 
              label=f'Mean: {avg:.3f}s')
    
    # Calculate and plot 99th percentile
    percentile_99 = np.percentile(data, 99)
    ax.axvline(x=percentile_99, color='g', linestyle='--', 
              label=f'99th %ile: {percentile_99:.3f}s')
    
    ax.set_title(title)
    ax.set_xlabel('Response Time (seconds)')
    ax.set_ylabel('CDF')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    
    # Set consistent axis limits
    ax.set_xlim(min_time, max_time)
    ax.set_ylim(0, 1)

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    sjn_response_times = get_response_times('./outputs_b/sjn_40.txt')
    fifo_response_times = get_response_times('./outputs_b/40.txt')

    # Find overall min and max for consistent axes
    min_time = min(sjn_response_times.min(), fifo_response_times.min())
    max_time = max(sjn_response_times.max(), fifo_response_times.max())

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot both CDFs
    plot_cdf(sjn_response_times, ax1, "SJN Response Time CDF", min_time, max_time)
    plot_cdf(fifo_response_times, ax2, "FIFO Response Time CDF", min_time, max_time)

    plt.show()

    # plt.tight_layout()
    # plt.savefig('response_time_cdfs.png')
    # plt.close()

    # Print statistics
    for name, data in [("SJN", sjn_response_times), ("FIFO", fifo_response_times)]:
        print(f"\n{name} Statistics:")
        print(f"Average Response Time: {np.mean(data):.3f}s")
        print(f"99th Percentile: {np.percentile(data, 99):.3f}s")
        print(f"Median: {np.median(data):.3f}s")
        print(f"Min: {np.min(data):.3f}s")
        print(f"Max: {np.max(data):.3f}s")