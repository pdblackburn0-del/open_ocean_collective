from django.contrib import admin
from .models import Profile, Meetup, MeetupSignup, Story, Comment, TripSignup
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(Story)
class StoryAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author', 'content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    summernote_fields = ('content',)


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('user', 'story', 'created_at')
    search_fields = ('content', 'user__username', 'story__title')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    summernote_fields = ('content',)


@admin.register(TripSignup)
class TripSignupAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'signed_up_at')
    search_fields = ('user__username', 'user__email', 'trip')
    list_filter = ('trip', 'signed_up_at')
    readonly_fields = ('signed_up_at',)
    ordering = ('-signed_up_at',)

