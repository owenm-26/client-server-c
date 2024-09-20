/*******************************************************************************
* CPU Clock Measurement Using RDTSC
*
* Description:
*     This C file provides functions to compute and measure the CPU clock using
*     the `rdtsc` instruction. The `rdtsc` instruction returns the Time Stamp
*     Counter, which can be used to measure CPU clock cycles.
*
* Author:
*     Owen Mariani
*
* Affiliation:
*     Boston University
*
* Creation Date:
*     September 10, 2023
*
* Last Update:
*     September 14, 2024
*
* Notes:
*     Ensure that the platform supports the `rdtsc` instruction before using
*     these functions. Depending on the CPU architecture and power-saving
*     modes, the results might vary. Always refer to the CPU's official
*     documentation for accurate interpretations.
*
*******************************************************************************/

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

#include "timelib.h"

int main (int argc, char ** argv)
{
	/*uint64_t clock;
	get_clocks(clock);
	printf("get_clock(clock): %llu\n", clock);
	
	int sleep;
	sleep = get_elapsed_sleep(1, 100);
	printf("get_elapsed_sleep(): %d\n", sleep);

	int busy;
	busy = get_elapsed_busywait(2,100);
	printf("get_elapsed_busywait(): %d\n", busy);
	*/

	if (argc != 4){
		printf("Incorrect number of parameters. Please enter exactly 3. The first is seconds, second is nanoseconds, and the third is either 's' or 'b' for sleep or busy.");
		return -1;
	}
	char *mode = argv[3];
	if (strcmp(mode, "s")!=0  && strcmp(mode, "b")!=0) {
		printf("Invalid third paramter. Should be 's' for sleep or 'b' for busy.");
		return -1;
	}
	uint64_t elapsed_time;
	char *method;
	long sec = strtol(argv[1], NULL, 10);
	long nsec = strtol(argv[2], NULL, 10);
	
	if (strcmp(mode, "s")==0) {
		elapsed_time = get_elapsed_sleep(sec, nsec);
		method = "SLEEP";	
	}
	if (strcmp(mode, "b")==0) {
		elapsed_time = get_elapsed_busywait(sec, nsec);
		method = "BUSYWAIT";
	}
	
	double milliseconds = (double)(sec) * 1000 + (double)(nsec)/1000000;
	milliseconds = milliseconds * 1000;
	//calculate clock speed
	double clock_speed = (double)elapsed_time / milliseconds;
	// format and print results
	printf("WaitMethod: %s\nWaitTime: %ld %ld\nClocksElapsed: %lu\nClockSpeed: %lf\n", method, sec, nsec, elapsed_time, clock_speed); 
	return EXIT_SUCCESS;
}

