from django.db import models
from PIL import Image
from django.db.models import Avg,Count



from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER_TYPE = (
         
        ('Employee', 'Employee'),
        ('Employer', 'Employer'),
        ('Site Administration', 'Site Administration'),
    )

    type = models.CharField(max_length = 250,choices=USER_TYPE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True )


    def __str__(self):
        return self.username


class Employeeprofile(models.Model):

    LICENCE_TYPE = (

        ('None', 'None'), 
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('K', 'K'),
        ('T', 'T'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_place = models.CharField(max_length=200,null=True)
    birth_date = models.DateField(null=True)
    address = models.CharField(max_length=250,null=True)
    phone_number = models.CharField(max_length=20,null=True)
    image = models.ImageField(null=True, blank=True ,upload_to="images/profile_avatars")
    profession = models.CharField(null=True,blank=True,max_length=250)
    sector = models.ForeignKey(to="jobs.JobCategory",related_name='cvs', on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(max_length=500,null=True)
    salary = models.PositiveIntegerField(default=0,null=True, blank=True)
    driving_licence = models.CharField(max_length = 10,choices=LICENCE_TYPE, default="None")

    def __str__(self):

        return f'{self.user.first_name}-{self.user.last_name}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



   
class EmployeeSchool(models.Model):

    SCHOOL_TYPE = [

        ('Elementary School', 'Elementary School'), 
        ('Professional School', 'Professional School'),
        ('vocational school', 'Vocational school'),
        ('College', 'College'),
        ('University', 'University'),

    ]

    employee = models.ForeignKey(Employeeprofile, related_name="schools" ,on_delete=models.CASCADE)
    school_type = models.CharField(max_length = 100,choices=SCHOOL_TYPE, default="Elementary School")
    name = models.CharField(max_length=250)
    education = models.TextField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name



class EmployeeJobplace(models.Model):

    employee = models.ForeignKey(Employeeprofile, related_name="jobplace" ,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    position_name = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name



class EmployerProfile(models.Model):

    AREA_CHOICES = (
        ('Economy', 'Economy'),
        ('IT', 'IT'),
        ('Develpoment','Development'),
        ('Commerce', 'Commerce'),
        ('Manufacturing','Manufacturing'),
        ('Healtcare','Healtcare'),
        ('Logistic','Logistic'),
        ('Public Relations','Public Relations'),
        ('Human Resources','Human Resources'),
        ('Entertainment','Entertainment'),
        ('State and public sector','State and public sector'),
        ('Services','Services'),
    )


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=250)
    sector = models.CharField(max_length = 250,choices=AREA_CHOICES)
    main_profile = models.TextField(max_length=500)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    employee_number = models.PositiveIntegerField(null=True)
    logo = models.ImageField(null=True, blank=True ,upload_to="images/company_logos")

    def __str__(self):
        return self.company_name
    

    @property
    def imageURL(self):
        try:
            url = self.logo.url
        except:
            url = ''
        return url
    

    @property
    def averagerate(self):
        review = EmployerRatio.objects.filter(employer=self).aggregate(average=Avg('star_rating'))
        avg=0
        if review["average"] is not None:
            avg=float(review["average"])
        return avg
    
    @property
    def countrate(self):
        reviews = EmployerRatio.objects.filter(employer=self).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt
    

class Messages(models.Model):

    title = models.CharField(max_length=250)
    sender = models.ForeignKey(User, related_name="sent_by", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name="sent_to", on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='message_reply', null=True, blank=True)
    message = models.TextField(max_length=2000)
    checked = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.title}-from: {self.sender}-to: {self.receiver}'
    
    @property
    def get_reply(self):
        return Messages.objects.filter(reply=self).reverse()
    


class EmployerReview(models.Model):

    employer =  models.ForeignKey(EmployerProfile, related_name="employer_reviews" ,on_delete=models.CASCADE)
    employee = models.ForeignKey(Employeeprofile,related_name="employee_reviews", on_delete=models.CASCADE)
    review = models.TextField(max_length=2000)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.employer.company_name} -by: {self.employee.user.last_name}-{self.employee.user.first_name}'
    

class EmployerRatio(models.Model):

    employee = models.ForeignKey(Employeeprofile, related_name="send_ration", on_delete=models.CASCADE, null=True, blank=True)
    employer = models.ForeignKey(EmployerProfile, related_name="get_ration", on_delete=models.CASCADE, null=True, blank=True)
    star_rating = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):

        return f'{self.employee.user.last_name}-{self.employee.user.first_name} to - {self.employer.company_name}'