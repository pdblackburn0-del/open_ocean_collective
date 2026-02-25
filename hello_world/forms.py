from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    age = forms.IntegerField(required=True)
    surfing_ability = forms.ChoiceField(
        choices=[
            ('beginner','Beginner'),
            ('intermediate','Intermediate'),
            ('advanced','Advanced'),
        ]
    )
    county = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def save(self, request):
        user = super().save(request)
        user.profile.age = self.cleaned_data['age']
        user.profile.surfing_ability = self.cleaned_data['surfing_ability']
        user.profile.county = self.cleaned_data['county']
        user.profile.save()
        return user