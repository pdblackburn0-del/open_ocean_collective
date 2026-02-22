from django.urls import path
from . import views

app_name = 'hello_world'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('meetups/', views.meetups, name='meetups'),
    path('stories/create/', views.create_story, name='create_story'),
    path("homepage/", views.homepage, name="homepage"),
]
