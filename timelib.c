/*******************************************************************************
* Time Functions Library (implementation)
*
* Description:
*     A library to handle various time-related functions and operations.
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
*     Ensure to link against the necessary dependencies when compiling and
*     using this library. Modifications or improvements are welcome. Please
*     refer to the accompanying documentation for detailed usage instructions.
*
*******************************************************************************/

#include "timelib.h"
#include <time.h>

/* Utility function to add two timespec structures together. The input
 * parameter a is updated with the result of the sum. */
void timespec_add (struct timespec * a, struct timespec * b)
{
	/* Try to add up the nsec and see if we spill over into the
	 * seconds */
	time_t addl_seconds = b->tv_sec;
	a->tv_nsec += b->tv_nsec;
	if (a->tv_nsec > NANO_IN_SEC) {
		addl_seconds += a->tv_nsec / NANO_IN_SEC;
		a->tv_nsec = a->tv_nsec % NANO_IN_SEC;
	}
	a->tv_sec += addl_seconds;
}

/* Utility function to compare two timespec structures. It returns 1
 * if a is in the future compared to b; -1 if b is in the future
 * compared to a; 0 if they are identical. */
int timespec_cmp(struct timespec *a, struct timespec *b)
{
	if(a->tv_sec == b->tv_sec && a->tv_nsec == b->tv_nsec) {
		return 0;
	} else if((a->tv_sec > b->tv_sec) ||
		  (a->tv_sec == b->tv_sec && a->tv_nsec > b->tv_nsec)) {
		return 1;
	} else {
		return -1;
	}
}

/* Return the number of clock cycles elapsed when waiting for
 * wait_time seconds using sleeping functions */
uint64_t get_elapsed_sleep(long sec, long nsec)
{
	uint64_t start_time;
	get_clocks(start_time);
	struct timespec req, remaining;
	req.tv_sec = sec;
	req.tv_nsec = nsec;
	nanosleep(&req, &remaining);
	uint64_t after_time;
	get_clocks(after_time);
	return after_time - start_time;
}

/* Return the number of clock cycles elapsed when waiting for
 * wait_time seconds using busy-waiting functions */
uint64_t get_elapsed_busywait(long sec, long nsec)
{
	struct timespec begin_timestamp;
	clock_gettime(CLOCK_MONOTONIC, &begin_timestamp);
	
	struct timespec end_timestamp;
	end_timestamp.tv_sec = sec;
	end_timestamp.tv_nsec = nsec;
	timespec_add(&end_timestamp, &begin_timestamp);

	uint64_t start_time;
	get_clocks(start_time);
	
	struct timespec current_timestamp = begin_timestamp;
	while(timespec_cmp(&end_timestamp, &current_timestamp) == 1){
		clock_gettime(CLOCK_MONOTONIC, &current_timestamp);
	}
	uint64_t end_time;
	get_clocks(end_time);
	return end_time - start_time;
}
/* Busywait for the amount of time described via the delay
 * parameter */
uint64_t busywait_timespec(struct timespec delay)
{
	return get_elapsed_busywait(delay.tv_sec, delay.tv_nsec);
}


