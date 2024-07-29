from django.db import models
from django.contrib.auth.models import User

# User Profile model to store status
class UserProfile(models.Model):
    STATUS_CHOICES = [
        ('S', 'Student'),
        ('T', 'Teacher'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.user.username

# File model
class File(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.name