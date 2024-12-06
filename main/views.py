from django.http import HttpResponse
from django.shortcuts import render,redirect
from django .views import View
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.urls import reverse_lazy,reverse
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserSignupForm,UserLoginForm,EmployeeEditProfileForm,EmployerEditProfileForm,StudiesForm,JobForm,UserEditform,MessageForm,ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .models import Employeeprofile,EmployerProfile,EmployeeSchool,EmployeeJobplace,Messages,EmployerReview,EmployerRatio
from  jobs.models import JobCategory
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from jobs.mixins import EmployeeRequiredMixin,EmployerRequiredMixin
from django.db.models import Q
from .models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage






class Homeview(View):

    def get(self,request):

        categories = JobCategory.objects.all().order_by('-category_name')
        categories_2 = categories

        employerprofiles = EmployerProfile.objects.all().order_by('company_name')


        search=self.request.GET.get('searchemployer')

        if search:

            employerprofiles = EmployerProfile.objects.filter(company_name__icontains=search).order_by('company_name')
         

        p = Paginator(employerprofiles,7)
        page = request.GET.get('page')
                    

        try:
            employerprofiles = p.page(page)
        except PageNotAnInteger:
            employerprofiles = p.page(1)
        except EmptyPage:
            employerprofiles = p.page(p.num_pages)


        p = Paginator(categories,7)
        page2 = request.GET.get('page2')
                    

        try:
            categories = p.page(page2)
        except PageNotAnInteger:
            categories = p.page(1)
        except EmptyPage:
            categories = p.page(p.num_pages)


        p = Paginator(categories_2,7)
        page3 = request.GET.get('page3')
                    

        try:
            categories_2 = p.page(page3)
        except PageNotAnInteger:
            categories_2 = p.page(1)
        except EmptyPage:
            categories_2 = p.page(p.num_pages)

        syle = request.session.setdefault('style', 'light')



        

        context = {'categories':categories,'categories_2':categories_2,'employerprofiles':employerprofiles}
        return render(self.request,'main/home.html',context)
    


    

    
class SetNavbarStyle(View):

    def post(self,request):
   
        type = self.request.POST.get('type')

        if type and type == "dark" :

            request.session['style'] = "dark"
        
        elif type and type == "light":

            request.session['style'] = "light"

        return redirect(request.META.get('HTTP_REFERER'))



class EmployeeSignupview(View):

    def get(self,request):
        
        form = UserSignupForm()
        context={'form':form,'page_name':'signup_employee'}
        return render(self.request,'main/universal_form.html',context)

    def post(self,request):

        form = UserSignupForm(self.request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.type = "Employee"
            new_user.save()

            profile = Employeeprofile.objects.create(user=new_user,pk=new_user.pk)

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username,password=password)

            if user is not None:

                login(self.request,user)


            messages.success(self.request,f'Your account has been created Welcome: {username}')
            return redirect('update_employee')
        
        else:

            for error in list(form.errors.values()):
                messages.error(self.request,error)
            return redirect('signup_employee')
       


class EmployerSignupview(View):

    def get(self,request):
        
        form = UserSignupForm()
        context={'form':form,'page_name':'signup_employer'}
        return render(self.request,'main/universal_form.html',context)

    def post(self,request):

        form = UserSignupForm(self.request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.type = "Employer"
            new_user.save()

            profile = EmployerProfile.objects.create(user=new_user,pk=new_user.pk)

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username,password=password)

            if user is not None:

                login(self.request,user)


            messages.success(self.request,f'Your account has been created Welcome: {username}')
            return redirect('update_employer')
        
        else:

            for error in list(form.errors.values()):
                messages.error(self.request,error)
            return redirect('signup_employer')



class UpdateEmployeeview(EmployeeRequiredMixin,View):

    def get(self,request):

        form = EmployeeEditProfileForm(instance=self.request.user.employeeprofile)
        user_form = UserEditform(instance=self.request.user)
        context = {'form':form,'user_form':user_form}

        return render(request,'main/update_employee.html',context)

    def post(self,request):

        form = EmployeeEditProfileForm(request.POST,request.FILES,instance=self.request.user.employeeprofile)
        user_form = UserEditform(request.POST,instance=self.request.user)

        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()

            messages.success(request,'Your profile has been updated')
            return redirect('update_employee')

        else:
            for error in list(form.errors.values()):
                messages.error(self.request,error)
                return redirect('update_employee')


    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')    
        
    login_url = "/login/"
    redirect_field_name = "redirect_to"
        


