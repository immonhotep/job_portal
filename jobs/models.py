from django.db import models
from main.models import EmployerProfile,Employeeprofile



class JobCategory(models.Model):

    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class JobPossibility(models.Model):


    SCHOOL_TYPE = (

        ('Elementary School', 'Elementary School'), 
        ('Professional School', 'Professional School'),
        ('vocational school', 'Vocational school'),
        ('College', 'College'),
        ('University', 'University'),

    )


    title = models.CharField(max_length=250)
    employer = models.ForeignKey(EmployerProfile, related_name="employer_jobs", on_delete=models.CASCADE)
    required_school = models.CharField(max_length = 100,choices=SCHOOL_TYPE, default="Elementary School")
    job_type = models.ForeignKey(JobCategory, on_delete=models.CASCADE,related_name="job_categories",null=True ,blank=True)
    payment = models.PositiveIntegerField(default=0, null=True, blank=True)
    required_skills = models.TextField(max_length=1000)
    job_description = models.TextField(max_length=1000)
    job_location = models.CharField(max_length=100)
    benefits_package = models.TextField(max_length=1000)
    other_information = models.TextField(max_length=1000)
    publication_date = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=True)

    def __str__(self):

        return f'{self.title}-{self.employer}'
    

class JobNotification(models.Model):

    SCHOOL_TYPE = (

        ('Elementary School', 'Elementary School'), 
        ('Professional School', 'Professional School'),
        ('vocational school', 'Vocational school'),
        ('College', 'College'),
        ('University', 'University'),

    )

    title = models.CharField(max_length=250)
    required_school = models.CharField(max_length = 100,choices=SCHOOL_TYPE, default="Elementary School")
    job_type = models.ForeignKey(JobCategory, on_delete=models.CASCADE,null=True ,blank=True)
    job_location = models.CharField(max_length=100)
    employee = models.ForeignKey(Employeeprofile, on_delete=models.CASCADE)
   
    def __str__(self):

        return f'{self.title}-{self.employee}'



class JobApplication(models.Model):

    STATUS_TYPE = (

        ('Pending', 'Pending'), 
        ('Invited', 'Invited'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired'),
    )

    job  = models.ForeignKey(JobPossibility, related_name="applications",on_delete=models.CASCADE)
    applicant = models.ForeignKey(Employeeprofile, related_name="candidates" ,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 100,choices=STATUS_TYPE, default="Pending")
    archived = models.BooleanField(default=False)

    def __str__(self):
        
        return f'{self.job}-{self.applicant}'





    
