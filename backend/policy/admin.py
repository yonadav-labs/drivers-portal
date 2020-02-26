from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from django_object_actions import DjangoObjectActions

from base.admin import stable_admin

from policy.forms import AdminPolicyForm
from policy.models import Policy
from policy.proxy_models import CreatePolicy


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
stable_admin.register(Policy)
admin.site.register(Policy)
