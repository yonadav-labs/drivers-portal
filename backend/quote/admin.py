import csv

from django.contrib import admin
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from django_object_actions import DjangoObjectActions
from nested_admin import NestedStackedInline, NestedModelAdmin

from base.admin import stable_admin
from base.tasks import send_user_quote_task
from users.models import MagicLink

from quote.models import (
    QuoteProcess, QuoteProcessDocuments, QuoteProcessDocumentsAccidentReport,
    QuoteProcessPayment, QuoteSoftFallout, QuoteProcessVariations
)
from quote.proxy_models import (
    SendQuoteProcessPayment
)
from quote.forms import AdminSendQuoteProcessPaymentForm
from quote.resources import get_quote_export

class QuoteProcessDocumentsAccidentReportInline(NestedStackedInline):
    model = QuoteProcessDocumentsAccidentReport
    extra = 0

class QuoteProcessDocumentsInline(NestedStackedInline):
    model = QuoteProcessDocuments
    inlines = [QuoteProcessDocumentsAccidentReportInline, ]

class QuoteProcessPaymentInline(NestedStackedInline):
  model = QuoteProcessPayment


class QuoteProcessVariationsInline(NestedStackedInline):
  model = QuoteProcessVariations

def export_as_csv(modeladmin, request, queryset):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="quote_process.csv"'

  if len(queryset):
    header_set = False
    writer = None
    for quote in queryset:
        quote_headers, export = get_quote_export(quote)
        if not header_set:
            writer = csv.DictWriter(response, fieldnames=quote_headers)
            writer.writeheader()
            header_set = True
        writer.writerow(export)
    return response


class QuoteProcessAdmin(DjangoObjectActions, NestedModelAdmin):
    change_actions = ('generate_dashboard_link', 'generate_quote_link', 'add_user_manually' )
    actions = (export_as_csv, )
    inlines = [QuoteProcessVariationsInline, QuoteProcessDocumentsInline, QuoteProcessPaymentInline]

    def get_change_actions(self, request, object_id, form_url):
        actions = super(QuoteProcessAdmin, self).get_change_actions(
            request, object_id, form_url)
        actions = list(actions)

        obj = self.model.objects.get(pk=object_id)
        if obj.user:
            actions.remove('generate_quote_link')
            actions.remove('add_user_manually')
        else:
          actions.remove('generate_dashboard_link')
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
            request, messages.INFO, f'Quote Page Link: {settings.FRONTEND_URL}/quote/{str(obj.id)}')
    generate_quote_link.label = 'Generate Quote Page Link'

    def generate_dashboard_link(self, request, obj):
        if obj.user:
          ml, created = MagicLink.objects.get_or_create(
              user=obj.user, valid_forever=True)
          messages.add_message(
              request, messages.INFO, f'Dashboard Link: {ml.get_url()}')
    generate_dashboard_link.label = 'Generate Dashboard Link'

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
            f'{reverse("stable_admin:quote_sendquoteprocesspayment_add")}'
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

class SendQuoteProcessPaymentAdmin(DjangoObjectActions, admin.ModelAdmin):
  change_form_template = "admin/quote/quoteprocesspayment/change_form.html"
  form = AdminSendQuoteProcessPaymentForm

  def get_form(self, request, obj=None, **kwargs):
    form = super(SendQuoteProcessPaymentAdmin, self).get_form(request, obj, **kwargs)
    quote_id = request.GET.get('quote_process')
    if quote_id:
      form.base_fields['quote_process'].initial = request.GET.get(
          'quote_process')
    return form

  def response_add(self, request, obj):
      send_user_quote_task.delay(str(obj.quote_process.user.id))
      messages.add_message(
          request, messages.SUCCESS, f'The Payment has been sent to the user!')
      quote_process = obj.quote_process
      return redirect(
          reverse('stable_admin:quote_quoteprocess_change',
                  args=(quote_process.id, ))
      )
stable_admin.register(SendQuoteProcessPayment, SendQuoteProcessPaymentAdmin)


class QuoteProcessPaymentAdmin(DjangoObjectActions, admin.ModelAdmin):
  change_actions = ('create_policy', 'view_full_quote_process', )

  def view_full_quote_process(self, request, obj):
      return redirect(
          reverse('stable_admin:quote_quoteprocess_change',
                  args=(obj.quote_process.id, ))
      )
  view_full_quote_process.label = 'View Full Quote Process'

  def create_policy(self, request, obj):
    return redirect(
        (
            f'{reverse("stable_admin:policy_createpolicy_add")}'
            f'?quote_process={str(obj.quote_process_id)}'
            f'&user={str(obj.quote_process.user.id)}'
        )
    )

  def get_change_actions(self, request, object_id, form_url):
    if object_id:
      obj = QuoteProcessPayment.objects.get(id=object_id)
      if not obj.is_paid:
        return ('view_full_quote_process', )
      return self.change_actions
    return ()

stable_admin.register(QuoteProcessPayment, QuoteProcessPaymentAdmin)
admin.site.register(QuoteProcessPayment)

stable_admin.register(QuoteSoftFallout)
admin.site.register(QuoteSoftFallout)
