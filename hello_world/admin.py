from django.contrib import admin
from .models import Profile, Meetup, MeetupSignup, Story, Comment

# Register your models here.

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author', 'content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'created_at')
    search_fields = ('content', 'user__username', 'story__title')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
