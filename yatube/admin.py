from django.contrib import admin
from .models import Group, Contact, Comment

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image","user_name")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "text")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'text', 'created')