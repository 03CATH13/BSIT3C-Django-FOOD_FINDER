from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin import AdminSite
from django.apps import apps

# ==========================================
# CUSTOM ADMIN SITE PARA ITAGO ANG FOOD_FINDER
# ==========================================
class CustomAdminSite(AdminSite):
    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        # Laktawan ang food_finder sa sidebar at dashboard
        return [app for app in app_list if app['app_label'] != 'food_finder']

# I-override ang default admin site
admin.site.__class__ = CustomAdminSite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('users/', include('apps.users.urls')),
    path('info/', include('apps.info.urls')),
    path('finder/', include('apps.food_finder.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)