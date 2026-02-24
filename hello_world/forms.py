from allauth.account.forms import SignupForm
from django import forms
from .models import Story

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


class StoryForm(forms.ModelForm):
    """Form for users to create and share their surf stories"""
    
    class Meta:
        model = Story
        fields = ['title', 'content', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Give your story a title',
                'maxlength': '255'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your inspiring surf story... (Tell us about your journey, what surfing means to you, how Open Ocean Collective has impacted you)',
                'rows': 8,
                'style': 'resize: vertical;'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Image URL (e.g., https://example.com/image.jpg)',
                'required': False
            })
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 50:
            raise forms.ValidationError('Story must be at least 50 characters long.')
        return content
