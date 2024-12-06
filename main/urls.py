
from django.urls import path
from .views import *
from . import  views
 
urlpatterns = [
    path('',Homeview.as_view(),name='home'),
    path('signup_employee/',EmployeeSignupview.as_view(),name='signup_employee'),
    path('signup_employer/',EmployerSignupview.as_view(),name='signup_employer'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('change_password/',CustompasswordchangeView.as_view(),name='change_password'),
    path('update_employee/',UpdateEmployeeview.as_view(),name='update_employee'),
    path('update_employer/',UpdateEmployerview.as_view(),name='update_employer'),
    path('navbarstyle',SetNavbarStyle.as_view(),name='navbarstyle'),
    path('studies/',StudiesView.as_view(),name='studies'),
    path('add_study',AddnewStudyView.as_view(),name='add_study'),
    path('update_study/<int:pk>/',EditStudyView.as_view(),name='update_study'),
    path('delete_study/<int:pk>/',DeleteStudyView.as_view(),name='delete_study'),
    path('jobs/',JobsView.as_view(),name='jobs'),
    path('add_job/',AddnewJobView.as_view(),name="add_job"),
    path('update_job/<int:pk>/',EditJobView.as_view(),name='update_job'),
    path('delete_job/<int:pk>/',DeleteJobView.as_view(),name='delete_job'),
    path('search_employee/',SearchEmployeeView.as_view(),name='search_employee'),
    path('see_profile/<int:pk>/',SeeEmployeeProfile.as_view(),name='see_profile'),
    path('employer_detail/<int:pk>/',ShowemployerDetails.as_view(),name='employer_detail'),
    path('follow_employee/<int:pk>/',FollowEmployeeview.as_view(),name='follow_employee'),
    path('list_followed_employee/',ListFollowedEmployeeView.as_view(),name='list_followed_employee'),
    path('list_employee_profiles/<int:pk>/',ListEmployeeProfiles.as_view(),name='list_employee_profiles'),
    path('reply_message/<int:pk1>/<int:pk2>/',ReplyMessageView.as_view(),name='reply_message'),
    
    path('send_message/<int:pk>/',SendMessageView.as_view(),name='send_message'),
    path('show_messages/',ShowMessagesView.as_view(),name='show_messages'),
    path('update_message/<int:pk>/',UpdateMessage.as_view(),name='update_message'),
    path('delete_message/<int:pk>/',DeleteMessage.as_view(),name='delete_message'),
    path('set_to_read/',SetMessageRead.as_view(),name='set_to_read'),

    path('profile_CV',GenerateCV.as_view(),name='profile_CV'),
    
    
]
