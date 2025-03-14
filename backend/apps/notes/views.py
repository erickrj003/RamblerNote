from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime, timedelta
from .models import (Home, Student, Behavior, SchoolNote, Period, 
                    BehaviorEntry, HomeworkEntry)
from .serializers import (HomeSerializer, StudentSerializer, SchoolNoteSerializer,
                         PeriodSerializer, BehaviorEntrySerializer, 
                         HomeworkEntrySerializer)
from apps.logs.models import ChangeLog
from django.conf import settings

class HomeViewSet(viewsets.ModelViewSet):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    permission_classes = [permissions.IsAdminUser]

class SchoolNoteViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolNoteSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.user_type == 'admin':
            return SchoolNote.objects.all()
        elif user.user_type == 'family_teacher':
            return SchoolNote.objects.filter(student__home__in=user.homes.all())
        elif user.user_type == 'teacher':
            return SchoolNote.objects.filter(periods__teacher=user).distinct()
        elif user.user_type == 'student':
            return SchoolNote.objects.filter(student__user=user)
        
        return SchoolNote.objects.none()
    
    def perform_update(self, serializer):
        old_instance = SchoolNote.objects.get(pk=self.get_object().pk)
        instance = serializer.save()
        
        # Log changes
        for field in serializer.changed_data:
            ChangeLog.objects.create(
                school_note=instance,
                user=self.request.user,
                field_changed=field,
                old_value=str(getattr(old_instance, field)),
                new_value=str(getattr(instance, field))
            )
    
    @action(detail=False, methods=['get'])
    def current_week(self, request):
        today = datetime.now().date()
        monday = today - timedelta(days=today.weekday())
        queryset = self.get_queryset().filter(
            date__gte=monday,
            date__lte=monday + timedelta(days=6)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PeriodViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Period.objects.all()
        elif user.user_type == 'teacher':
            return Period.objects.filter(teacher=user)
        return Period.objects.none()

class BehaviorEntryViewSet(viewsets.ModelViewSet):
    serializer_class = BehaviorEntrySerializer
    
    def get_queryset(self):
        return BehaviorEntry.objects.filter(
            period__school_note__id=self.kwargs['school_note_pk'],
            period__id=self.kwargs['period_pk']
        ) 