from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import JobPossibilityForm,JobcategoryForm,ApplicationForm,EmployeeReviewForm,NotificationForm
from .models import JobPossibility,JobCategory,JobApplication,JobNotification
from  main.models import EmployerReview
from main.models import EmployerProfile,EmployerRatio
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django .views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .mixins import SuperUserRequiredMixin,EmployeeRequiredMixin,EmployerRequiredMixin
from django.db.models import Q




class AddNewJobView(EmployerRequiredMixin,View):


    def get(self,request):

        self.request.user.employerprofile
        form = JobPossibilityForm()
        context={'form':form,'page_name':'add_jobs'}
        return render(self.request,'jobs/universal_form.html',context)
        

    def post(self,request):

            form = JobPossibilityForm(self.request.POST)
            if form.is_valid():

                job = form.save(commit=False)
                job.employer = self.request.user.employerprofile
                job.save()

                messages.success(self.request,'New job added')
                return redirect('home')
            
            else:

                for error in list(form.errors.values()):
                    messages.error(self.request,error)
                    return redirect('add_job')


    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ListEmployerJobsView(EmployerRequiredMixin,View):

    def get(self,request):

        selection = request.GET.get("status","")

        if selection == "YES":
            myjobs = JobPossibility.objects.filter(employer=self.request.user.employerprofile,valid=False).order_by('-publication_date')
            request.session['selection'] = "YES"
            
            
        elif selection == "NO":
            myjobs = JobPossibility.objects.filter(employer=self.request.user.employerprofile,valid=True).order_by('-publication_date')
            request.session['selection'] = "NO"

        elif selection == "ONGOING":

            jobs = JobPossibility.objects.filter(employer=self.request.user.employerprofile,valid=True)
            myjobs = []
            for job in jobs:
                if job.applications.count() >= 1:
                    myjobs.append(job)

            request.session['selection'] = "ONGOING"

        else:
           myjobs = JobPossibility.objects.filter(employer=self.request.user.employerprofile).order_by('-publication_date')
           request.session['selection'] = "ALL"
      
       
        p = Paginator(myjobs,4)
        page = request.GET.get('page')
                

        try:
            myjobs = p.page(page)
        except PageNotAnInteger:
            myjobs = p.page(1)
        except EmptyPage:
            myjobs = p.page(p.num_pages)

        context={'myjobs':myjobs}
        return render(self.request,'jobs/list_employer_jobs.html',context)
    

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"


class DeleteEmployerJobView(EmployerRequiredMixin,View):

    def post(self,request,pk):

        job = get_object_or_404(JobPossibility,pk=pk)

        if job.employer == self.request.user.employerprofile:

            job.delete()
            messages.success(self.request,f'{job.title} successfully removed')
            return redirect('employer_list_jobs')

        else:
            messages.error(self.request,'Access Denied')
            return redirect('employer_list_jobs')


    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"




class UpdateEmployerJobView(EmployerRequiredMixin,View):

    def get(self,request,pk):

        job = get_object_or_404(JobPossibility,pk=pk)

        if job.employer == self.request.user.employerprofile:

            form = JobPossibilityForm(instance=job)
            context={'form':form,'page_name':'update_job'}
            return render(self.request,'jobs/universal_form.html',context)

        else:

            messages.error(self.request,'Access Denied')
            return redirect('employer_list_jobs')

        

    def post(self,request,pk):

        job = get_object_or_404(JobPossibility,pk=pk)

        if job.employer == self.request.user.employerprofile:

            form = JobPossibilityForm(self.request.POST,instance=job)

            if form.is_valid():
                form.save()
                messages.success(self.request,f'You successfully modified job: {job.title}')
                return redirect('employer_list_jobs')
            
            else:

                for error in list(form.errors.values()):
                    messages.error(self.request,error)
                    return redirect('update_employer_job',job.pk)

        else:

            messages.error(self.request,'Access Denied')
            return redirect('employer_list_jobs')

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"