class UpdateEmployerview(EmployerRequiredMixin,View):

    def get(self,request):

        form = EmployerEditProfileForm(instance=self.request.user.employerprofile)
        user_form = UserEditform(instance=self.request.user)
        
        context = {'form':form,'user_form':user_form}
        return render(request,'main/update_employer.html',context)

    def post(self,request):

        form = EmployerEditProfileForm(request.POST,request.FILES,instance=self.request.user.employerprofile)
        user_form = UserEditform(self.request.POST,instance=self.request.user)
        

        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('update_employer')


    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')  

    login_url = "/login/"
    redirect_field_name = "redirect_to"
    


class UserLoginView(SuccessMessageMixin,LoginView):

    template_name = 'main/universal_form.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

   
    def get_success_message(self,cleaned_data):
        return(f'{self.request.user} logged in successfully' )
    

    def get_context_data(self, *args,**kwargs):
        context = super(UserLoginView,self).get_context_data(*args,**kwargs)

        context['page_name'] = "login"
        return context


    def get_success_url(self):
         
        try:
            self.request.user.employeeprofile
            self.request.session['style'] = "light"
           

        except:
             self.request.session['style'] = "dark" 
              
        return reverse_lazy('home')
    

    def form_invalid(self,form):
        messages.error(self.request,'Invalid Username or password')
        return self.render_to_response(self.get_context_data(form=form))



class UserLogoutView(LoginRequiredMixin,View):

    def post(self,request):
        
        logout(self.request)
        messages.success(self.request,'You have been logged out')
        return redirect('home')
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"




class CustompasswordchangeView(LoginRequiredMixin,SuccessMessageMixin,PasswordChangeView):

    form_class = ChangePasswordForm
    template_name = 'main/universal_form.html'

    def get_success_message(self, cleaned_data):
        return('Your password has been changed')
    
    def get_success_url(self):
        return reverse('home')
    
   
    def form_invalid(self, form):
        for error in list(form.errors.values()):
            messages.error(self.request,error) 
            
        return self.render_to_response(self.get_context_data(form=form))

    
    def get_context_data(self, *args, **kwargs):

        context = super(CustompasswordchangeView,self).get_context_data(*args,**kwargs)
        context['page_name'] = "change_password"
        return context

        
    login_url = "/login/"
    redirect_field_name = "redirect_to"    




class StudiesView(EmployeeRequiredMixin,View):


    def get(self,request):

        studies = EmployeeSchool.objects.filter(employee=self.request.user.employeeprofile).order_by('-start_date')
        context={'studies':studies}
        return render(request,'main/studies.html',context)
    
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')


    login_url = "/login/"
    redirect_field_name = "redirect_to"



class AddnewStudyView(EmployeeRequiredMixin,View):

    def get(self,request):
       

        form = StudiesForm()
        context={'form':form,'page_name':'add_study'}
        return render(request,'main/universal_form.html',context)

    def post(self,request):

        form = StudiesForm(self.request.POST)
        if form.is_valid():
            study = form.save(commit=False)
            study.employee = self.request.user.employeeprofile
            study.save()
            messages.success(self.request,'Your study has been saved')
            return redirect('studies')
        
        else:

            for error in list(form.errors.values()):
                messages.error(self.request,error)
                return redirect('add_study')
            

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')


    login_url = "/login/"
    redirect_field_name = "redirect_to"



class EditStudyView(EmployeeRequiredMixin,View):

    def get(self,request,pk):
        
        school = get_object_or_404(EmployeeSchool,pk=pk)

        if school.employee == self.request.user.employeeprofile:
            form = StudiesForm(instance=school)
            context = {'form':form,'page_name':'update_study'}
            return render(request,'main/universal_form.html',context)
        else:
            messages.error(request,'Access denied')
            return redirect('studies')

    def post(self,request,pk):
        
        school = get_object_or_404(EmployeeSchool,pk=pk)

        if school.employee == self.request.user.employeeprofile:
            form = StudiesForm(self.request.POST,instance=school)
            if form.is_valid():
                form.save()
                messages.success(self.request,'Your Study has been updated')
                return redirect('studies')

            for error in list(form.errors.values()):
                    messages.error(self.request,error)
                    return redirect('studies')
  
        else:
            messages.error(request,'Access denied')
            return redirect('update_study')
        
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')
        
    login_url = "/login/"
    redirect_field_name = "redirect_to"
        


class DeleteStudyView(EmployeeRequiredMixin,View):

    def post(self,request,pk):

        school = get_object_or_404(EmployeeSchool,pk=pk)

        if school.employee == self.request.user.employeeprofile:

            school.delete()
            messages.success(self.request,f'{school.name} has been deleted')
            return redirect('studies')
            
        else:
            messages.error(self.request,'Access Denied')
            return redirect('studies')

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class JobsView(EmployeeRequiredMixin,View):


    def get(self,request):

        jobs = EmployeeJobplace.objects.filter(employee=self.request.user.employeeprofile).order_by('-start_date')
        context={'jobs':jobs}
        return render(request,'main/jobs.html',context)
    

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')


    login_url = "/login/"
    redirect_field_name = "redirect_to"



