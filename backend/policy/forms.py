from django import forms

from users.models import User

from quote.models import QuoteProcess

class AdminPolicyForm(forms.ModelForm):
  quote_process = forms.ModelChoiceField(
      queryset=QuoteProcess.objects.all(),
      widget=forms.HiddenInput())
  user = forms.ModelChoiceField(
      queryset=User.objects.all(),
      widget=forms.HiddenInput())
      
  class Meta:
    fields = (
      'quote_process', 'user', 'policy_number', 'certificate_of_liability',
      'fh1_document', 'insurance_document', 'fee_amount'
    )
    widgets = {
      'fee_amount': forms.HiddenInput
    }
