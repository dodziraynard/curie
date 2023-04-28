"""banga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('app/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('setup/', include('setup.urls')),
    path('pdf/', include('pdf_processor.urls')),
    path('api/v1/', include('graphql_api.urls')),
]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

# Customize django admin page.
admin.site.site_header = "LMS SYSTEM ADMINISTRATION"  # default: "Django Administration"
admin.site.index_title = "Site Administration"  # default: "Site Administration"
admin.site.site_title = 'LMS System site admin'  # default: "Django site admin"
