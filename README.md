# Observation
This micro-service aims to serve Observation data.

# Solution
This repository presents a REST API that will allow you to:
 - Introduce Observations into the system
 - For any given Monitored:
   - Fetch all Observations given an observation name
   - Fetch the latest Observation for a specific type of Observation.
 - Compute and fetch the mean of Observation values (or component's values) for a given observation_name.

# Suggestions about the solution:
1. The solution does not provide a complete RESTful solution.
2. The solution is based on the composition of Django, DRF (Django Rest Framework), Django-Filters, and Django-Spectacular.
3. To learn, I used the newest 5.0 version of Django, which is still in development status.
4. The "Monitored" model, usually known as "User," is a simple model without any additional attributes.
5. I didn't create an additional "Observation Components" model because using the same "Observation" model can improve the possibility to calculate parameters easily. However, it may have some disadvantages, such as possible recursion in relations.
6. I didn't create an authentication system because it should be technically defined. Without authentication, this solution should not be used for working with sensitive private data.
7. I also didn't use any "sessioned" connection because it should be based on the client application's possibilities, which are unknown at the moment.

# Tasks that should be discussed in detail:
1. "Latest Observation for a specific type of Observation" is not clear. It's unclear whether "latest" means the latest saved observation in the system or the latest issued observation. Further clarification is needed.
2. "Compute and fetch the mean of Observation values (or component’s values) for a given observation_name." The term "mean" needs clarification - whether it refers to the mathematical average or a measurement that is closest to the average. The handling of time periods and activity hours also needs clarification for steps data, heartbeat frequency, and blood pressure data.

Additionally, it's important to specify how errors or data cleaning should be handled.

I have implemented mathematical average calculations as well as max and min, but these may not align with the desired results.

# How to start
1. Clone the repository.
2. Run the application in Docker, depending on your operating system.
3. Use a web browser to access http://localhost:8000/api/schema/swagger-ui/ and utilize the web interface according to the provided API schema.
4. Use Postman to send requests to the test server, for example, http://localhost:8000/api/observations/1/.