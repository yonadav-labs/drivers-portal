from django.urls import path

from importer.rest_views import RetrieveTLCNameView

urlpatterns = [
    path('active_driver/<license_number>/', RetrieveTLCNameView.as_view(), name="retrieve-tlc")
]