# Cloudinary Setup Guide for Open Ocean Collective

## Configuration Instructions

### 1. Get Your Cloudinary Credentials

1. Sign up at https://cloudinary.com (free tier available)
2. Go to your Dashboard
3. Copy your credentials:
   - **Cloud Name** (visible at top)
   - **API Key** (in Settings)
   - **API Secret** (in Settings)

### 2. Set Environment Variables

#### Local Development
Create a `.env` file in your project root:
```bash
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

#### Heroku Production
Set config variables:
```bash
heroku config:set CLOUDINARY_CLOUD_NAME=your_cloud_name --app open-ocean
heroku config:set CLOUDINARY_API_KEY=your_api_key --app open-ocean
heroku config:set CLOUDINARY_API_SECRET=your_api_secret --app open-ocean
```

### 3. Using Cloudinary in Your Django Models

Example with a User Profile model:

```python
from cloudinary.models import CloudinaryField
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField('image', null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
```

### 4. Using in Templates

```html
{% load cloudinary %}

<!-- Display an image -->
<img src="{{ profile.profile_image.url }}" alt="Profile" class="img-fluid">

<!-- With transformations -->
<img src="{{ profile.profile_image|cloudinary_url:width=300,height=300,crop='fill' }}" alt="Profile">
```

### 5. Upload Forms

```python
from django import forms
from cloudinary.models import CloudinaryField

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'bio']
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
```

### 6. Cloudinary Transformations

Common image transformations in URLs:
- `width=300` - Set width
- `height=300` - Set height
- `crop='fill'` - Crop to fill dimensions
- `crop='fit'` - Fit within dimensions
- `quality='auto'` - Auto optimize quality
- `fetch_format='auto'` - Auto format (webp, jpg, etc)

Example:
```html
<img src="{{ image|cloudinary_url:width=500,height=500,crop='fill',quality='auto',fetch_format='auto' }}" />
```

## Benefits

✅ No local storage needed  
✅ Automatic image optimization  
✅ CDN distribution for fast loading  
✅ Responsive image handling  
✅ Image transformations on-the-fly  
✅ Scalable for production  

## Free Tier Limits

- Up to 25GB total storage
- 2GB monthly bandwidth
- 7,500 monthly transformations
- Great for most projects!

## Next Steps

1. Create user models with profile images
2. Add image fields to your forms
3. Test uploading images locally
4. Deploy to Heroku and set environment variables
