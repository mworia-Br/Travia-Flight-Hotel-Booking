from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, CustomPasswordResetForm, EmailAuthenticationForm, CustomAuthenticationForm

from amadeus import Client, ResponseError, Location

amadeus = Client(
    client_id='zUlxNy4Kc6l5oSALcurajPCAUaYpDq1s',
    client_secret='K95GQ2APHlRQ0R1l'
)

# Create your views here.

@login_required(login_url='login')
def Index(req):
    return render(req, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            user.set_password(password)
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'login.html', {})
'''
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'login.html', {})
'''
def logout_view(request):
    logout(request)
    return redirect('login')

def password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('password_reset_done')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'password_reset_invalid.html')
