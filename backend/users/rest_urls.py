from django.urls import path

from users.rest_views import RetrieveUserExistsView

urlpatterns = [
    path('<email>/exists/', RetrieveUserExistsView.as_view(), name="user_exists"),
]
