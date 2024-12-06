from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm

from .models import User,Employeeprofile,EmployerProfile,EmployeeSchool,EmployeeJobplace,Messages
from jobs.models import JobCategory
import datetime


class UserSignupForm(UserCreationForm):

    class  Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    username = forms.CharField(label="",max_length=50,widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Enter username',

    }))


    first_name =  forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Enter lirst name',

    }))

    last_name =  forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Enter last name',

    }))


    email = forms.CharField(label="",max_length=100,widget=forms.EmailInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Enter email address',

    }))


    password1 = forms.CharField(label="",max_length=20,widget=forms.PasswordInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Enter your password',

    }))


    password2 = forms.CharField(label="",max_length=20,widget=forms.PasswordInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Repeat your password',

    }))

class UserEditform(forms.ModelForm):

    class Meta:

        model = User

        fields = ('username','first_name','last_name','email')


    username = forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Username',
        
    })) 

    first_name = forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'First name',
        
    })) 

    last_name = forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Last name',
        
    })) 

    email = forms.CharField(label="",max_length="100",widget=forms.EmailInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Email',
        
    })) 



class EmployeeEditProfileForm(forms.ModelForm):

    class Meta:
        model = Employeeprofile

        fields=('birth_place','birth_date','address','phone_number','image','sector','profession','bio','driving_licence','salary')



    LICENCE_TYPE = [

        ('None', 'None'), 
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('K', 'K'),
        ('T', 'T'),
    ]


    birth_place = forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Birth place',
        
    })) 


    birth_date = forms.DateField(
        label="Date of Birth",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={

            'min': '1901-01-01', 'max': '2090-01-01',   
            'type': 'date',                                                      
            'class':'form-control form-control-sm',                                             
        }),
        input_formats=["%Y-%m-%d"]
    )


    address = forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Addresss',
        
    }))

    phone_number = forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Phone Number',
        
    }))

    image = forms.ImageField(required=True)


    profession = forms.CharField(label="",max_length="250",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Profession',
        
    }))


    sector = forms.ModelChoiceField(queryset=JobCategory.objects.all(),widget=forms.Select(attrs={
          'class':'form-select form-control fw-bolder'
     }),required=True)

    bio = forms.CharField(label="",max_length="500",widget=forms.Textarea(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'From yourself',
        
    }))

    driving_licence = forms.ChoiceField(
        
        choices=LICENCE_TYPE,
        widget=forms.Select(attrs={
         
            'class':'form-select form-control fw-bolder'
            
            })
        )
    
    salary = forms.IntegerField(label="Requested netto salary",widget=forms.NumberInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'0',


    }))

    def is_valid(self):
        valid = super().is_valid()

        if hasattr(self, 'cleaned_data') and valid:

            birth_date = self.cleaned_data.get('birth_date')

            today = datetime.date.today()

            if birth_date > today:
                self.add_error('birth_date', 'Incorrect date: Birth day in the future ')
                valid = False

        return valid


class UserLoginForm(AuthenticationForm):

    def __init__(self,*args,**kwargs):
        super(UserLoginForm,self).__init__(*args,**kwargs)

   
    username = forms.CharField(label="",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Username',

    }))

    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Password',
    }))



class EmployerEditProfileForm(forms.ModelForm):
    
    class Meta:
        model = EmployerProfile
        fields = ('company_name','sector','main_profile','address','phone','employee_number','logo')

    AREA_CHOICES = [
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
        ]
    

    company_name = forms.CharField(label="",widget=forms.TextInput(attrs={

            'class':'form-control form-control-sm',
            'placeholder':'Company name ',

        }))


    sector = forms.ChoiceField(
        
        choices=AREA_CHOICES,
        widget=forms.Select(attrs={
         
            'class':'form-select form-control fw-bolder'
            
            })
        )
        
    main_profile = forms.CharField(label="",widget=forms.Textarea(attrs={

            'class':'form-control form-control-sm',
            'placeholder':'Company Description ',


        }))


    address = forms.CharField(label="",widget=forms.TextInput(attrs={

            'class':'form-control form-control-sm',
            'placeholder':'Address ',

        }))


    phone = forms.CharField(label="",widget=forms.TextInput(attrs={

            'class':'form-control form-control-sm',
            'placeholder':'Phone Number ',

        }))


    employee_number = forms.IntegerField(label="Employee number",widget=forms.NumberInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'0',


    }))