class AddnewJobView(EmployeeRequiredMixin,View):

    def get(self,request):
       
        form = JobForm()
        context={'form':form,'page_name':'add_job'}
        return render(request,'main/universal_form.html',context)

    def post(self,request):

        form = JobForm(self.request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employee = self.request.user.employeeprofile
            job.save()
            messages.success(self.request,'Your job has been saved')
            return redirect('jobs')
        
        else:

            for error in list(form.errors.values()):
                messages.error(self.request,error)
                return redirect('add_job')
            
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class EditJobView(EmployeeRequiredMixin,View):

    def get(self,request,pk):
        
        job = get_object_or_404(EmployeeJobplace,pk=pk)

        if job.employee == self.request.user.employeeprofile:
            form = JobForm(instance=job)
            context = {'form':form,'page_name':'update_job'}
            return render(request,'main/universal_form.html',context)
        else:
            messages.error(request,'Access Denied')
            return redirect('jobs')

    def post(self,request,pk):
        
        job = get_object_or_404(EmployeeJobplace,pk=pk)

        if job.employee == self.request.user.employeeprofile:
            form = JobForm(self.request.POST,instance=job)
            if form.is_valid():
                form.save()
                messages.success(self.request,'Your job has been updated')
                return redirect('jobs')

            for error in list(form.errors.values()):
                    messages.error(self.request,error)
                    return redirect('jobs')
  
        else:
            messages.error(request,'Access Denied')
            return redirect('update_job')
        
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')
        
    login_url = "/login/"
    redirect_field_name = "redirect_to"




class DeleteJobView(EmployeeRequiredMixin,View):

    def post(self,request,pk):

        job = get_object_or_404(EmployeeJobplace,pk=pk)

        if job.employee == self.request.user.employeeprofile:

            job.delete()
            messages.success(self.request,f'{job.name} has been deleted')
            return redirect('jobs')
            
        else:
            messages.error(self.request,'Access Denied')
            return redirect('jobs')
        

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"




class SearchEmployeeView(EmployerRequiredMixin,View):

    def get(self,request):

        

        categories = JobCategory.objects.all()
        
        selected_category = self.request.GET.get('jobcategory',"")
        search_element = self.request.GET.get('search',"")
       
        

        if  selected_category == "" and search_element == "":
            context={'categories':categories}
            return render(self.request,'main/search_employee.html',context)
            

        if selected_category != "":
            search_result = User.objects.filter(Q(employeeprofile__profession__icontains=search_element) | Q(employeeprofile__jobplace__description__icontains=search_element) | Q(employeeprofile__jobplace__position_name__icontains=search_element),employeeprofile__sector=selected_category).distinct().order_by('-username')
            

        else:
             search_result = User.objects.filter(Q(employeeprofile__profession__icontains=search_element) | Q(employeeprofile__jobplace__description__icontains=search_element) | Q(employeeprofile__jobplace__position_name__icontains=search_element)).distinct().order_by('-username')     
             

        p = Paginator(search_result,6)
        page = request.GET.get('page')
                

        try:
            search_result = p.page(page)
        except PageNotAnInteger:
            search_result = p.page(1)
        except EmptyPage:
            search_result = p.page(p.num_pages)               
                
        context={'search_result':search_result,'categories':categories}
        return render(self.request,'main/search_employee.html',context)
        

        context={'categories':categories} 
        return render(self.request,'main/search_employee.html',context)
    
    
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')
          
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class SeeEmployeeProfile(EmployerRequiredMixin,View):

    def get(self,request,pk):
        
        employee_profile = get_object_or_404(Employeeprofile,pk=pk)


        context={'employee_profile':employee_profile}
        return render(self.request,'main/see_profile.html',context)

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ShowemployerDetails(View):

    def get(self,request,pk):
        
        employer = get_object_or_404(EmployerProfile,pk=pk)
        reviews = EmployerReview.objects.filter(employer=employer).order_by('-review_date')
        review_count = reviews.count()

        try:
            ratio = EmployerRatio.objects.filter(employer=employer,employee=self.request.user.employeeprofile)
        except:
            ratio = {}
       
        p = Paginator(reviews,8)
        page = request.GET.get('page')

        try:
            reviews = p.page(page)
        except PageNotAnInteger:
            reviews = p.page(1)
        except EmptyPage:
            reviews = p.page(p.num_pages) 

            
        context = {'employer':employer,'reviews':reviews,'ratio':ratio,'review_count':review_count}
        return render(self.request,'main/employer_details.html',context)




class FollowEmployeeview(EmployerRequiredMixin,View):

    def get(self,request,pk):

        user = get_object_or_404(User,pk=pk)

        if user.follows.filter(pk=self.request.user.pk):

            user.follows.remove(self.request.user)
            messages.success(self.request,f'You now unfollowed {user}')
            return redirect('see_profile',user.employeeprofile.pk)

        else:

            user.follows.add(self.request.user)
            messages.success(self.request,f'You now followed {user}')

            return redirect('see_profile',user.employeeprofile.pk)
        
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"

        

class ListFollowedEmployeeView(EmployerRequiredMixin,View):

    def get(self,request):

        follows = self.request.user.followed_by.all().order_by('-username')
     

        p = Paginator(follows,5)
        page = request.GET.get('page')

        try:
            follows = p.page(page)
        except PageNotAnInteger:
            follows = p.page(1)
        except EmptyPage:
            follows = p.page(p.num_pages)

        context={'follows':follows}

        return render(self.request,'main/list_followed_employees.html',context)

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class SendMessageView(LoginRequiredMixin,View):


    def post(self,request,pk):

        receiver = get_object_or_404(User, pk=pk)
        sender = self.request.user

        title = self.request.POST.get('messagetitle')
        message = self.request.POST.get('messagebody')

        if message and title:

            Messages.objects.create(title=title,message=message,sender=sender,receiver=receiver)
            messages.success(self.request,f'You now sent message to: {receiver}')

        else:
            messages.error(self.request,'unable to sent nothing')

    
        if receiver.type  == "Employee":
            
            return redirect ('see_profile',receiver.pk)
        else:
            return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class ReplyMessageView(LoginRequiredMixin,View):

    def post(self,request,pk1,pk2):

        receiver = get_object_or_404(User, pk=pk1)
        sender = self.request.user
        message = get_object_or_404(Messages,pk=pk2)

        title = self.request.POST.get('replytitle')
        text_body = self.request.POST.get('replybody')

        if title and text_body:
            Messages.objects.create(receiver=receiver,sender=sender,reply=message,message=text_body,title=title)
            message.checked = True
            message.save()
            messages.success(self.request,f'You now sent message to: {receiver}')
        
        else:
            messages.error(self.request,'Unable to send nothing')

        return redirect('show_messages')    
    


    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ShowMessagesView(LoginRequiredMixin,View):

    def get(self,request):

        return render(self.request,'main/show_messages.html')
    

    login_url = "/login/"
    redirect_field_name = "redirect_to"


class SetMessageRead(LoginRequiredMixin,View):


    def post(self,request):

        messages = Messages.objects.filter(receiver=self.request.user,checked=False)

        for message in messages:
            message.checked=True
            message.save()

        return redirect('show_messages')
    
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"




class UpdateMessage(LoginRequiredMixin, View):
    
    def get(self,request,pk):
        message = get_object_or_404(Messages,pk=pk)
        if message.sender == self.request.user:
            form = MessageForm(instance=message)
            context = {'form':form, 'page_name':'update_message'}
            return render(self.request,'main/universal_form.html',context)
        
        else:
            messages.error(self.request,'Access Denied')
            return redirect('show_messages')
      
    def post(self,request,pk):

        message = get_object_or_404(Messages,pk=pk)

        if message.sender == self.request.user:
            form = MessageForm(self.request.POST,instance=message)
            if form.is_valid():
                form.save()
                messages.success(self.request,'Message has been updated')
                
            else:
                messages.error(self.request,'Unable to modify message')
                
        else:
            messages.error(self.request,'Access Denied')
            
        return redirect('show_messages')

            

    login_url = "/login/"
    redirect_field_name = "redirect_to"


class DeleteMessage(LoginRequiredMixin, View):

    def post(self,request,pk):


        message = get_object_or_404(Messages,pk=pk)

        if message.sender == self.request.user:
            message.delete()
            messages.success(self.request,'Your message has been deleted')
        else:
           
            messages.error(self.request,'Access Denied')

        return redirect('show_messages')
    


class ListEmployeeProfiles(EmployerRequiredMixin,View):

    def get(self,request,pk):

        sector = get_object_or_404(JobCategory,pk=pk)
        profiles = Employeeprofile.objects.filter(sector=sector).order_by('-user')
        profile_count = profiles.count()

        p = Paginator(profiles,6)
        page = request.GET.get('page')

        try:
            profiles = p.page(page)
        except PageNotAnInteger:
            profiles = p.page(1)
        except EmptyPage:
            profiles = p.page(p.num_pages)


        context = {'profiles':profiles,'sector':sector,'profile_count':profile_count}
        return render(self.request,'main/list_employee_profiles.html',context)

        
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class GenerateCV(EmployeeRequiredMixin,View):
    
    def get(self,request):

        user = self.request.user
        schools = EmployeeSchool.objects.filter(employee=user.employeeprofile)
        jobs = EmployeeJobplace.objects.filter(employee=user.employeeprofile)

        context={'user':user,'schools':schools,'jobs':jobs}
        return render(self.request,'main/employeeCV.html',context)
