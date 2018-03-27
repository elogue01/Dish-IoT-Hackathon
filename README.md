# Dish-IoT-Hackathon
This repo includes code and a powerpoint presentation from the Dish IoT Hackathon on 2/11/2018 - 2/12/2018. The goal of this hackathon was to create an IoT device that would improve the Dish campus community.  The IoT device needed to sense or monitor something in the environment and update information based on that sensor input. The hackathon was co-sponsored by Amazon Web Services (AWS) and teams were also mandated to incorporate an Alexa skill with their IoT device.

## Team SeatIt

### Team Members:
1) Eric Logue - Galvanize Data Science Grad   
2) Jonathan Herring - Galvanize Web Dev Grad  
3) Robert Reed - Dish Employee  
4) Clark Newell - Galvanize Web Dev Student  
5) Andrew Lattner - Dish Employee  
6) Kimberly Mavrakos - Dish Employee  
7) Paula Robson - Dish Employee  

### Team Goal:
Create a web app and Alexa Skill that lets Dish employees know if seats are available in the cafeteria.

### Approach:
1) Use a raspberry pi and PIR (proximity) sensor to detect movement under a seat in order to determine whether a seat is occupied.  
2) A Python script was written to allow the IoT device to monitor movement under the table in order to determine seat occupancy.
3) The Python script allows a change in the seat occupancy state to be delivered as a message to AWSIoT which then updates a AWS DynamoDB (noSQL database).   
4) Data stored in this database was then used to dynamically update a web app and to update an Alexa Skill.

### Team Member Roles:
**Eric Logue** - I wrote the Python code that ran our IoT device and delivered a change in occupancy state as a meassage to AWSIoT. I also worked with Jonathan Herring to register our device with AWSIoT and create an IoT rule that delivered our data to an AWS DynamoDB.  
**Jonathan Herring** - Jonathan built the IoT hardware using a raspberry pi and the PIR sensor.  He worked with me to register our device with AWSIoT and create the IoT rule that delivered data to an AWS DynamoDB.  While not a Python coder, Jonathan provided valuable input on developing the python code that ran on our IoT device.
**Robert Reed** - Bob built our SeatIt web app. The app used data in the DynamoDB to dynamically update the seat availability information presented in the app.  
**Clark Newell and Andrew Lattner** - Clark and Andrew worked together to develop the Alexa skill.  The skill was designed to allow an employee to ask Alexa how many seats were available in the Dish cafeteria.  
**Kimberly Mavrakos and  Paula Robson** - Kim and Paula worked to determine the business feasibility of our IoT device.  They also put together the teams powerpoint presentation and delivered the majority of that presentation to the hackathon judges.  Paula also assisted Jonathan in the hardware set up for our IoT device.

###Conclusion:
This was my first experience coding for a raspberry pi but I have to say I am hooked.  I have a number of projects planned to build raspberry pi IoT sensors for use around my house now.  Overall, I learned a lot about coding for a pi, about delivering data to the AWS cloud services, and in using noSQL databases.  Everyone on my team worked hard over the 2 day hackathon and were all great people to work with.  Our team did not win this competition but the judges were impressed by what we accomplished and encouraged us to work on the project further in a future hackathon.  Feel free to contact me if you have comments or questions about our hackathon project.  My email is elogue01@gmail.com
