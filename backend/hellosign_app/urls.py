from django.conf.urls import url

from hellosign_app.views import HelloSignCallbackView


urlpatterns = [
  url(
    r'^callback/$',
    HelloSignCallbackView.as_view(),
    name='callback'
  ),
]
