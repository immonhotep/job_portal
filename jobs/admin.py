from django.contrib import admin

from .models import JobPossibility,JobCategory,JobApplication

admin.site.register(JobPossibility)
admin.site.register(JobCategory)
admin.site.register(JobApplication)
