from django.contrib import admin
from .models import ContactFormSubmission, EmailModel

# Register your models here.
@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']


@admin.register(EmailModel)
class EmailModelAdmin(admin.ModelAdmin):
    search_fields = ['sender']
    list_display = ['sender']