class EmployeeSearchJobView(View):

    def get(self,request):

        categories = JobCategory.objects.all()

        search_category = request.GET.get('category',"")
        search_school = request.GET.get('school',"")
        search_location = request.GET.get('location',"")
        search_input = request.GET.get('search',"")

        quicksearch = request.GET.get('quicksearch',"")
       
        

        if quicksearch:
          
            search_input = quicksearch
          
    


        if  search_category == "" and search_school == "" and search_location == "" and search_input == "":
            context={'categories':categories}
            return render(self.request,'jobs/employee_search_job.html',context)


        if search_category != "":
            jobs = JobPossibility.objects.filter(Q(job_type=search_category) & Q(required_school__icontains=search_school) & (Q(title__icontains=search_input) | Q(employer__company_name__icontains=search_input))& Q(job_location__icontains=search_location)).order_by('-title')
          
        else:
            jobs = JobPossibility.objects.filter(Q(required_school__icontains=search_school) & (Q(title__icontains=search_input) | Q(employer__company_name__icontains=search_input))  & Q(job_location__icontains=search_location)).order_by('-title')

        p = Paginator(jobs,4)
        page = request.GET.get('page')
                    

        try:
            jobs = p.page(page)
        except PageNotAnInteger:
            jobs = p.page(1)
        except EmptyPage:
            jobs = p.page(p.num_pages)

        context={'categories':categories,'jobs':jobs,'quicksearch':quicksearch}
        return render(self.request,'jobs/employee_search_job.html',context)
    


class ShowJobCategorylist(View):

    def get(self,request,pk):


        category = get_object_or_404(JobCategory,pk=pk)
        jobs = JobPossibility.objects.filter(job_type=category,valid=True).order_by('-publication_date')

        p = Paginator(jobs,4)
        page = request.GET.get('page')
                    

        try:
            jobs = p.page(page)
        except PageNotAnInteger:
            jobs = p.page(1)
        except EmptyPage:
            jobs = p.page(p.num_pages)

        context = {'jobs':jobs,'category':category}
        return render(self.request,'jobs/job_category_list.html',context)
    


class  ShowEmployerJobsView(View):

    def get (self,request,pk):

        employer = get_object_or_404(EmployerProfile,pk=pk)
        jobs = JobPossibility.objects.filter(employer=employer,valid=True).order_by('-title')

        p = Paginator(jobs,4)
        page = request.GET.get('page')
                    

        try:
            jobs = p.page(page)
        except PageNotAnInteger:
            jobs = p.page(1)
        except EmptyPage:
            jobs = p.page(p.num_pages)


        context={'employer':employer,'jobs':jobs}
        return render(self.request,'jobs/employer_jobs.html',context)




class EmployeeJobDetailView(View):

    def get(self,request,pk):

        job = get_object_or_404(JobPossibility,pk=pk)

        context={'job':job}
        return render(self.request,'jobs/job_detail.html',context)
    


class ApplyJobView(EmployeeRequiredMixin,View):

    def post(self,request,pk):

        job = get_object_or_404(JobPossibility,pk=pk)

        application, created = JobApplication.objects.get_or_create(job=job,applicant=self.request.user.employeeprofile)

        if created:
            messages.success(self.request,'You now succefully sent apply')
        else:
            messages.info(self.request,'You already sent apply for this job')
            
        return redirect('job_detail',job.pk)


    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')
        
 
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ListJobApplyView(EmployeeRequiredMixin,View):

    def get(self,request):

        status = request.GET.get('applies',"")

        if status == "ALL":
            jobapplies = JobApplication.objects.filter(applicant = self.request.user.employeeprofile).order_by('-date')
            request.session['selection'] = "ALL"

        elif status == "ARCHIVED":
            jobapplies = JobApplication.objects.filter(applicant = self.request.user.employeeprofile,archived=True).order_by('-date')
            request.session['selection'] = "ARCHIVED"

        else:
            jobapplies = JobApplication.objects.filter(applicant = self.request.user.employeeprofile,archived=False).order_by('-date')
            request.session['selection'] = "CURRENT"



        p = Paginator(jobapplies,3)
        page = request.GET.get('page')
                    

        try:
            jobapplies = p.page(page)
        except PageNotAnInteger:
            jobapplies = p.page(1)
        except EmptyPage:
            jobapplies = p.page(p.num_pages)

        return render(request,'jobs/list_job_applies.html',context={'jobapplies':jobapplies})
    
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')
        
 
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ShowJobCandidates(EmployerRequiredMixin,View):

    def get(self,request,pk):

        job = get_object_or_404(JobPossibility,pk=pk)
        applications = JobApplication.objects.filter(job=job)

        if job.employer == self.request.user.employerprofile:
            context={'applications':applications,'job':job}
            return render(self.request,'jobs/list_candidates.html',context)
        else:
            messages.error(self.request,'Access Denied')
            return redirect('home')


    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')
        
 
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class RemoveJobApplyView(EmployeeRequiredMixin,View):

    
    def post(self,request,pk):

        apply = get_object_or_404(JobApplication,pk=pk)

        if apply.applicant == self.request.user.employeeprofile:

            apply.delete()
            messages.success(self.request,'Your application has been removed')
            return redirect('list_applies')
    
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')
        
 
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ArchiveJobApplyView(EmployeeRequiredMixin,View):

    
    def post(self,request,pk):

        apply = get_object_or_404(JobApplication,pk=pk)

        if apply.applicant == self.request.user.employeeprofile:
            apply.archived = True
            apply.save()
            messages.success(self.request,'Your application has been archived')
            return redirect('list_applies')
    
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')
        
 
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class ApplicationDetailView(EmployerRequiredMixin,View):

    def get(self,request,pk):

        application = get_object_or_404(JobApplication,pk=pk)

        if application.job.employer == self.request.user.employerprofile:

            form = ApplicationForm(instance=application)

            context={'application':application,'form':form}
            return render(self.request,'jobs/show_application.html',context)
        
        else:
            messages.error(self.request,'Access denied')
            return redirect('home')

    def post(self,request,pk):

        application = get_object_or_404(JobApplication,pk=pk)

        if application.job.employer == self.request.user.employerprofile:

            form = ApplicationForm(self.request.POST,instance=application)
            if form.is_valid():
                app=form.save()
                job = app.job

                if app.status == "Hired":
                    app.job.valid = False
                    job.save()

                else:
                    app.job.valid = True
                    job.save()

            
                messages.success(self.request,f'You modified the application status to: {app.status}')

            return redirect('show_candidates',application.job.pk)
        
        else:
            messages.error(self.request,'Access denied')
            return redirect('home')

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home')

    login_url = "/login/"
    redirect_field_name = "redirect_to"




