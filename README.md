# A RESTful Sensor Data Web Service
This project originated from the end of a University course project, from 2020. The purpose was to explore the creation of a functional web service from the ground up. Functionally it could store IoT data and also be used to retrieve data for analysis. The original concept was for a general-purpose web service that could be modified and adapted for various purposes.  Yet, during the project, I was advised to be more specific about the web services application. I then chose to focus on a service that would gather environmental data. A prototype IoT device would periodically generate the data and send it to the web service, The IoT device comprised of a Raspberry PI Zero, Arduino Nano and a couple of inexpensive hobbyist sensors.  

Functionally, the final solution for the course project was a success, but it had a flaw.  The web services query calls where were tightly coupled with a database of choice, MongoDB. This dependency was not in line with my original concept, in which the developer could change one type of database for another with a few modifications.  

This project hopes to address such issues and so fulfil the original intention of creating a functional web service that could be modified and used for various purposes without too much trouble. 

I strongly advise against running this web service in its current state as it is unstable due to the refactoring process.  

**Technologies:**
+ Python 3.7
+ Flask 1.1
+ pymongo 3.10
+ MongoDB

**Supporting technologies used to run the service:**
+ uWSGI
+ Ubuntu Linux server
+ Nginx proxy/webserver. Others web servers are available if they have support uWSGI. 

**Status:**
Alpha 1.1   
