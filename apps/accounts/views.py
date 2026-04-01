from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm


# ============================================================
# Login View
# Handles both GET and POST requests
# GET  — just shows the login form
# POST — validates credentials and logs the user in
# ============================================================
def login_view(request):

    # if the user is already logged in, send them straight to dashboard
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    form = LoginForm()

    if request.method == 'POST':
        # fill the form with the submitted data
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # authenticate checks if the username and password are correct
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # credentials are correct — log the user in
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('core:dashboard')
            else:
                # credentials are wrong — show an error message
                messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'accounts/login.html', {'form': form})


# ============================================================
# Logout View
# Logs the user out and redirects to login page
# ============================================================
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login') 