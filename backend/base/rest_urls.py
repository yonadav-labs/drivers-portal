from django.urls import path

from base.rest_views import ApiStatusView

urlpatterns = [
  path('status/', ApiStatusView.as_view(), name="status")
]