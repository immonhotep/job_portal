from .models import Messages
from jobs.models import JobNotification
from django.db.models import Q
from django.db.models import Count

def base_page_context(request):

    if request.user.is_authenticated: 
        notes = Messages.objects.filter(receiver=request.user) | Messages.objects.filter(sender=request.user).order_by('-date')

        try:
            notifications = JobNotification.objects.filter(employee=request.user.employeeprofile)

        except:
            notifications = {}
        
        unread_notes = notes.filter(checked=False,receiver=request.user)
        notes_count = notes.count()

        if notes:
            return {'notes': notes,'unread_notes':unread_notes,'notifications':notifications }
        
        else:
            return {'notifications':notifications}
        

           
        
    else:

        return {}