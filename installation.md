# Installation & Setup

In order to use the application for the first time follow these steps:
0. install anaconda
0. set up the virtual environment
0. setup the database
0. run the server
0. open the browser pointing at the running server
0. login as student or teacher

Next time, the application can be started by just following the last three steps

## install anaconda
[Download](https://www.anaconda.com/distribution/#download-section) and install Anaconda for your operating system, 
the latest version is recommended

## environment setup
Open the "Anaconda Prompt" application and navigate to the folder where this file is contained.
Then run the following command to create the environment:
```
conda env create -f environment.yml
```
Once the environment is create it, activate it as follows:
```
conda activate msc_project 
```
More information about managing conda virtual environment can be found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)

## setup the database
To setup the application database the following commands need to be run:
```
python manage.py makemigrations
python manage.py migrate
```
and then to populate it with some test data run:
```
python populate_project.py
```

## run the server
To run the server, run the following command
```
python manage.py runserver
```
If not coming from the previous setup, make sure the command prompt is pointing at the folder where this file is and 
that the 'msc_project' virtual environment is activated (see 'environment setup')

## open the web app in the browser
As the server is running a local application, you should be able to reach it by opening the browser and navigating to:
```
http://localhost:8000/
```

## login
If the database was populated with the test data, the following users are available:
- theteacher
- student1
- student2
- student3
- student4
The password for all of them has been setup as: *h$iog892f*

theteacher user also have access to the Django admin page, where models can be viewed and manipulated.
The admin page can be reached from the browser at the following address:
```
http://localhost:8000/admin
```
## ACJ-function
The ACJ-functionality can be found by logging in as as theteacher, click on 'Patch1' in the student-table, and then click on the button 'judge submissions'.

