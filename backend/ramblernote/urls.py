from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from apps.notes.views import HomeViewSet, SchoolNoteViewSet, PeriodViewSet, BehaviorEntryViewSet

router = DefaultRouter()
router.register(r'homes', HomeViewSet)
router.register(r'school-notes', SchoolNoteViewSet, basename='schoolnote')
router.register(r'periods', PeriodViewSet, basename='period')

admin.site.site_header = 'RamblerNote Administration'
admin.site.site_title = 'RamblerNote Admin Portal'
admin.site.index_title = 'Welcome to RamblerNote Admin Portal'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('apps.accounts.urls')),
]

# Add this for serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 