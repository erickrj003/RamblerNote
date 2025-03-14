from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.notes.models import Student, SchoolNote
from datetime import datetime

class Command(BaseCommand):
    help = 'Creates school notes for all active students for the current day'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        
        # Skip weekends
        if today.weekday() >= 5:
            self.stdout.write('Skipping weekend')
            return
        
        active_students = Student.objects.filter(is_active=True)
        notes_created = 0
        
        for student in active_students:
            _, created = SchoolNote.objects.get_or_create(
                student=student,
                date=today
            )
            if created:
                notes_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {notes_created} school notes'
            )
        ) 