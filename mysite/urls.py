from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views as core_views  # <--- Import para sa home view

# ==========================================
# STANDARD ADMIN SITE (Gikuha ang CustomAdminSite)
# ==========================================

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('home/', core_views.home, name='home_redirect'),  # <--- IDUGANG ITO
    path('users/', include('apps.users.urls')),
    path('info/', include('apps.info.urls')),
    path('finder/', include('apps.food_finder.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)