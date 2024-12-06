from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser
    

class EmployeeRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):

        try:
            self.request.user.employeeprofile
            return self.request.user.employeeprofile
        
        except:
            return False


class EmployerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):

        try:
            self.request.user.employerprofile
            return self.request.user.employerprofile
        
        except:
             return False