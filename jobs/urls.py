from django.urls import path
from .views import *

urlpatterns = [

    path('employer_add_job/',AddNewJobView.as_view(),name='employer_add_job'),
    path('employer_list_jobs/',ListEmployerJobsView.as_view(),name='employer_list_jobs'),
    path('delete_employer_job/<int:pk>/',DeleteEmployerJobView.as_view(),name="delete_employer_job"),
    path('update_employer_job/<int:pk>/',UpdateEmployerJobView.as_view(),name='update_employer_job'),
    path('employee_search_job/',EmployeeSearchJobView.as_view(),name='employee_search_job'),
    path('show_job_category_list/<int:pk>/',ShowJobCategorylist.as_view(),name='show_job_category_list'),
    path('show_employer_jobs/<int:pk>/',ShowEmployerJobsView.as_view(),name='show_employer_jobs'),
    path('job_detail/<int:pk>/',EmployeeJobDetailView.as_view(),name='job_detail'),
    path('send_apply/<int:pk>/',ApplyJobView.as_view(),name='send_apply'),
    path('list_applies/',ListJobApplyView.as_view(),name='list_applies'),
    path('remove_apply/<int:pk>/',RemoveJobApplyView.as_view(),name="remove_apply"),
    path('archive_apply/<int:pk>/',ArchiveJobApplyView.as_view(),name='archive_apply'),
    path('show_candidates/<int:pk>/',ShowJobCandidates.as_view(),name="show_candidates"),
    path('show_application/<int:pk>/',ApplicationDetailView.as_view(),name='show_application'),
    path('send_review/<int:pk>/',SendEmployerReviewView.as_view(),name='send_review'),
    path('show_reviews/',MyReviewsView.as_view(),name='show_reviews'),
    path('delete_review/<int:pk>/',DeleteReviewView.as_view(),name='delete_review'),
    path('modify_review/<int:pk>/',ModifyReviewView.as_view(),name='modify_review'),
    path('send_star_rating/<int:pk>/',SendStarRatingView.as_view(),name='send_star_rating'),
    path('show_employee_applications/',ShowEmployeeApplications.as_view(),name='show_employee_applications'),

    path('list_category/',ListJobCategoryView.as_view(),name='list_category'),
    path('add_job_category/',AddJobCategoryView.as_view(),name='add_job_category'),
    path('edit_job_category/<int:pk>/',ModifyJobCategoryView.as_view(),name='edit_job_category'),
    path('delete_category/<int:pk>/',DeleteJobCategoryView.as_view(),name='delete_category'),
    path('make_notification/',SendJobNotification.as_view(),name="make_notification"),
    path('show_notified_jobs/',ViewNotifiedJobs.as_view(),name='show_notified_jobs'),
    path('delete_notification',DeleteNotification.as_view(),name='delete_notification'),

]
