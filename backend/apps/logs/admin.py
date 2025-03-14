from django.contrib import admin
from .models import ChangeLog

@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('school_note', 'user', 'timestamp', 'field_changed')
    list_filter = ('timestamp', 'field_changed', 'user')
    search_fields = ('school_note__student__user__username', 'user__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',) 