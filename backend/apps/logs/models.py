from django.db import models
from django.conf import settings

class ChangeLog(models.Model):
    school_note = models.ForeignKey(
        'notes.SchoolNote', 
        on_delete=models.CASCADE,
        related_name='change_logs'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    field_changed = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.school_note} - {self.field_changed} - {self.timestamp}" 