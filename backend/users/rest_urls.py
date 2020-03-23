from django.urls import path

from users.rest_views import (
  RetrieveUserExistsView, RetrieveCurrentUserView,
  UpdateUserPasswordView, RetrieveMagicLinkView,
  CheckTokenView, LoginView, ForgotPasswordView,
  ResetPasswordView
)

urlpatterns = [
    path('<email>/exists/', RetrieveUserExistsView.as_view(), name="user_exists"),
    path('current/', RetrieveCurrentUserView.as_view(), name="current_user"),
    path('current/set_password/', UpdateUserPasswordView.as_view(), name="set_password"),
    path('magic_link/<uuid:pk>/', RetrieveMagicLinkView.as_view(), name="use_magiclink"),
    path('check_token/', CheckTokenView.as_view(), name="check_token"),
    path('login/', LoginView.as_view(), name="login"),
    path('forgot_password/', ForgotPasswordView.as_view(), name="forgot_password"),
    path('reset_password/<pk>/', ResetPasswordView.as_view(), name="reset_password"),
]
