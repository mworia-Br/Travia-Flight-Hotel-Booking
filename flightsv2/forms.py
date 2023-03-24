from django import forms


class TravelerForm(forms.Form):
    id = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    date_of_birth = forms.DateField()
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    email = forms.EmailField()
    PHONE_DEVICE_CHOICES = [
        ('MOBILE', 'Mobile'),
        ('HOME', 'Home'),
        ('WORK', 'Work'),
        ('OTHER', 'Other'),
    ]
    phone_device = forms.ChoiceField(choices=PHONE_DEVICE_CHOICES)
    phone_country_code = forms.CharField(max_length=5)
    phone_number = forms.CharField(max_length=15)
    DOC_TYPE_CHOICES = [
        ('PASSPORT', 'Passport'),
        ('DRIVERS_LICENSE', "Driver's License"),
        ('NATIONAL_ID', 'National ID'),
        ('OTHER', 'Other'),
    ]
    doc_type = forms.ChoiceField(choices=DOC_TYPE_CHOICES)
    doc_birthplace = forms.CharField(max_length=50)
    doc_issuance_location = forms.CharField(max_length=50)
    doc_issuance_date = forms.DateField()
    doc_number = forms.CharField(max_length=50)
    doc_expiry_date = forms.DateField()
    doc_issuance_country = forms.CharField(max_length=50)
    doc_validity_country = forms.CharField(max_length=50)
    doc_nationality = forms.CharField(max_length=50)
    doc_holder = forms.BooleanField(required=False)
