"""cdd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns

from .views import set_language

handler400 = 'dashboard.authentication.views.handler400'
handler403 = 'dashboard.authentication.views.handler403'
handler404 = 'dashboard.authentication.views.handler404'
handler500 = 'dashboard.authentication.views.handler500'



urlpatterns = [
    path('set-language/', 
         set_language, 
         name='set_language'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('attachments/', include('attachments.urls')),
    path('authentication/', include('authentication.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
)


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('attachments/', include('attachments.urls')),
#     path('i18n/', include('django.conf.urls.i18n')),
#     path('authentication/', include('authentication.urls')),
#     path('', include('dashboard.urls')),
#     path('api/', include('api.urls')),
# ]


if settings.DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    urlpatterns += [
        # YOUR PATTERNS
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        # Optional UI:
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
