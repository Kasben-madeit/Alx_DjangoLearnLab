"""
URL configuration for the social_media_api project.

The ``urlpatterns`` list routes URLs to views.  For more information
please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

Examples
========

Function views
    1. Add an import:  ``from my_app import views``
    2. Add a URL to ``urlpatterns``:  ``path('example/', views.example, name='example')``

Class-based views
    1. Add an import:  ``from other_app.views import ExampleView``
    2. Add a URL to ``urlpatterns``:  ``path('example/', ExampleView.as_view(), name='example')``

Including another URLconf
    1. Import the ``include()`` function: from django.urls import include, path
    2. Add a URL to ``urlpatterns``:  ``path('blog/', include('blog.urls'))``
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),  # user authentication and profile
    path('api/', include('posts.urls')),          # posts, comments, likes and feed
    path('api/notifications/', include('notifications.urls')),  # notifications
]

# In development mode serve media files directly from Django.  In production
# you should configure your web server to serve ``MEDIA_ROOT`` under
# ``MEDIA_URL``.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)