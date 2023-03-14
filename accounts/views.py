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
from django.views.decorators.csrf import csrf_exempt

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

def oneway_view(req):
    if req.method == 'POST':
        try:
            data = json.loads(req.POST.get('dataflight'))
            flight = data.get('flight')
            return render(req, 'flightcheckout.html', {'flight': flight})
        except json.JSONDecodeError as error:
            return JsonResponse({"error": str(error)})
    else:
        return render(req, 'flights-category.html', {})

def roundtrip_view(req):
    if req.method == 'POST':
        origin = req.POST['origin']
        destination = req.POST['destination']
        departure_date = req.POST['departure_date']
        return_date = req.POST['return_date']
        adults = req.POST['adults']
        children = req.POST['children']
        infants = req.POST['infants']
        travel_class = req.POST['travel_class']
        currency = req.POST['currency']
        non_stop = req.POST['non_stop']
        max_price = req.POST['max_price']
        max = req.POST['max']
        print(origin)
        print(destination)
        print(departure_date)
        print(return_date)
        print(adults)
        print(children)
        print(infants)
        print(travel_class)
        print(currency)
        print(non_stop)
        print(max_price)
        print(max)
        try:
            response = amadeus.shopping.flight_offers_search.get(originLocationCode=origin, destinationLocationCode=destination, departureDate=departure_date, returnDate=return_date, adults=adults, children=children, infants=infants, travelClass=travel_class, currencyCode=currency, nonStop=non_stop, maxPrice=max_price, max=max)
            print(response.data)
            return render(req, 'flights-category-round.html', {'response': response.data})
        except ResponseError as error:
            print(error)
    else:
        return render(req, 'flights-category-round.html', {})

def hotels_view(req):
    if req.method == 'POST':
        city_code = req.POST['city_code']
        check_in_date = req.POST['check_in_date']
        check_out_date = req.POST['check_out_date']
        adults = req.POST['adults']
        children = req.POST['children']
        radius = req.POST['radius']
        radius_unit = req.POST['radius_unit']
        currency = req.POST['currency']
        print(city_code)
        print(check_in_date)
        print(check_out_date)
        print(adults)
        print(children)
        print(radius)
        print(radius_unit)
        print(currency)
        try:
            response = amadeus.shopping.hotel_offers.get(cityCode=city_code, checkInDate=check_in_date, checkOutDate=check_out_date, adults=adults, radius=radius, radiusUnit=radius_unit, currencyCode=currency)
            print(response.data)
            return render(req, 'hotels.html', {'response': response.data})
        except ResponseError as error:
            print(error)
    else:
        return render(req, 'hotels.html', {})

def profile_view(req):
    return render(req, 'profile.html', {})

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

def search_flights(request):
    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        departure_date = request.POST.get('departure_date')
        return_date = request.POST.get('return_date')
        adults = request.POST.get('adults')
        children = request.POST.get('children')

        try:
            flights = amadeus_api.shopping.flight_offers_search.get(
                origin=origin,
                destination=destination,
                departureDate=departure_date,
                returnDate=return_date,
                adults=adults,
                children=children
            )
        except ResponseError as error:
            print(error)
            flights = []
            print(flights)

        return render(request, 'flight_search/results.html', {'flights': flights})

    return render(request, 'flight_search/search.html')
