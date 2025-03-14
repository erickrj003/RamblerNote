from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('family_teacher', 'Family Teacher'),
        ('student', 'Student'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    # homes = models.ManyToManyField('notes.Home', blank=True)  # For family teachers

    class Meta:
        permissions = [
            ("can_view_all_notes", "Can view all school notes"),
            ("can_edit_all_notes", "Can edit all school notes"),
            ("can_view_home_notes", "Can view home's school notes"),
        ] 