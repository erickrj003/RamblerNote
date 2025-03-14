from django.contrib import admin
from .models import (Home, Student, Behavior, SchoolNote, 
                    Period, BehaviorEntry, HomeworkEntry)

@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    filter_horizontal = ('family_teachers',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'home', 'is_active')
    list_filter = ('home', 'is_active')
    search_fields = ('user__first_name', 'user__last_name')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Student Name'

@admin.register(Behavior)
class BehaviorAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_default')
    ordering = ('order',)
    search_fields = ('name',)

@admin.register(SchoolNote)
class SchoolNoteAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'created_at', 'updated_at')
    list_filter = ('date', 'student__home')
    search_fields = ('student__user__first_name', 'student__user__last_name')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('school_note', 'period', 'teacher')
    list_filter = ('period', 'teacher')
    search_fields = ('school_note__student__user__first_name', 'school_note__student__user__last_name')

@admin.register(BehaviorEntry)
class BehaviorEntryAdmin(admin.ModelAdmin):
    list_display = ('period', 'behavior', 'is_positive')
    list_filter = ('is_positive', 'behavior')
    search_fields = ('period__school_note__student__user__first_name', 'period__school_note__student__user__last_name')

@admin.register(HomeworkEntry)
class HomeworkEntryAdmin(admin.ModelAdmin):
    list_display = ('school_note', 'subject')
    search_fields = ('subject', 'school_note__student__user__first_name', 'school_note__student__user__last_name') 