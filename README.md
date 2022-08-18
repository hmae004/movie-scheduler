# movie-scheduler
This repository contains the HTML, Django files for a Multiplex Mall Movie Scheduler.

This repository contains the HTML and Django files for a Multiplex Mall Movie Scheduler.
It establishes week-to-week movie scheduling in a multiplex mall 

Inputs: 
The number of new movies released this week.
Number of movies already running
Cast weightage (scale of 5)
Movie demand score (scale of 10)
Success rate (scale of 5)
Language of the movie
Features of the movie
Local language
Special days of the week


Constraints: 
Demand-based calculation of the number of shows and screens based on cast weightage and demand score.
Prime time is show time with higher priority.
Priority for shows is on a scale of 1 to 5 (5 shows) 5 highest priority and 1 lowest.
 If the success rate of the movie goes below 60 % number of shows/screens need to be reduced.
If the success rate goes below 30 % movie is likely to be removed.
If the movie is running for more than a week, its priority should be reduced.
The priority of the movie is calculated based on cast weightage, demand score, and success rate.
A movie with higher priority is scheduled for show time with higher priority.
A new movie will initially have a success rate of 100.
Create a list of movies with movie names and priorities based on the above criteria.
Schedule for weekdays and weekend 

The total number of slots for a day is 6, the timings of the slots are:
The slots are of 3 hours each with a 30-minute break in between slots.

Slot 1 :  5:00am - 8:00am
Slot 2 :  8:30am - 11:30am
Slot 3 :  12:00pm - 3:00pm
Slot 4 : 3:30pm - 6:30pm
Slot 5 : 7:00pm - 10:00pm
Slot 6: 10:30pm - 1:30am
