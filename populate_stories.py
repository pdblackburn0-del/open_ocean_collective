#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openocean.settings')
django.setup()

from hello_world.models import Story, Comment
from django.contrib.auth.models import User

# Clear existing stories
Story.objects.all().delete()

# Create 3 stories
story1 = Story.objects.create(
    title="Finding My Voice in the Ocean",
    author="Sarah Ahmed",
    content="Three years ago, I never thought I'd be a surfer. Coming from an underrepresented background in British surfing, I felt like I didn't belong in the water. Then I discovered Open Ocean Collective, and everything changed. The welcoming community, diverse faces in the lineup, and supportive instructors gave me the confidence to pursue my passion. Now, I'm not just surfing—I'm thriving. Every wave feels like a victory, not just for me, but for everyone who told me this wasn't \"my space.\" Open Ocean Collective didn't just teach me to surf; they showed me that the ocean truly is for everyone.",
    image_url="https://res.cloudinary.com/dwe00uiuy/image/upload/v1771818012/piri_amgpqh.png"
)

story2 = Story.objects.create(
    title="From Landlocked to Wave Rider",
    author="Marcus Chen",
    content="Growing up in the Midlands, I never dreamed I'd be a surfer. Surfing seemed like something that happened in far-off places, not for people like me. When Open Ocean Collective organized a trip to Devon, I decided to give it a shot. I was terrified. I fell off my board more times than I can count, but the community never made me feel bad about it. They cheered me on, gave me tips, and made me feel like I belonged. Now, monthly trips are my therapy. Being on the water, surrounded by people who celebrate diversity as much as great waves, has transformed my life. I've found not just a hobby, but a family.",
    image_url="https://res.cloudinary.com/dwe00uiuy/image/upload/v1771818743/marcus_ns3wgs.webp"
)

story3 = Story.objects.create(
    title="Breaking Barriers, One Wave at a Time",
    author="Priya Desai",
    content="As a woman of color navigating the British surf scene, I faced more than just challenging waters. There were sidelong glances, assumptions, and times I felt invisible in the lineup. Open Ocean Collective changed everything. For the first time, I saw people who looked like me out there, breaking the stereotype. I found mentors, made lifelong friends, and most importantly, I found my voice. The ocean doesn't care about your background—it tests your courage, your determination, and your spirit. And Open Ocean Collective made sure I knew I deserved to be there. If you've ever felt like the ocean wasn't \"for you,\" I'm here to tell you: it absolutely is. Come join us. 🌊",
    image_url="https://res.cloudinary.com/dwe00uiuy/image/upload/v1771817513/Sarah_y4zgix.png"
)

print("Stories created successfully!")
print(f"Story 1: {story1.title} (ID: {story1.id})")
print(f"Story 2: {story2.title} (ID: {story2.id})")
print(f"Story 3: {story3.title} (ID: {story3.id})")
