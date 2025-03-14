from rest_framework import serializers
from .models import Home, Student, Behavior, SchoolNote, Period, BehaviorEntry, HomeworkEntry
from apps.accounts.models import CustomUser

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['id', 'name', 'is_active']

class StudentSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    home_name = serializers.CharField(source='home.name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'user_full_name', 'home', 'home_name', 'is_active']

class BehaviorEntrySerializer(serializers.ModelSerializer):
    behavior_name = serializers.CharField(source='behavior.name', read_only=True)
    
    class Meta:
        model = BehaviorEntry
        fields = ['id', 'behavior', 'behavior_name', 'is_positive', 'notes']

class PeriodSerializer(serializers.ModelSerializer):
    behavior_entries = BehaviorEntrySerializer(many=True, read_only=True)
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    
    class Meta:
        model = Period
        fields = ['id', 'period', 'teacher', 'teacher_name', 'behavior_entries']

class HomeworkEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkEntry
        fields = ['id', 'subject', 'description', 'teacher_acknowledgement']

class SchoolNoteSerializer(serializers.ModelSerializer):
    periods = PeriodSerializer(many=True, read_only=True)
    homework_entries = HomeworkEntrySerializer(many=True, read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    home_name = serializers.CharField(source='student.home.name', read_only=True)
    
    class Meta:
        model = SchoolNote
        fields = ['id', 'student', 'student_name', 'home_name', 'date', 
                 'extra_effort', 'areas_for_improvement', 'periods', 
                 'homework_entries', 'created_at', 'updated_at'] 