from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm


# ============================================================
# Login View
# ============================================================
def login_view(request):
    # already logged in — go to dashboard
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('core:dashboard')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'accounts/login.html', {'form': form})


# ============================================================
# Register View
# New users register using the firm's registration code
# ============================================================
def register_view(request):
    # already logged in — go to dashboard
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('accounts:login')

    return render(request, 'accounts/register.html', {'form': form})


# ============================================================
# Logout View
# ============================================================
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')