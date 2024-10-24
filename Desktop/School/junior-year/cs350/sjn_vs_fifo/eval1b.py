def get_utlization_of_run(filepath):
    with open(filepath, 'r') as f:
        content = f.readlines()
        response_lines = [line for line in content if line.startswith('T') and 'R' in line]

    # Get first and last response lines
    first_response = response_lines[0]
    last_response = response_lines[-1]

    # get sum of all times in use
    busy_time = 0
    total_response_time = 0
    for line in response_lines:
        # build total busy time
        req_len = line.split(':')[1].split(',')[1]
        busy_time += float(req_len)

        # build total response time
        completion = float(line.split(':')[1].split(',')[-1])
        sent = float(line.split(':')[1].split(',')[0])
        total_response_time += completion - sent

    # average resp time
    avg_resp_time = total_response_time / 1500

    last_number_last_response = float(last_response.split(',')[-1])
    first_number_first_response = float(first_response.split(':')[1].split(',')[0])

    # compute time window
    total_run_time = last_number_last_response - first_number_first_response

    # return utilization
    return busy_time / total_run_time, avg_resp_time

def plot_utilization_vs_resp_time(utilizations, avg_resp_times):
    import matplotlib.pyplot as plt
    import numpy as np

    # Convert to numpy arrays for easier calculations
    fifo_utils, sjn_utils = np.array(utilizations[0]), np.array(utilizations[1])
    fifo_resp, sjn_resp = np.array(avg_resp_times[0]), np.array(avg_resp_times[1])

    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot both curves
    plt.plot(fifo_utils, fifo_resp, 'b.-', label='FIFO', linewidth=2, markersize=8)
    plt.plot(sjn_utils, sjn_resp, 'r.-', label='SJN', linewidth=2, markersize=8)
    
    # Add labels and title
    plt.xlabel('System Utilization')
    plt.ylabel('Average Response Time (seconds)')
    plt.title('System Utilization vs Average Response Time: FIFO vs SJN')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

    # Calculate performance difference
    avg_improvement = np.mean((fifo_resp - sjn_resp) / fifo_resp * 100)
    max_improvement = np.max((fifo_resp - sjn_resp) / fifo_resp * 100)

    # Print analysis
    print(f"\nPerformance Analysis:")
    print(f"Average improvement with SJN: {avg_improvement:.1f}%")
    print(f"Maximum improvement with SJN: {max_improvement:.1f}%")
    print(f"SJN consistently performs {'better' if avg_improvement > 0 else 'worse'} than FIFO")

if __name__ == "__main__":

    # get all fifo utilizations and avg resp times
    fifo_utilizations = []
    fifo_avg_resp_times = []
    for i in range(22, 41, 2):
        utilization, avg_resp_time = get_utlization_of_run(f'./outputs_b/{i}.txt')
        fifo_utilizations.append(utilization)
        fifo_avg_resp_times.append(avg_resp_time)

    
    # get all sjn utilizations and avg resp times
    print()
    sjn_utilizations = []
    sjn_avg_resp_times = []
    for i in range(22, 41, 2):
        utilization, avg_resp_time = get_utlization_of_run(f'./outputs_b/sjn_{i}.txt')
        sjn_utilizations.append(utilization)
        sjn_avg_resp_times.append(avg_resp_time)

    # print()
    # for i in range(len(sjn_utilizations)):
    #     print(fifo_utilizations[i], '-----', sjn_utilizations[i], '==', fifo_utilizations[i] > sjn_utilizations[i])
        # print(fifo_avg_resp_times[i], '----', sjn_avg_resp_times[i], '==', fifo_avg_resp_times[i] > sjn_avg_resp_times[i])

    utilizations = [fifo_utilizations, sjn_utilizations]
    avg_resp_times = [fifo_avg_resp_times, sjn_avg_resp_times]

    plot_utilization_vs_resp_time(utilizations, avg_resp_times)


    

    

    