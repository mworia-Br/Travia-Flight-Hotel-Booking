from django.shortcuts import render
from django.views import View
from .forms import TravelerForm


class TravelerView(View):
    template_name = 'traveler.html'

    def get(self, request, *args, **kwargs):
        form = TravelerForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = TravelerForm(request.POST)
        if form.is_valid():
            traveler_id = form.cleaned_data.get('id')
            traveler_name_first = form.cleaned_data.get('first_name')
            traveler_name_last = form.cleaned_data.get('last_name')
            traveler_date_of_birth = form.cleaned_data.get('date_of_birth')
            traveler_gender = form.cleaned_data.get('gender')
            traveler_email = form.cleaned_data.get('email')
            traveler_phone_device = form.cleaned_data.get('phone_device')
            traveler_phone_country_code = form.cleaned_data.get('phone_country_code')
            traveler_phone_number = form.cleaned_data.get('phone_number')
            traveler_doc_type = form.cleaned_data.get('doc_type')
            traveler_doc_birthplace = form.cleaned_data.get('doc_birthplace')
            traveler_doc_issuance_location = form.cleaned_data.get('doc_issuance_location')
            traveler_doc_issuance_date = form.cleaned_data.get('doc_issuance_date')
            traveler_doc_number = form.cleaned_data.get('doc_number')
            traveler_doc_expiry_date = form.cleaned_data.get('doc_expiry_date')
            traveler_doc_issuance_country = form.cleaned_data.get('doc_issuance_country')
            traveler_doc_validity_country = form.cleaned_data.get('doc_validity_country')
            traveler_doc_nationality = form.cleaned_data.get('doc_nationality')
            traveler_doc_holder = form.cleaned_data.get('doc_holder')
            traveler = {
                "id": traveler_id,
                "dateOfBirth": traveler_date_of_birth,
                "name": {"firstName": traveler_name_first, "lastName": traveler_name_last},
                "gender": traveler_gender,
                "contact": {
                    "emailAddress": traveler_email,
                    "phones": [
                        {
                            "deviceType": traveler_phone_device,
                            "countryCallingCode": traveler_phone_country_code,
                            "number": traveler_phone_number,
                        }
                    ],
                },
                "documents": [
                    {
                        "documentType": traveler_doc_type,
                        "birthPlace": traveler_doc_birthplace,
                        "issuanceLocation": traveler_doc_issuance_location,
                        "issuanceDate": traveler_doc_issuance_date,
                        "number": traveler_doc_number,
                        "expiryDate": traveler_doc_expiry_date,
                        "issuanceCountry": traveler_doc_issuance_country,
                        "validityCountry": traveler_doc_validity_country,
                        "nationality": traveler_doc_nationality,
                        "holder": traveler_doc_holder,
                    }
                ],
            }
            context = {'traveler': traveler}
            return render(request, 'success.html', context)
        else:
            context = {'form': form}
            return render(request, self.template_name, context)
