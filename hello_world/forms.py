from allauth.account.forms import SignupForm
from django import forms
from django.core.exceptions import ValidationError

class CustomSignupForm(SignupForm):
    age = forms.IntegerField(
        required=True,
        min_value=18,
        max_value=100,
        help_text="Must be between 18 and 100 years old"
    )
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

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None:
            if age < 18:
                raise ValidationError('You must be at least 18 years old to join.')
            if age > 100:
                raise ValidationError('Please enter a valid age.')
        return age

    def save(self, request):
        user = super().save(request)
        user.profile.age = self.cleaned_data['age']
        user.profile.surfing_ability = self.cleaned_data['surfing_ability']
        user.profile.county = self.cleaned_data['county']
        user.profile.save()
        return user