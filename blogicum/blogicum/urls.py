from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from blog import views as blog_views


handler404 = 'pages.views.page_not_found_view'
handler403 = 'pages.views.csrf_failure_view'
handler500 = 'pages.views.server_error_view'


urlpatterns = [
    path('auth/registration/', blog_views.register, name='registration'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
