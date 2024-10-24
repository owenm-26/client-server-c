#!/bin/bash

# Create the outputs folder if it doesn't exist
mkdir -p outputs_b

output_dir="outputs_b"


# Loop from 10 to 19 (adjust based on your needs)

for i in {22..40..2}
do
    # Run the server command and redirect output to a numbered file
    unbuffer ./build/server_pol -w 2 -q 100 -p SJN 2223 > $output_dir/sjn_$i.txt &

    # Capture the PID of the server process
    SERVER_PID=$!

    # Sleep for 2 seconds to ensure the server has time to start properly
    sleep 0.1

    # Run the client command with the current index for the -a flag
    ./client -a "$i" -s 20 -n 1500 2223 > /dev/null 
    
    # Stop the server after the client command has run
    kill $SERVER_PID

    # Wait for the server to shut down
    wait $SERVER_PID
done

echo "All runs completed. Outputs saved in the $output_dir"
