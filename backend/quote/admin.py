from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from django_object_actions import DjangoObjectActions
from nested_admin import NestedStackedInline, NestedModelAdmin

from base.admin import stable_admin

from quote.models import (
    QuoteProcess, QuoteProcessDocuments, QuoteProcessDocumentsAciddentReport
)

class QuoteProcessDocumentsAciddentReportInline(NestedStackedInline):
    model = QuoteProcessDocumentsAciddentReport
    extra = 0

class QuoteProcessDocumentsInline(NestedStackedInline):
    model = QuoteProcessDocuments
    inlines = [QuoteProcessDocumentsAciddentReportInline, ]


class QuoteProcessAdmin(DjangoObjectActions, NestedModelAdmin):
    change_actions = ('generate_quote_link', 'add_user_manually' )
    inlines = [QuoteProcessDocumentsInline, ]

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
    change_actions = ('view_full_quote_process',  )
    inlines = [QuoteProcessDocumentsAciddentReportInline, ]

    def view_full_quote_process(self, request, obj):
        return redirect(
            reverse('stable_admin:quote_quoteprocess_change', args=(obj.quote_process.id, ))
        )
    view_full_quote_process.label = 'View Full Quote Process'

stable_admin.register(QuoteProcessDocuments, QuoteProcessDocumentsAdmin)