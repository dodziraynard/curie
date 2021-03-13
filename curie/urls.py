from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("school.urls")),
    path("students/", include("students.urls")),
    path("staff/", include("staff.urls")),
    path("auth/", include("accounts.urls")),
    path("pdf/", include("pdf_engine.urls")),
    path("ajax/", include("ajax.urls")),
    path("sms/", include("sms.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
