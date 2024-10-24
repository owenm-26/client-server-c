#!/bin/bash

# Output file to store the results
output_file="eval1-sjnt-hi.txt"

# Initialize or clear the output file
echo "Timing results for SJN policy" > "$output_file"

# Run the command 10 times
for ((i=1; i<=10; i++))
do
    echo "Run $i..." >> "$output_file"
    
    # Run the server in the background, and the client, and capture /usr/bin/time output into the output file
    /usr/bin/time -v ./build/server_pol -w 2 -q 100 -p SJN 2226 2>> "$output_file" > /dev/null & server_pid=$!

    sleep 1 
    
    ./client -a 10 -s 20 -n 150 2226 > /dev/null 

    wait $server_pid

    # Wait for the server process to finish
    wait

    # Append a separator for each run
    echo "------------------------------" >> "$output_file"
done

echo "Results written to $output_file"

