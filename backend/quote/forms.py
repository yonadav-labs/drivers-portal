from django import forms

from quote.models import QuoteProcess


class AdminSendQuoteProcessPaymentForm(forms.ModelForm):
  quote_process = forms.ModelChoiceField(
      queryset=QuoteProcess.objects.all(),
      widget=forms.HiddenInput())
      
  class Meta:
    fields = (
      'quote_process', 'official_hereford_quote', 'deposit_payment_amount',
      'liability_amount', 'physical_amount'
    )
