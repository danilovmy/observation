# observation
A little micro-service which aims to serve the Observation data.

# Solution

This repository present e a REST API that will allow to:
 ● Introduce Observations into the system
 ● For any given Monitored:
   ○ Fetch all Observations given an observation name
   ○ Fetch the latest Observation, for a specific type of Observation.
 ● Compute and fetch the mean of Observations values (or component’s values) for a given observation_name.


# Suggestion about solution:

1. Solution not prowide the REST-FULL solution.
2. Solution based on the composition of the Django + DRF + Django-Filters + Django-Spectacular
3. To learn i take the newest 5.0 version of Django - it is still in dev status. 
4. Model Monitored, usally aka "User", is simply model without any additional attributes.
5. I dont create additional Model Observation Components, becaue to use the came model Observation can impove possibility to calculate parameters easily. But also provde some disadwantages, like a possible recurson in relations.
6. I dont create any Authentication System, because it should be technically defined, but without autentification this solution should not be used due work with "sencitiv privat data".
7. I also dont use any "sessioned" connection, because it should be based on the possibility of the clyent application, which are unknownon the curren moment.


# Task which chould be discussed in Detail:
1. Latest Observation for a specific type of Observation. It is not clear, that means "latest" in this moment: as "Latest Saved in system Observation" can contain old measure date and can be probably not the "latest issued Observation".
2. Compute and fetch the mean of Observations values (or component’s values)
for a given observation_name.

3. Completely unclear "mean" - matematical "average", or real measurment maximally close to awerage? 

What to do with steps? If We speak about steps - per hour/day, but we probably should speak about activity hours? Other case - if i sleep from 0 till 6 and can not have activity 1000steps/per hour. It should be choosen before calculation.

If we speak about Heartbit-frequency - moustly goes about heartbeat in silent phase, because it we can not speak about mean/average. It should be clear what we need before calculation.

If we speak about Blood Pressure - there is important the difference inbetween systolic und diastolic as a 'average' systolic or 'mean' diastolic. "Mean/average" in which periode? Whole life? 

What it should be done with errors? Or data is already cleaned?

I did an mathematical average calculation as well as max or min, but it is against humanity ideology :)


# How to start

Clone the repository.

run application in docker (depends on your OS)

Use browser to achieve http://localhost:8000/api/schema/swagger-ui/
Ant try to use the web interface accordingly to offered API-schema

Use Postman to send requests to test-server, for example
http://localhost:8000/api/observations/1/
