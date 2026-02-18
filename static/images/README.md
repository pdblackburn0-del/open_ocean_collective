# Images Directory

This folder contains all images used throughout the Open Ocean Collective website.

## Folder Structure

```
images/
├── logo/           # Logo and branding images
├── hero/           # Hero section images
├── team/           # Team member photos
├── events/         # Event images
├── gallery/        # Photo gallery images
└── icons/          # Custom icons (if not using Font Awesome)
```

## Image Naming Convention

Use descriptive names in lowercase with hyphens:
- `ocean-wave-hero.jpg`
- `diverse-surfers-group.png`
- `beach-cleanup-event.jpg`

## Usage in Templates

Reference images in your HTML templates like this:

```html
{% load static %}
<img src="{% static 'images/logo/logo.png' %}" alt="Open Ocean Collective Logo">
```

## Optimization Tips

- Use WebP format for better compression
- Provide fallback JPG/PNG for older browsers
- Optimize images before uploading (resize, compress)
- Use appropriate alt text for accessibility

## Supported Formats

- JPG/JPEG (photographs)
- PNG (graphics with transparency)
- WebP (optimized web format)
- SVG (scalable graphics/logos)
