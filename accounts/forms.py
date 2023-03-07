from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm


class SetPasswordForm(BaseSetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'email'


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        fields = ('email',)

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    new_password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))

    class Meta:
        fields = ('new_password1', 'new_password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))

    class Meta:
        fields = ('username', 'password')

class OneWayFlightSearchForm(ModelForm):
    class Meta:
        model = models.OneWayFlightSearch
        fields = ('origin', 'destination', 'departure_date', 'adults', 'children',
        'infants', 'travel_class', 'non_stop', 'currency', 'max_price')

class TwoWayFlightSearchForm(ModelForm):
    class Meta:
        model = models.TwoWayFlightSearch
        fields = ('origin', 'destination', 'departure_date', 'return_date', 'adults', 'children',
        'infants', 'travel_class', 'non_stop', 'currency', 'max_price')
