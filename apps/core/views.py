from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# login_required means only logged-in users can access this view
# anyone not logged in gets redirected to the login page
@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')