from django.urls import path

from quote.rest_views import (
  CreateQuoteProcessView, RetrieveUpdateQuoteProcessView,
  RetrieveQuoteProcessView
)

urlpatterns = [
    path(
      'quote_process/create/', 
      CreateQuoteProcessView.as_view(), 
      name="create-quote-process"
    ),
    path(
        'quote_process/<uuid:pk>/',
        RetrieveQuoteProcessView.as_view(),
        name="retrieve-quote-process"
    ),
    path(
        'quote_process/<email>/',
        RetrieveUpdateQuoteProcessView.as_view(),
        name="retrieve-update-quote-process"
    ),
]
