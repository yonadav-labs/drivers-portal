from django import forms
from django.contrib import messages

from quote.models import QuoteProcess
from users.proxy_models import ManualQuoteUser

class AdminManualQuoteUserForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(
        max_length=32, 
        widget=forms.PasswordInput,
        help_text="Leave blank if you want the user to create a password",
        required=False
    )
    confirm_password = forms.CharField(
        max_length=32, widget=forms.PasswordInput, required=False)
    quote_process = forms.ModelChoiceField(
        queryset=QuoteProcess.objects.without_user(),
        widget=forms.HiddenInput())

    class Meta:
        fields = ('email', 'password', 'confirm_password', 'quote_process')

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm_password']
        if password != confirm:
            raise forms.ValidationError("Passwords must match")
        return confirm

    def clean_quote_process(self):
        if not self.cleaned_data['quote_process']:
            messages.add_message(
                request, messages.ERROR, 'You followed an invalid link')
            raise forms.ValidationError("You followed an invalid link")
        return self.cleaned_data['quote_process']

    def save(self, commit=True):
        instance = super(AdminManualQuoteUserForm, self).save(commit=False)
        if self.cleaned_data['password']:
            instance.set_password(self.cleaned_data['password'])
        else:
            instance.set_unusable_password()
        instance.save()

        quote = self.cleaned_data['quote_process']
        quote.add_user(instance)
        return instance