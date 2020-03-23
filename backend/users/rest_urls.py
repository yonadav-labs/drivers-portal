from django.urls import path

from users.rest_views import (
  RetrieveUserExistsView, RetrieveCurrentUserView,
  UpdateUserPasswordView, RetrieveMagicLinkView,
  CheckTokenView, LoginView, UpdateUserEmailView
)

urlpatterns = [
    path('<email>/exists/', RetrieveUserExistsView.as_view(), name="user_exists"),
    path('current/', RetrieveCurrentUserView.as_view(), name="current_user"),
    path('current/set_password/', UpdateUserPasswordView.as_view(), name="set_password"),
    path('current/set_email/', UpdateUserEmailView.as_view(), name="set_email"),
    path('magic_link/<uuid:pk>/', RetrieveMagicLinkView.as_view(), name="use_magiclink"),
    path('check_token/', CheckTokenView.as_view(), name="check_token"),
    path('login/', LoginView.as_view(), name="login"),
]
