#!/bin/bash

# Output file to store the results
output_file="eval1-fifo-hi.txt"

# Initialize or clear the output file
echo "Timing results for FIFO policy" > "$output_file"

# Run the command 10 times
for ((i=1; i<=10; i++))
do
    echo "Run $i..." >> "$output_file"
    
    # Run the server in the background, and the client, and capture /usr/bin/time output into the output file
    
    /usr/bin/time -v ./build/server_pol -w 2 -q 100 -p FIFO 2229 2>> "$output_file" > /dev/null & ./client -a 40 -s 20 -n 1500 2229 > /dev/null

    # Wait for the server process to finish
    wait

    # Append a separator for each run
    echo "------------------------------" >> "$output_file"
done

echo "Results written to $output_file"
