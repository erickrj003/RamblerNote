from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Home(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    family_teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='managed_homes',
        blank=True
    )
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    home = models.ForeignKey(Home, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.home.name}"

class Behavior(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)
    is_default = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class SchoolNote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    extra_effort = models.TextField(blank=True)
    areas_for_improvement = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'date']

class Period(models.Model):
    PERIOD_CHOICES = [
        (i, str(i)) for i in range(1, 12)
    ] + [('H', 'Hallway')]
    
    school_note = models.ForeignKey(SchoolNote, on_delete=models.CASCADE)
    period = models.CharField(max_length=2, choices=PERIOD_CHOICES)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

class BehaviorEntry(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    behavior = models.ForeignKey(Behavior, on_delete=models.PROTECT)
    is_positive = models.BooleanField()
    notes = models.TextField(blank=True)

class HomeworkEntry(models.Model):
    school_note = models.ForeignKey(SchoolNote, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    teacher_acknowledgement = models.TextField(blank=True) 