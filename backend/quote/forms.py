from django import forms
from django.utils.safestring import mark_safe

from quote.models import QuoteProcess
from quote.constants import QUOTE_PROCESS_DEPOSIT_CHOICES


class AdminSendQuoteProcessPaymentForm(forms.ModelForm):
  quote_process = forms.ModelChoiceField(
    queryset=QuoteProcess.objects.all(),
    widget=forms.HiddenInput())

  def __init__(self, *args, **kwargs):
    super(AdminSendQuoteProcessPaymentForm, self).__init__(*args, **kwargs)
    self.fields['deposit_percentage'].required = True
      
  class Meta:
    fields = (
      'quote_process', 'official_hereford_quote', 'deposit_percentage', 
      'liability_amount', 'physical_amount', 'has_third_party_deposit',
      'third_party_name', 'third_party_amount', 'deposit_payment_amount', 
    )
    labels = {
      "has_third_party_deposit": "Is the deposit being partially covered by a 3rd party?",
      "third_party_name": "Who is covering part of the deposit?",
      "third_party_amount": "How much is being covered?",
    }
    widgets = {
      "has_third_party_deposit": forms.RadioSelect,
      "deposit_payment_amount": forms.HiddenInput,
    }
