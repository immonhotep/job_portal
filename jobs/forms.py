from django import forms

from .models import JobPossibility,JobCategory,JobApplication,JobNotification
from  main.models import EmployerReview



class JobPossibilityForm(forms.ModelForm):

    class Meta:
        model = JobPossibility
        fields = ('title','required_school','job_type','payment','required_skills','job_description','job_location','benefits_package','other_information')




    SCHOOL_TYPE = [

        ('Elementary School', 'Elementary School'), 
        ('Professional School', 'Professional School'),
        ('vocational school', 'Vocational school'),
        ('College', 'College'),
        ('University', 'University'),

    ]


    title = forms.CharField(label="",max_length="255",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Job Title',

    }))



    required_school = forms.ChoiceField(
        
        choices=SCHOOL_TYPE,
        widget=forms.Select(attrs={
         
            'class':'form-select form-control fw-bolder'
            
            })
        )
    

    job_type = forms.ModelChoiceField(queryset=JobCategory.objects.all(),widget=forms.Select(attrs={
          'class':'form-select form-control fw-bolder'
     }),required=True)
    
    
    
    payment = forms.IntegerField(label="Payment",required=False,widget=forms.NumberInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'0',


    }))


    required_skills = forms.CharField(label="",max_length="1000",widget=forms.Textarea(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Required skills',
        
    }))


    job_description = forms.CharField(label="",max_length="1000",widget=forms.Textarea(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Job Description',
        
    }))


    job_location = forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Job Location',

    }))


    benefits_package = forms.CharField(label="",max_length="1000",widget=forms.Textarea(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Benefits Package',
        
    }))


    other_information = forms.CharField(label="",max_length="1000",widget=forms.Textarea(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Other Information',
        
    }))


class JobcategoryForm(forms.ModelForm):

    class Meta:

        model = JobCategory

        fields = ('category_name',)

    category_name = forms.CharField(label="",max_length="255",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Job Category',
        
    }))


class ApplicationForm(forms.ModelForm):

    class Meta:

        model = JobApplication

        fields=('status',)


    APP_STATUS = [

        ('Pending', 'Pending'), 
        ('Invited', 'Invited'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired'),

    ]


    status = forms.ChoiceField(
        
        choices=APP_STATUS,
        widget=forms.Select(attrs={
         
            'class':'form-select form-control form-control-sm fw-bolder mb-2' 
            
            })
        )
    


class EmployeeReviewForm(forms.ModelForm):

    class Meta:

        model = EmployerReview
        fields = ('review',)

    review =  forms.CharField(label="",max_length="255",widget=forms.Textarea(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Review',
        
    })) 



class NotificationForm(forms.ModelForm):
    
    class Meta:

        model = JobNotification
        fields = ('title','required_school','job_type','job_location')  


    SCHOOL_TYPE = [

        ('Elementary School', 'Elementary School'), 
        ('Professional School', 'Professional School'),
        ('vocational school', 'Vocational school'),
        ('College', 'College'),
        ('University', 'University'),

    ]     

    title = forms.CharField(label="",max_length="250",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Job title',
        
    }),required=False)


    required_school = forms.ChoiceField(
        
        choices=SCHOOL_TYPE,
        widget=forms.Select(attrs={
         
            'class':'form-select form-control form-control-sm fw-bolder mb-2' 
            
            })
        )

    job_type = forms.ModelChoiceField(queryset=JobCategory.objects.all(),widget=forms.Select(attrs={
          'class':'form-select form-control fw-bolder'
     }),required=True)
    


    job_location = forms.CharField(label="",max_length="250",widget=forms.TextInput(attrs={

        'class':'form-control form-control-sm',
        'placeholder':'Job Location',
        
    }),required=False)
