from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import UserInformation, Answer, Feedback

# Register your Models
@admin.register(UserInformation)
class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'language', 'set_of_questions', 'level', 'question', 'answer')
    search_fields = ('user__username', 'language', 'level')
    list_filter = ('language', 'level')
    ordering = ('-id',)
    actions = ['mark_approved']

    def mark_approved(self, request, queryset):
        queryset.update(approved=True)
    mark_approved.short_description = "Mark selected answers as approved"

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'feedback_text', 'created_at')
    search_fields = ('answer__id', 'feedback_text')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
