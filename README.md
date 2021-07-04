# DocIT

## Objective:
### The project aims to connect doctors and patients during lockdown via online technology. During the pandemic, since no one could go outside, people had to resort to video conferencing with their doctors in case of any medical emergency and guidance. Widespread use of video conferencing platforms like Google Meet, Microsoft Teams, etc. has become prevalent during the lockdown period. Previously there have been applications like Practo that allow the user to connect with a doctor.

## Implementation: 
### With this project, we aim at developing a multipurpose one-for-all website that provides a variety of features to the user. Our website will inculcate the following features:

#### Login and Signup Pages for both Patient and Doctor as well as Admin

#### Doctor verification via a special link that takes the doctor's email and sends them a link for a form. This can be checked by the admin team to make sure that only legitimate doctors are coming to the website.

#### Video and chat conferencing with the doctor of preference

#### Latest Health Related News

#### Calendar for the Doctor and Patient to check for their appointments

#### Scheduling new appointments at any time

#### Feature that allows the doctor to cancel any appointment, which will be followed by email notification to the patient. This email contains a link for the rescheduling page, through which the patient can alter their appointment time.

#### An FAQ bot that allows the user to ask questions related to the app

#### We have also implemented a Voice Assistant that allows the user to go to any page on the website.

#### The doctor can also write a prescription to the patient while conducting the meeting. This can be later printed by the patient for future reference.

## Applications: 
### In these Covid-19 related times, physical appointments with doctors can be a threat to both the patient and the doctors life. By providing online consultation facility, we reduce this risk extensively. - We are focussing more on user experience by providing all the functionalities in a single app giving users the ease of access.

## Instructions:
### The entire application has been hosted on the link provided.

### The application can be also run on the local system.

### To run the application on the local system, one has to download flask and node.js, npm. Although, to run a few components installation of node.js and npm is required. The standard node.js installation will successfully run features like voice control, chat section, and video call section.

### The entire database is set up on Remote MySQL. Features like chatbot have been created using Azure Functionalities. Nutrition analysis and voice control have been made using respective API calls.

### The API keys stored in the config.py are not included in the source code due to security reasons as Github won't allow it. So to experience the full web app, you can go to the hosted link provided and create an account using a valid email id to explore all the features. And if a user wants to run the app locally then he would have to contact us for details or he would have to create API keys and the remote SQL database.

### To run the project locally, start the flask app after installing all the required libraries using the 'pip' command mentioned in requirement.txt. Then open the app.py file and run it using any standard IDE like Spyder, VScode, etc. Then go to '127.0.0.1:9000' on your chrome browser to see the app running. But as mentioned a user can't properly run the app without the API keys as the prototype is supported by remote Mysql.

### To run node app: Firstly, install NodeJS: https://nodejs.org/en/download/ Download the repository or clone it. Then change the directory of the respective components and run npm install. Example: For docit-video-call(in Connect Components): Run the following commands: cd docit-video-call npm install yarn dev

### For other components:
#### Run the following commands:
#### cd <directory name>
#### npm install
#### npm start
#### The application will run on localhost:3000. The deployed links for all the components (for ease of access) are as follows: - https://docit-voicecontrold.netlify.app/ - https://docit-voicecontrol.netlify.app/ - https://docit-prescription.netlify.app/ - https://docit-videocall.herokuapp.com/

## Future Scope: 
### We would be scaling the app enabling higher number of users and seemless functionality implementation. - We would be improving the security of the application by enabling two factor authentication on multiple access points. - We would restrict the chat functionality between the doctor and the patient to a certain number of days. After the query period is exceeded the patient will have to pay an additional fee to consult the doctor via chat for the previous appointment. There is a transcript function that will allow the user to refer to the appointment once it is over. This is happening at the back end but the saving and viewing of this transcript has been kept as a future scope.
