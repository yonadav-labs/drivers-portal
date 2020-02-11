from django import forms

from quote.models import QuoteProcess

class AdminQuoteProcessPaymentForm(forms.ModelForm):
  quote_process = forms.ModelChoiceField(
      queryset=QuoteProcess.objects.all(),
      widget=forms.HiddenInput())
      
  class Meta:
    fields = ('quote_process', 'official_hereford_quote', 'liability_amount', 'physical_amount')
