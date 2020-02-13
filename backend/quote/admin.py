from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from django_object_actions import DjangoObjectActions
from nested_admin import NestedStackedInline, NestedModelAdmin

from base.admin import stable_admin

from quote.models import (
    QuoteProcess, QuoteProcessDocuments, QuoteProcessDocumentsAccidentReport,
    QuoteProcessPayment
)
from quote.forms import AdminQuoteProcessPaymentForm

class QuoteProcessDocumentsAccidentReportInline(NestedStackedInline):
    model = QuoteProcessDocumentsAccidentReport
    extra = 0

class QuoteProcessDocumentsInline(NestedStackedInline):
    model = QuoteProcessDocuments
    inlines = [QuoteProcessDocumentsAccidentReportInline, ]

class QuoteProcessPaymentInline(NestedStackedInline):
  model = QuoteProcessPayment


class QuoteProcessAdmin(DjangoObjectActions, NestedModelAdmin):
    change_actions = ('generate_quote_link', 'add_user_manually' )
    inlines = [QuoteProcessDocumentsInline, QuoteProcessPaymentInline]

    def get_change_actions(self, request, object_id, form_url):
        actions = super(QuoteProcessAdmin, self).get_change_actions(
            request, object_id, form_url)
        actions = list(actions)

        obj = self.model.objects.get(pk=object_id)
        if obj.user:
            actions.remove('generate_quote_link')
            actions.remove('add_user_manually')
        return actions
    
    def add_user_manually(self, request, obj):
        return redirect(
            (
                f'{reverse("stable_admin:users_manualquoteuser_add")}'
                f'?quote_process={str(obj.id)}&email={str(obj.email)}'
            )
        )
    add_user_manually.label = 'Add User manually'

    def generate_quote_link(self, request, obj):
        messages.add_message(
            request, messages.INFO, f'Quote Page Link: stableins.com/{str(obj.id)}')
    generate_quote_link.label = 'Generate Quote Page Link'

admin.site.register(QuoteProcess)
stable_admin.register(QuoteProcess, QuoteProcessAdmin)

class QuoteProcessDocumentsAdmin(DjangoObjectActions, NestedModelAdmin):
    change_actions = ('view_full_quote_process',  'send_official_hereford_quote')
    inlines = [QuoteProcessDocumentsAccidentReportInline, ]

    def view_full_quote_process(self, request, obj):
        return redirect(
            reverse('stable_admin:quote_quoteprocess_change', args=(obj.quote_process.id, ))
        )
    view_full_quote_process.label = 'View Full Quote Process'

    def send_official_hereford_quote(self, request, obj):
      return redirect(
        (
            f'{reverse("stable_admin:quote_quoteprocesspayment_add")}'
            f'?quote_process={str(obj.quote_process_id)}'
        )
    )

    def get_change_actions(self, request, object_id, form_url):
      if object_id:
        obj = QuoteProcessDocuments.objects.get(id=object_id)
        if obj.is_submitted_for_review:
          return ('view_full_quote_process',  'send_official_hereford_quote')
      return ('view_full_quote_process', )

stable_admin.register(QuoteProcessDocuments, QuoteProcessDocumentsAdmin)


class QuoteProcessPaymentQuoteProccessInline(admin.StackedInline):
  fields = ('quote_amount', 'deposit', 'deductible', 'start_date')
  model = QuoteProcess
  read_only_fields = ('quote_amount', 'deposit', 'deductible', 'start_date')

class QuoteProcessPaymentAdmin(DjangoObjectActions, admin.ModelAdmin):
  change_form_template = "admin/quote/quoteprocesspayment/change_form.html"
  form = AdminQuoteProcessPaymentForm

  def get_form(self, request, obj=None, **kwargs):
    form = super(QuoteProcessPaymentAdmin, self).get_form(request, obj, **kwargs)
    quote_id = request.GET.get('quote_process')
    if quote_id:
      form.base_fields['quote_process'].initial = request.GET.get('quote_process')
    return form

  def response_add(self, request, obj):
      messages.add_message(
          request, messages.SUCCESS, f'The Payment has been sent to the user!')
      quote_process = obj.quote_process
      return redirect(
          reverse('stable_admin:quote_quoteprocess_change', args=(quote_process.id, ))
      )

stable_admin.register(QuoteProcessPayment, QuoteProcessPaymentAdmin)