#job portal application


This web application made only for educational and practise purposes.
Application backend written with python, and django web framework , frontend have simple design, and contain bootsrap (fastboostrap) elements, and free templates - contain several java-scripts.

Application main functions:

1. 
- Select navbar for employee or employer signup, and different functions
- login as employer or employee or admin


2. With admin user login 
- Add job categories
- list job categories (with delete, and modify options)

3. with Employee login 

- view, update employee profile, export  CV to pdf 
- add remove or update jobs, schools 
- create, modify, delete, and view job notifications
- Apply to jobs, list applications, remove or archive applications
- Send review about employers (modify, and delete reviews)
- send start rating about employers
- view messages, reply messages (update, and delete messages)


4. with employer login 

- search for employees, list them order by category.
- see employee profiles, export to pdf.
- send messages, view messages, reply messages ( update and delete messages) 
- follow or unfollow employees
- list followed employees
- add new job
- list uploaded jobs (modify and delete) 
- view job candidates 
- modify application status 
- list applications 


5. functions to both logged and not logged in users

- list jobs order by category  
- list jobs according to employers
- simple, and advanced job search functions
- list employers
- simple employer search 
- see jobs and job details 
- see star rating and reviews

# installation

1. clone the repository  ( https://github.com/immonhotep/job_portal.git )
2. create python virtual environment ( virtualenv venv on linux )
3. activate the virtual environment ( source venv/bin/activate )
4. install django and required packages ( pip install -r requirements.txt)
5. run  the necessary commands to auto create database system  ( python manage.py makemigrations) and then ( python manage.py migrate )
6. create superuser account  ( python manage.py runserver)
7. login with your superuser account on http://127.0.0.1:8000/
8. create some job categories under navbar project dropdown menu
9. after this  register as employee and employee and test application functions


