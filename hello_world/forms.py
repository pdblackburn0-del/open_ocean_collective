from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):  # <- must match settings.py
    age = forms.IntegerField(required=True)
    surfing_ability = forms.ChoiceField(
        choices=[('beginner','Beginner'), 
                 ('intermediate','Intermediate'), 
                 ('advanced','Advanced')
            ]
    )
    county = forms.CharField(required=True)

    def save(self, request):
        user = super().save(request)
        user.profile.age = self.cleaned_data['age']
        user.profile.surfing_ability = self.cleaned_data['surfing_ability']
        user.profile.county = self.cleaned_data['county']
        user.profile.save()
        return user