class ListJobCategoryView(SuperUserRequiredMixin,View):

    def get(self,request):

        categories = JobCategory.objects.all()
        context = {'categories':categories}
        return render(self.request,'main/home.html',context)
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ModifyJobCategoryView(SuperUserRequiredMixin,View):

    def get(self,request,pk):

        category = get_object_or_404(JobCategory,pk=pk)

        form = JobcategoryForm(instance=category)
        context={'form':form}
        return render(self.request,'jobs/universal_form.html',context)
    

    def post(self,request,pk):

        category = get_object_or_404(JobCategory,pk=pk)

        form = JobcategoryForm(self.request.POST,instance=category)
        if form.is_valid():
            item = form.save()

            messages.success(self.request,f'{category.category_name} has been modified')
            return redirect('list_category')
        else:
            messages.error(self.request,'Something bad happend')
            return redirect('list_category')

    login_url = "/login/"
    redirect_field_name = "redirect_to"




class AddJobCategoryView(SuperUserRequiredMixin,View):

    def get(self,request):

        form = JobcategoryForm()
        context={'form':form,'page_name':'add_category'}
        return render(self.request,'jobs/universal_form.html',context)
    
    def post(self,request):

        form = JobcategoryForm(self.request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(self.request,f'new category has been created:{category.category_name}')
            return redirect('add_job_category')
        else:
            messages.error(self.request,'Something bad happend')
            return redirect('add_job_category')
        

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class DeleteJobCategoryView(SuperUserRequiredMixin,View):

    def post(self,request,pk):
        category = get_object_or_404(JobCategory,pk=pk)
        category.delete()
        messages.success(self.request,'Category has been removed')
        return redirect('list_category')
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class SendEmployerReviewView(EmployeeRequiredMixin,View):


    def post(self,request,pk):

        employer = get_object_or_404(EmployerProfile,pk=pk)

        review = self.request.POST.get('reviewbody')

        if review:
            EmployerReview.objects.create(employer=employer,employee=self.request.user.employeeprofile,review=review)
            messages.success(self.request,'Your review has been saved')
        else:
            messages.error(self.request,'You sent nothing')

        return redirect('employer_detail',employer.pk)
    

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home') 
     
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class MyReviewsView(EmployeeRequiredMixin,View):

    def get(self,request):

        reviews = EmployerReview.objects.filter(employee=self.request.user.employeeprofile).order_by('-review_date')
        reviews_count = reviews.count()

        p = Paginator(reviews,6)
        page = request.GET.get('page')
                    

        try:
            reviews = p.page(page)
        except PageNotAnInteger:
            reviews = p.page(1)
        except EmptyPage:
            reviews = p.page(p.num_pages)

        context = {'reviews':reviews,'reviews_count':reviews_count}
        return render(self.request,'jobs/reviews.html',context)
    

    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home') 
     
    login_url = "/login/"
    redirect_field_name = "redirect_to"




class DeleteReviewView(EmployeeRequiredMixin,View):

    def post(self,request,pk):

        review = get_object_or_404(EmployerReview,pk=pk)

        if review.employee == self.request.user.employeeprofile:

            review.delete()
            messages.success(self.request,'Your review has been deleted')
            return redirect('show_reviews')
        
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home') 
     
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class ModifyReviewView(EmployeeRequiredMixin,View):

    def get(self,request,pk):

        review = get_object_or_404(EmployerReview,pk=pk)

        if review.employee == self.request.user.employeeprofile:

            form = EmployeeReviewForm(instance=review)
            context={'form':form}
            return render(self.request,'jobs/universal_form.html',context)
        else:
            messages.error(self.request,'Access Denied')
            return redirect('show_reviews')

    def post(self,request,pk):

        review = get_object_or_404(EmployerReview,pk=pk)

        if review.employee == self.request.user.employeeprofile:

            form = EmployeeReviewForm(self.request.POST,instance=review)
            if form.is_valid():
                form.save()
                messages.success(self.request,'Your review has been modified')
                return redirect('show_reviews')
            else:
                 messages.error(self.request,'Something bad happend')
                 return redirect('show_reviews') 

        else:
            messages.error(self.request,'Access Denied')
            return redirect('show_reviews')


    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home') 
     
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class SendStarRatingView(EmployeeRequiredMixin,View):

    def post(self,request,pk):

        employer = get_object_or_404(EmployerProfile,pk=pk)
        employee = self.request.user.employeeprofile
        rating = EmployerRatio.objects.filter(employee=employee,employer=employer)

        if not rating:
            
            star = self.request.POST.get('star')
            rate_range, created = EmployerRatio.objects.get_or_create(employer=employer,employee=employee,star_rating=star)


            if  created:
                messages.success(self.request,'Your rating has been saved')
                
        return redirect('employer_detail',employer.pk)


    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home') 
     
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ShowEmployeeApplications(EmployerRequiredMixin,View):

    def get(self,request):

        applications = JobApplication.objects.filter(job__employer=self.request.user.employerprofile).order_by('-date')

      
        p = Paginator(applications,8)
        page = request.GET.get('page')
                    

        try:
            applications = p.page(page)
        except PageNotAnInteger:
            applications = p.page(1)
        except EmptyPage:
            applications = p.page(p.num_pages)


        context={'applications':applications}
        return render(self.request,'jobs/show_applications.html',context)
    


    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home') 
     
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class SendJobNotification(EmployeeRequiredMixin,View):

    def get(self,request):

        notification = JobNotification.objects.filter(employee=self.request.user.employeeprofile).first()

        form = NotificationForm(instance=notification)

        context= {'form':form,'page_name':'notifications'}
        return render(self.request,'jobs/universal_form.html',context)

    def post(self,request):

        notification = JobNotification.objects.filter(employee=self.request.user.employeeprofile).first()

        form = NotificationForm(self.request.POST,instance=notification)
        if form.is_valid():

            data = form.save(commit=False)
            data.employee = self.request.user.employeeprofile
            data.save()
            messages.success(self.request,'Your job notification has been saved')
            return redirect('show_notified_jobs')

            
        else:
            for error in list(form.error.values()):
                messages.error(self.request,error)
                return redirect('make_notification')


        


    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home') 
     
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class ViewNotifiedJobs(EmployeeRequiredMixin,View):

    def get(self,request):

        notification = JobNotification.objects.filter(employee=self.request.user.employeeprofile).first()
        jobs = JobPossibility.objects.filter(Q(title__icontains=notification.title) & Q(required_school__icontains=notification.required_school) & Q(job_type=notification.job_type) & Q(job_location__icontains=notification.job_location)).distinct().order_by('-title')
        jobs_count = jobs.count()

        p = Paginator(jobs,4)
        page = request.GET.get('page')
                    

        try:
            jobs = p.page(page)
        except PageNotAnInteger:
            jobs = p.page(1)
        except EmptyPage:
            jobs = p.page(p.num_pages)

        context={'jobs':jobs,'jobs_count':jobs_count}
        return render(self.request,'jobs/notified_jobs.html',context)
    
    def handle_no_permission(self):
        messages.error(self.request,'Access Denied')
        return redirect('home') 
     
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class DeleteNotification(EmployeeRequiredMixin,View):

    def post(self,request):

      notification = JobNotification.objects.filter(employee=self.request.user.employeeprofile).first()
      notification.delete()
      messages.success(self.request,'Your job notifications has been removed')
      return redirect('home')
    












    

