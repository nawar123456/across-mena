from django.db import models

# Create your models here.

class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EmailModel(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.EmailField()
    date = models.DateTimeField()
    body = models.TextField()