class StudiesForm(forms.ModelForm):

    class Meta:

        model = EmployeeSchool
        fields = ('school_type','name','education','start_date','end_date')

    
    SCHOOL_TYPE = [

        ('Elementary School', 'Elementary School'), 
        ('Professional School', 'Professional School'),
        ('vocational school', 'Vocational school'),
        ('College', 'College'),
        ('University', 'University'),

    ]

    school_type = forms.ChoiceField(
        
        choices=SCHOOL_TYPE,
        widget=forms.Select(attrs={
         
            'class':'form-select form-control fw-bolder'
            
            })
        )


    name = forms.CharField(label="",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'School name',

    }))


    start_date = forms.DateField(
        label="Start Date",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={

            'min': '1901-01-01', 'max': '2090-01-01',
            'type': 'date',
            'class':'form-control form-control-sm',
            
            }),
        input_formats=["%Y-%m-%d"]
    )


    end_date = forms.DateField(
        label="End date",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={

            'min': '1901-01-01', 'max': '2090-01-01',  
            'type': 'date',
            'class':'form-control form-control-sm'
            
            }),
        input_formats=["%Y-%m-%d"]
    )

    education = forms.CharField(label="",widget=forms.Textarea(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Description',


    }))

    def is_valid(self):
        valid = super().is_valid()

        if hasattr(self, 'cleaned_data') and valid:

            start_date = self.cleaned_data.get('start_date')
            end_date = self.cleaned_data.get('end_date')
            today = datetime.date.today()


            if end_date < start_date:
                self.add_error('end_date', 'Incorrect date: End date before than the start date')
                valid = False

            if end_date > today:
                self.add_error('end_date', 'Incorrect date: End date in the future ')
                valid = False

        return valid


class JobForm(forms.ModelForm):

    class Meta:

        model = EmployeeJobplace
        fields = ('name','position_name','description','start_date','end_date')

    name = forms.CharField(label="",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Job place name',

    }))

    position_name = forms.CharField(label="",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Position name',

    }))


    description = forms.CharField(label="",widget=forms.Textarea(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Description',

    }))


    start_date = forms.DateField(
        label="Start Date",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={

            'min': '1901-01-01', 'max': '2090-01-01',
            'type': 'date',
            'class':'form-control form-control-sm'
            
            }),

        input_formats=["%Y-%m-%d"]
    )




    end_date = forms.DateField(
        label="End date",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={

            'min': '1901-01-01', 'max': '2090-01-01',
            'type': 'date',
            'class':'form-control form-control-sm'
            
            }),
        input_formats=["%Y-%m-%d"]
    )


    def is_valid(self):
        valid = super().is_valid()

        if hasattr(self, 'cleaned_data') and valid:

            start_date = self.cleaned_data.get('start_date')
            end_date = self.cleaned_data.get('end_date')
            today = datetime.date.today()


            if end_date < start_date:
                self.add_error('end_date', 'Incorrect date: End date before than the start date')
                valid = False

            if end_date > today:
                self.add_error('end_date', 'Incorrect date: End date in the future ')
                valid = False

        return valid



class MessageForm(forms.ModelForm):

    class Meta:

        model = Messages

        fields = ('title','message')


    title = forms.CharField(label="",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Description',

    }))


    message = forms.CharField(label="",widget=forms.Textarea(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Description',


    }))



class ChangePasswordForm(PasswordChangeForm):


    old_password = forms.CharField(widget = forms.PasswordInput(attrs={

        'placeholder':'Enter old password',
        'class':'form-control form-control-sm',

    })) 

    new_password1 = forms.CharField(label='New password ',widget = forms.PasswordInput(attrs={

        'placeholder':'Enter old new password ',
        'class':'form-control form-control-sm',

    }))

    new_password2 = forms.CharField(label='Retype New Password',widget = forms.PasswordInput(attrs={

        'placeholder':'Repeat new password',
        'class':'form-control form-control-sm',

    }))


