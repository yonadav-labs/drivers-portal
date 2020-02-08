from django.views.generic import TemplateView

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from base.admin import stable_admin


api_urlpatterns = [
    path('api/v1/', include('stableins.api_urls')),
]

admin_urlpatterns = [
    path('nested_admin/', include('nested_admin.urls')),
    path('admin_tools/', include('admin_tools.urls')),
    path('django_admin/', admin.site.urls),
    path('admin/', stable_admin.urls)
]

urlpatterns = [
    # path(
    #     '',
    #     TemplateView.as_view(template_name="core/home.html"),
    #     name="home"
    # ),
    # path(
    #     'fleet/',
    #     TemplateView.as_view(template_name="core/fleet.html"),
    #     name="fleet"
    # ),
    # path(
    #     'dashboard/',
    #     TemplateView.as_view(template_name="core/dashboard.html"),
    #     name="dashboard"
    # ),
]

urlpatterns += api_urlpatterns
urlpatterns += admin_urlpatterns

if getattr(settings, "DEBUG", False):
    from django.views import defaults
    from django.views.static import serve
    from django.conf.urls.static import static
    urlpatterns += [
        path('500/', defaults.server_error, name='500'),
        path(
            '404/', defaults.page_not_found,
            {'exception': Exception()},
            name='404'
        )
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
