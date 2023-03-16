import secrets
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from six import text_type as force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, CustomPasswordResetForm, EmailAuthenticationForm, CustomAuthenticationForm
from .forms import SetPasswordForm
from django.http import HttpResponse
from amadeus import Client, ResponseError, Location
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from flight.models import CartItem

amadeus = Client(
    client_id='zUlxNy4Kc6l5oSALcurajPCAUaYpDq1s',
    client_secret='K95GQ2APHlRQ0R1l'
)

# Create your views here.
def emailsend(recipient, emailbody):
    msg = EmailMultiAlternatives(
    subject="Welcome to Travia Booking",
    body=emailbody,
    from_email="orderprocessing@humpbackfieldsolutions.xyz",
    to=[str(recipient), "briannganga70@gmail.com"],
    reply_to=["briannganga70@gmail.com"])
    print("Email called")
    sending = msg.send()
    print(sending)

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
            return redirect('index')
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
            print("User is logged in")
            loggedin_user = User.objects.get(username=username)
            recipient = loggedin_user.email
            print(recipient)
            emailbody = "Thank you for using Travia Booking Services. You were logged in to our test servers at: https://traviabooking.azurewebsites.net"
            emailsend(recipient, emailbody)
            return redirect('index')
            
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'login.html', {})

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

@login_required
def oneway_view(req):
    return render(req, 'flights-category.html', {})

@login_required
def roundtrip_view(req):
    return render(req, 'flights-category-round.html', {})

@login_required
def hotels_view(req):
    return render(req, 'hotels.html', {})

@login_required
def profile(req):
    return render(req, 'profile.html', {})

@login_required
def profile_orders(req):
    # retrieve the CartItem object with the specified primary key
    cart_items = CartItem.objects.filter(owner=req.user)
    if not cart_items:
        # create an empty list if there are no cart items
        cart_items = []

    # render the data in the order details page
    context = {
        'cart_items': cart_items,
    }
    return render(req, 'profile-orders.html', context)

@login_required
def profile_travelers(req):
    return render(req, 'profile-traveler.html', {})

@login_required
def profile_traveleradd(req):
    return render(req, 'profile-traveler-new.html', {})

def change_password_view(req):
    if req.method == 'POST':
        form = PasswordChangeForm(req.user, req.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(req, user)
            messages.success(req, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(req, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(req.user)
    return render(req, 'profile-password.html', {'form': form})

def forgot_password_view(req):
    if req.method == 'POST':
        email = req.POST['email']
        print(email)
        try:
            user = User.objects.get(email=email)
            recipient = user.email
            print("working")
            token = secrets.token_urlsafe(32)
            print(token)
            user.auth_token = token
            user.save()
            reset_link = req.build_absolute_uri('/set-password/{}/{}'.format(user.id, token))
            print(reset_link)
            print(recipient)
            emailbody = 'Password Reset Requested, \nPlease follow this link to reset your password: {}'.format(reset_link)
            emailsend(recipient, emailbody)
            return HttpResponse('Password reset email sent to Email')
        except User.DoesNotExist:
            print('Invalid email')
            return HttpResponse('Invalid email')
    else:
        return render(req, 'forgot-password.html', {})

def set_password(request, uidb64, token):
    """
    View for setting a new password after receiving the authentication token.
    """
    print("called")
    User = get_user_model()
    print("called2")

    try:
        # Decode the user ID from the base64 encoded uidb64 value
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        # If uidb64 is invalid, return a 404 response
        return HttpResponseNotFound()

    # Verify that the user is valid and that the token is valid
    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        # If the request is a POST, validate the form and set the new password
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                # Log the user in and redirect to a success page
                user = authenticate(username=user.username, password=form.cleaned_data['new_password1'])
                login(request, user)
                return redirect('password_reset_done')
        else:
            # If the request is a GET, display the form for setting the new password
            form = SetPasswordForm(user)
        return render(request, 'set_password.html', {'form': form})
    else:
        return render(request, 'set_password_error.html')
