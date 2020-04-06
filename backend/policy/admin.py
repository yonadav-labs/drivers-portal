from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from django_object_actions import DjangoObjectActions
from nested_admin import NestedTabularInline

from base.admin import stable_admin

from policy.forms import AdminPolicyForm
from policy.models import Policy, PolicyPayment
from policy.proxy_models import CreatePolicy
from quote.models import QuoteProcess
from quote.constants import HEREFORD_FEES


# Register your models here.

class CreatePolicyAdmin(DjangoObjectActions, admin.ModelAdmin):
  # change_form_template = "admin/policy/policy/change_form.html"
  form = AdminPolicyForm

  def get_form(self, request, obj=None, **kwargs):
    form = super(CreatePolicyAdmin, self).get_form(
        request, obj, **kwargs)
    quote_id = request.GET.get('quote_process')
    user = request.GET.get('user')
    if quote_id:
      form.base_fields['quote_process'].initial = request.GET.get(
          'quote_process')
      quote = QuoteProcess.objects.filter(id=quote_id).first()
      if quote:
        form.base_fields['fee_amount'].initial = HEREFORD_FEES.get(quote.deposit)
    if user:
      form.base_fields['user'].initial = request.GET.get(
          'user')
    return form

  def response_add(self, request, obj):
      messages.add_message(
          request, messages.SUCCESS, f'The Policy has been created')
      return redirect(
          reverse('stable_admin:policy_policy_change',
                  args=(obj.id, ))
      )


stable_admin.register(CreatePolicy, CreatePolicyAdmin)


class PolicyPaymentInline(NestedTabularInline):
    model = PolicyPayment
    fields = (
      'payment_due_date', 'payment_date', 'payment_amount',
      'fee_amount', 'is_deposit', 'is_paid'
    )
    extra = 0


class PolicyAdmin(admin.ModelAdmin):
  inlines = [PolicyPaymentInline, ]

  def save_model(self, request, obj, form, change):
    # Propagate fee amount change in policy to all unpaid payments
    if 'fee_amount' in form.changed_data:
      obj.policypayment_set.filter(
        is_paid=False
      ).update(
        fee_amount=obj.fee_amount
      )
    super(PolicyAdmin, self).save_model(request, obj, form, change)


stable_admin.register(Policy, PolicyAdmin)


admin.site.register(Policy)
admin.site.register(PolicyPayment)
