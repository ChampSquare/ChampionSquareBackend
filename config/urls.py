"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views import defaults as default_view
from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [
    path('', TemplateView.as_view(template_name="pages/home.html"), name='home'),
    path('about/', TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # django admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # user management
    path('users/', include('champsquarebackend.users.urls', namespace='users')),
    path('accounts/', include('allauth.urls')),

    # urls for legacy site
    path('legacy/exam/', include('champsquarebackend.legacy.Uscholar.urls', namespace='Uscholar')),
    path('legacy/jee_main/', include('champsquarebackend.legacy.JeeMain.urls', namespace='JeeMain')),
    path('legacy/', include('champsquarebackend.legacy.Unicorn.urls', namespace="Unicorn")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, 
    # just visit these urls in browser to see what they look like

    urlpatterns += [
        path('400/', default_view.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path('403/', default_view.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        path('404/', default_view.page_not_found, kwargs={'exception': Exception('Page not found!')}),
        path('500/', default_view.server_error)
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


    
