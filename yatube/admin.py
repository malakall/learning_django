from django.contrib import admin
from .models import Group, Contact

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "user_name")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "text")
