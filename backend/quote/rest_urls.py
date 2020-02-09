from django.urls import path

from quote.rest_views import (
  CreateQuoteProcessView, RetrieveUpdateQuoteProcessView,
  RetrieveQuoteProcessView, CreateQuoteSoftFalloutView,
  UpdateQuoteProcessUserView, RetrieveCalcQuoteProcessVariationsView,
  UpdateQuoteProcessOptionsView, UpdateQuoteProcessDocumentsFileView,
  RetrieveQuoteProcessDocumentsView,
  CreateQuoteProcessDocumentsAccidentReportView, 
  UpdateQuoteProcessDocumentsAccidentReportView,
  DeleteQuoteProcessDocumentsAccidentReportView
)

urlpatterns = [
    path(
      'quote_process/create/', 
      CreateQuoteProcessView.as_view(), 
      name="create_quote_process"
    ),
    path(
        'quote_process/<uuid:pk>/',
        RetrieveQuoteProcessView.as_view(),
        name="retrieve_quote_process"
    ),
    path(
        'quote_process/<email>/',
        RetrieveUpdateQuoteProcessView.as_view(),
        name="retrieve_update_quote_process"
    ),
    path(
        'quote_process/<uuid:pk>/calc_variations/',
        RetrieveCalcQuoteProcessVariationsView.as_view(),
        name="calc_quote_process_variations"
    ),
    path(
        'quote_process/<uuid:pk>/update_options/',
        UpdateQuoteProcessOptionsView.as_view(),
        name="update_quote_process_options"
    ),
    path(
        'quote_process/<uuid:pk>/update_user/',
        UpdateQuoteProcessUserView.as_view(),
        name="update_quote_process_user"
    ),
    path(
      'quote_soft_fallout/create/',
      CreateQuoteSoftFalloutView.as_view(),
      name="create_quote_soft_fallout"
    ),
    path(
      'quote_process_documents/retrieve/',
      RetrieveQuoteProcessDocumentsView.as_view(),
      name="retrieve_quote_process_documents"
    ),
    path(
      'quote_process_documents/upload_file/',
      UpdateQuoteProcessDocumentsFileView.as_view(),
      name="update_quote_process_documents_file"
    ),
    path(
      'quote_process_documents_accident_report/create/',
      CreateQuoteProcessDocumentsAccidentReportView.as_view(),
      name="create_quote_process_documents_accident_report"
    ),
    path(
      'quote_process_documents_accident_report/<uuid:pk>/update/',
      UpdateQuoteProcessDocumentsAccidentReportView.as_view(),
      name="update_quote_process_documents_accident_report"
    ),
    path(
      'quote_process_documents_accident_report/<uuid:pk>/delete/',
      DeleteQuoteProcessDocumentsAccidentReportView.as_view(),
      name="delete_quote_process_documents_accident_report"
    ),
]
